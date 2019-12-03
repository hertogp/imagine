#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''\
Imagine
  A pandoc filter to turn fenced codeblocks into graphics or ascii art by
  wrapping some external command line utilities, such as:

    %(cmds)s


Installation

    %% sudo -H pip install pandoc-imagine

    or simply save `pandoc_imagine.py` anywhere along python's sys.path


Dependencies

    %% sudo -H pip install pandocfilters six

    and one (or more) of the packages that provide above utilities.


Pandoc usage

    %% pandoc --filter pandoc-imagine document.md -o document.pdf


Markdown usage

    ```cmd
    code
    ```

  Alternate, longer form:

    ```{.cmd im_opt=".." ...}
    code
    ```

  which will run `cmd` (if known) to proces the `code` into an image and
  replaces the fenced code block with an Image in a paragraph of its own or any
  ascii art in its own CodeBlock.

  If the command fails, the original fenced code block is retained unchanged.
  Usually, only errors are printed to stderr but you can get more info by
  setting the `im_log` option (see below).

  If the command succeeds but produces no image, a line reporting the missing
  image is included in the output document.


Imagine options

  Imagine's behaviour can be influenced by setting these options:

  - im_opt="" or any cli-options to pass in on the command line.
    Some classes already provide some defaults (as required by the command).

  - im_out="img", or ordered csv-list of keywords indicating what to produce:
    - img     an image-link in a paragraph
    - fcb     anonymous codeblock containing the original codeblock
    - stdout, anonymous codeblock containing captured stdout (if any)
    - stderr, anonymous codeblock containing captured stderr (if any)

    Some workers ignore 'img' by necessity since they donot produce graphical
    data that can be linked to, e.g. `figlet` or `protocol`, while others the
    'stdout' will ignored because that's were they produce their graphical
    data.

  - im_prg=None, or a cli-cmd name to override class-to-command map.
    Normally, the class on the code block is mapped to a command line tool to
    use. For example,
    ```gri
    ..
    ```
    maps gri to `gri`, but that can be changed by `{.gri im_prg="gri2"} to use
    `gri2` instead of `gri`.

  - im_fmt="png", or another output format of your choosing depending on the
    command line tool used.  Some tools donot derive their output image format
    from an intended output file name extension, but instead require it to be
    set in the tool's codeblock containing its instructions.  Be sure the code
    in the codeblock matches `im_fmt` or pandoc may have trouble assembling the
    final document.

  - im_dir="pd", or antoher absolute or relative (to the working directory)
    path in which input/output files are to be stored during processing.
    Note that an "-images" is still tacked onto the end of the path though.

  - im_log=0, which defaults to printing only errors caught during processing.
    Set it to -1 to completely silence Imagine, or as high as 4 for debug level
    output if somethings goes wrong and you need more information on what is
    going on.

  Option values are resolved in order of most to least specific::

  1. {.klass im_xyz=".."}       codeblock specific
  2. imagine.klass.im_xyz: ..   metadata, klass specific
  3. imagine.im_xyz             metadata, imagine specific
  4. class variable             hardcoded default

  Notes:
  - filenames are based on a hash of the codeblock + its attributes
  - uses subdir `{im_dir}-images` to store any input/output files
  - there's no clean up of files stored there
  - if an output filename exists, it is not regenerated but simply linked to.
  - `packetdiag`'s underlying library seems to have some problems.

  Some commands follow a slightly different pattern:
  - 'img' directive is ignored by commands that only produce ascii
  - ctioga2 defaults to pdf instead of png
  - flydraw produces a gif, not png
  - gle also creates a .gle subdir inside the images-dir
  - gri produces a ps, which is `convert`ed to png
  - imagine reads its code as help-topics, returns codeblocks with help-info
  - plot reads its codeblock as the relative path to the file to process
  - pyxplot will have `set terminal` & `set output` prepended to its `code`
  - shebang runs its codeblock as a script with <fname>.{im_fmt} as its argument.
    - use {.shebang im_out="stdout"} for text instead of an png


Security

  Imagine just hands the fenced codeblocks to plotting tools to process or
  simply runs them as system scripts, as-is.

  Shebang's are inherently unsafe and most of the plotting tools implement
  their own 'little' languages, which can create beautiful images, but can also
  cause harm.

  There is no way to check for 'side effects' in advance, so make sure to check
  the fenced codeblocks before running them through the filter.


Imagine class

The imagine class puts documentation of topics at your fingertips, like so:

    ```imagine
    klass
    ```

  Use `imagine` as klass to get the module's docstring (ie this text) and/or
  one or more of the commands you're interested in, each on a separate line.


Thanks for feedback:

  amietn, chdemko, heyrict, priiduonu, K4zuki
'''

from __future__ import print_function

import os
import sys
import stat
from textwrap import wrap
from subprocess import Popen, CalledProcessError, PIPE

# non-standard libraries
from six import with_metaclass
import pandocfilters as pf

# Author: Pieter den Hertog
# Email: git.hertogp@gmail.com
#
#-- Candidates:
# o grace (ie gracebat, the batchmode variant; indirect mode?)
#   script files are pretty big.  Perhaps indirectly.  It supports a batch mode
#   via `gracebat`, which symlinks to the real binary executable.
#
# o tizk, needs convert since eps wont go into pdflatex ..

# Notes:
# - using svg requires rsvg-convert which pandoc uses to convert the svg to
#   png before including in pdf
#   + sudo apt-get install librsvg2-bin


#-- version

__version__ = '0.1.6rc0'

#-- helpers
def to_str(s, enc='ascii'):
    'return encoded byte stream for s. PY2->str, PY3->bytes'
    err = 'replace'
    if isinstance(s, str):
        return s
    if isinstance(s, bytes):
        return s.decode(enc, err)
    try:
        # PY2 unicode object?
        return s.encode(enc, err)
    except AttributeError:
        # s is not a string
        return to_str(str(s))


def to_bytes(s, enc='ascii'):
    'return decoded char sequence for s'
    # in PY2 isinstance(str(), bytes) == True
    err = 'replace'
    if isinstance(s, bytes):
        try:
            return s.decode(enc, err).encode(enc, err)  # PY2
        except AttributeError:
            return s.encode(enc, err)  # PY3

    if isinstance(s, str):
        try:
            return s.encode(enc, err)  # PY3
        except UnicodeDecodeError:
            return s.decode(enc, err).encode(enc, err)  # PY2

    try:
        # sys.getfilesystemencoding()
        return to_bytes(str(s), sys.getdefaultencoding())
    except UnicodeEncodeError:
        return s.encode(enc, err)

# Notes:
# - if walker does not return anything, the element is kept
# - if walker returns a block element, it'll replace current element
# - block element = {'c': <value>, 't': <block_type>}


class HandlerMeta(type):
    'metaclass to register Handler subclasses (aka workers)'
    def __init__(cls, name, bases, dct):
        'register worker classes by cmdmap keys'
        super(HandlerMeta, cls).__init__(name, bases, dct)
        for klass in dct.get('cmdmap', {}):
            cls.workers[klass.lower()] = cls


class Handler(with_metaclass(HandlerMeta, object)):
    'baseclass for image/ascii art generators'
    severity = 'error warn note info debug'.split()
    workers = {}              # dispatch map for Handler, filled by HandlerMeta
    klass = None              # __call__ dispatches a worker & sets this
    meta = {}                 # stores user prefs in doc's meta yaml block
    cmdmap = {}               # worker subclass overrides, klass->cli-program
    # FIXME: output became im_out
    output = 'img'            # output an img by default, some workers should
                              #  override this with stdout (eg Boxes, Figlet..)

    # Imagine defaults for worker options
    im_dir = 'pd'             # dir for images (absolute or relative to cwd)
    im_fmt = 'png'            # default format for image creation
    im_log = 0                # log on notification level
    im_opt = ''               # options to pass in to cli-program
    im_out = 'img'            # what to output: csv-list img,fcb,stdout,stderr
    im_prg = None             # cli program to use to create graphic output

    # im_out is an ordered csv-list of what to produce:
    # - 'img'    outputs a link to an image (if any was produced)
    # - 'fcb'    outputs an anonymous codeblock showing the original codeblock
    # - 'stdout' outputs an anonymous codeblock showing a capture of stdout
    # - 'stderr' outputs an anonymous codeblock showing a capture of stderr


    def __call__(self, codec, fmt, meta):
        'Return worker class or self (Handler keeps CodeBlock unaltered)'
        # CodeBlock's value = [(Identity, [classes], [(key, val)]), code]
        self.msg(4, 'dispatch request for', codec[0])

        # get classes and keyvals from codeblock attributes
        try:
            _, klasses, keyvals = codec[0]
        except Exception as e:
            self.msg(0, 'Fatal:  invalid codeblock passed in', codec)
            raise e

        # try dispatching by class attribute
        for klass in klasses:
            worker = self.workers.get(klass.lower(), None)
            if worker is not None:
                worker.klass = klass.lower()
                self.msg(4, '- dispatched by class to', worker)
                return worker(codec, fmt, meta)

        # try dispatching via 'cmd' named by 'im_prg=cmd' key-value-pair
        if keyvals:  # pf.get_value barks if keyvals == []
            prog, _ = pf.get_value(keyvals, 'im_prg', '')
            worker = self.workers.get(prog.lower(), None)
            if worker is not None:
                self.msg(4, codec[0], 'dispatched by prog to', worker)
                return worker(codec, fmt,  meta)

        self.msg(4, codec[0], 'dispatched by default to', self)
        return self

    def __init__(self, codec, fmt, meta):
        'init by decoding the CodeBlock-s value'
        self.codec = codec # save original codeblock for later
        self.fmt = fmt     # some workers (flydraw) need access to this

        self.stdout = ''   # catches stdout by self.cmd, if any
        self.stderr = ''   # catches stderr by self.cmd, if any

        if codec is None:
            return         # initial dispatch creation

        # Options from to codeblock, meta data or imagine defaults
        cb = self.get_cb_opts(codec)                     # codeblock attrs
        kd = self.get_md_opts(meta).get(self.klass, {})  # metadata.klass
        md = self.md_opts                                # metadata (toplevel)
        opts = [x for x in dir(self) if x.startswith('im_')]
        for opt in opts:
            val = cb.get(opt,                      # 1 codeblock.opt
                    kd.get(opt,                    # 2 imagine.klass.opt (meta)
                        md.get(opt,                # 3 imagine.opt (meta)
                            getattr(self, opt))))  # 4 class.opt (class's code)
            setattr(self, opt, val)

        # post-process options
        self.im_opt = self.im_opt.split()
        self.im_out = self.im_out.lower().replace(',', ' ').split()
        self.im_log = int(self.im_log)
        self.im_fmt = pf.get_extension(fmt, self.im_fmt)

        if not self.im_prg:
            # if no im_prg was found, fallback to klass's cmdmap
            self.im_prg = self.cmdmap.get(self.klass, None)

        if self.im_prg is None:
            self.msg(0, self.klass, 'not listed in', self.cmdmap)
            raise Exception('no worker found for %s' % self.klass)

        self.basename = pf.get_filename4code(self.im_dir, str(codec))
        self.outfile = self.basename + '.%s' % self.im_fmt
        self.inpfile = self.basename + '.%s' % self.klass # _name.lower()

        if not os.path.isfile(self.inpfile):
            self.write('w', self.code, self.inpfile)

    def get_md_opts(self, meta):
        'pickup user preferences from meta block'
        dct = {}
        try:
            sep = "."
            for k,v in meta.items():
                if not k.lower().startswith("imagine."): continue
                if k.count(sep) == 1:
                    _, opt = k.split(sep)         # imagine.option: value
                    dct[opt] = pf.stringify(v)
                elif k.count(sep) == 2:
                    _, klass, opt = k.split(sep)  # imagine.klass.option: val
                    # klass = klass.lower()
                    if not dct.get(klass): dct[klass] = {}
                    dct[klass][opt] = pf.stringify(v)

        except AttributeError:
            pass

        self.msg(4, "meta-data:", dct)
        self.md_opts = dct
        return dct

    def get_cb_opts(self, codec):
        'pickup user preferences from code block'
        # also removes imagine class/attributes from code block, by
        # retaining only non-Imagine stuff in self.classes and self.keyvals
        dct = {}
        opts = [x for x in dir(self) if x.startswith('im_')]

        (self.id_, self.classes, self.keyvals), self.code = codec
        self.caption, self.typef, self.keyvals = pf.get_caption(self.keyvals)

        # - remove all Imagine-related classes from codeblock attributes
        self.classes = [k for k in self.classes if k not in self.workers]

        for opt in opts:
            val, self.keyvals = pf.get_value(self.keyvals, opt, None)
            if val: dct[opt] = val

        self.cb_opts = dct
        self.msg(4, "codeblock:", dct)
        return dct



    def read(self, mode, src):
        'read a file with given mode or return empty string'
        try:
            with open(src, mode) as f:
                return f.read()
        except (OSError, IOError) as e:
            self.msg(0, 'fail: could not read %si (%s)' % (src, repr(e)))
            return ''
        return ''

    def write(self, mode, dta, dst):
        'write a file, return success boolean indicator'
        if not dta:
            self.msg(3, 'skipped writing 0 bytes to', dst)
            return False
        try:
            with open(dst, mode) as f:
                f.write(dta)
            self.msg(3, 'wrote:', len(dta), 'bytes to', dst)
        except (OSError, IOError) as e:
            self.msg(0, 'fail: could not write', len(dta), 'bytes to', dst)
            self.msg(0, '>>: exception', e)
            return False
        return True

    def msg(self, level, *a):
        'possibly print a message to stderr'
        if level > self.im_log: return
        level %= len(self.severity)
        msg = '%s[%-9s:%5s] %s' % ('Imagine',
                                   self.__class__.__name__,
                                   self.severity[level],
                                   ' '.join(to_str(s) for s in a))
        print(msg, file=sys.stderr)
        sys.stderr.flush()

    def url(self):
        'return an image link for existing/new output image-file'
        # pf.Image is an Inline element. Callers usually wrap it in a pf.Para
        return pf.Image([self.id_, self.classes, self.keyvals],
                        self.caption, [self.outfile, self.typef])

    def anon_codeblock(self):
        'reproduce the original CodeBlock inside an anonymous CodeBlock'
        (id_, klasses, keyvals), code = self.codec
        id_ = '#' + id_ if id_ else id_
        klasses = ' '.join('.%s' % c for c in klasses)
        keyvals = ' '.join('%s="%s"' % (k, v) for k, v in keyvals)
        attr = '{%s}' % ' '.join(a for a in [id_, klasses, keyvals] if a)
        # prefer ```cmd over ```{.cmd}
        attr = attr if attr.find(' ') > -1 else attr[2:-1]
        codeblock = '```%s\n%s\n```' % (attr, code)
        return pf.CodeBlock(['', [], []], codeblock)

    def result(self):
        'return FCB, Para(url()) and/or CodeBlock(stdout) as ordered'
        rv = []
        enc = sys.getdefaultencoding()  # result always unicode
        for output_elm in self.im_out:
            if output_elm == 'img':
                if os.path.isfile(self.outfile):
                    rv.append(pf.Para([self.url()]))
                else:
                    msg = '?? missing %s' % self.outfile
                    self.msg(1, '>>:', msg)
                    rv.append(pf.Para([pf.Str(msg)]))

            elif output_elm == 'fcb':
                rv.append(self.anon_codeblock())

            elif output_elm == 'stdout':
                if self.stdout:
                    attr = ['', self.classes, self.keyvals]
                    rv.append(pf.CodeBlock(attr, to_str(self.stdout, enc)))
                else:
                    self.msg(1, '>>:', 'stdout requested, but saw nothing')

            elif output_elm == 'stderr':
                if self.stderr:
                    attr = ['', self.classes, self.keyvals]
                    rv.append(pf.CodeBlock(attr, to_str(self.stderr, enc)))
                else:
                    self.msg(1, '>>:', 'stderr requested, but saw nothing')

        if not rv:
            return None               # no results; None keeps original FCB
        if len(rv) > 1:
            return rv                 # multiple results
        return rv[0]                  # just 1 block level element

    def cmd(self, *args, **kwargs):
        'run, possibly forced, a cmd and return success indicator'
        forced = kwargs.get('forced', False)  # no need to pop
        stdin = kwargs.get('stdin', None)

        if os.path.isfile(self.outfile) and forced is False:
            self.msg(4, 're-use: {!r}'.format(self.outfile))
            return True

        try:
            self.msg(4, 'exec: ', *args)
            pipes = {'stdin': None if stdin is None else PIPE,
                     'stdout': PIPE,
                     'stderr': PIPE}
            p = Popen(args, **pipes)

            out, err = p.communicate(to_bytes(stdin))
            self.stdout = out
            self.stderr = err

            # STDERR
            if self.stderr and not 'stderr' in self.im_out:
                # not meant to capture, so simply print
                for line in self.stderr.splitlines():
                    self.msg(1, '<stderr>', line)
            elif self.stderr:
                self.msg(4, '<stderr>',
                         'captured {} bytes'.format(len(self.stderr)))
            else:
                self.msg(4, '<stderr>', 'no output seen')

            # STDOUT
            if self.stdout:
                self.msg(4, '<stdout>',
                    'saw {} bytes'.format(len(self.stdout)))
            else:
                self.msg(4, '<stdout>', 'no output seen')

            if os.path.isfile(self.outfile):
                # Note: not every worker actually produces an output file
                # e.g. because it captures stdout into a fenced codeblock
                # which is added to the document's AST
                self.msg(4, 'created: {!r}'.format(self.outfile))

            return p.returncode == 0

        except (OSError, CalledProcessError) as e:
            try:
                os.remove(self.outfile)
            except OSError:
                pass
            self.msg(1, 'fail:', *args)
            self.msg(1, 'msg:', self.im_prg, str(e))
            return False

    def image(self):
        'return an Image url or None to keep CodeBlock'
        # For cases where no handler could be associated with a fenced
        # codeblock, Handler itself will be the 'worker' who returns None
        # preserving the original codeblock as-is in the json AST.
        # Real workers (subclassing Handler) must override this method
        self.msg(2, 'CodeBlock ignored, keeping as-is')
        return None


class Asy(Handler):
    '''
    sudo-apt-get install asymptote

    See http://asymptote.sourceforge.net/
    '''
    cmdmap = {'asy': 'asy', 'asymptote': 'asy'}
    im_fmt = 'png'

    def image(self):
        'asy -o <fname>.{im_fmt} {im_opt} <fname>.asy'
        args = ['-o', self.outfile] + self.im_opt + [self.inpfile]
        if self.cmd(self.im_prg, *args):
            return self.result()


class Boxes(Handler):
    '''
    sudo apt-get install boxes
    http://boxes.thomasjensen.com
    '''
    cmdmap = {'boxes': 'boxes'}
    im_fmt = 'boxed'
    output = 'stdout'  # i.e. default to stdout

    def image(self):
        'boxes {im_opt} <fname>.boxes'

        # boxes produces text only, so silently ignore 'img'
        self.im_out = [x for x in self.im_out if x not in ['img']]
        args = self.im_opt + [self.inpfile]
        if self.cmd(self.im_prg, *args):
            if self.stdout:
                self.write('w', to_str(self.stdout), self.outfile)
            else:
                self.stdout = self.read('r', self.outfile)
            return self.result()


class BlockDiag(Handler):
    '''
    sudo pip install blockdiag nwdiag actdiag seqdiag
    http://blockdiag.com/
    '''
    progs = 'blockdiag seqdiag rackdiag nwdiag packetdiag actdiag'.split()
    cmdmap = dict(zip(progs, progs))

    def image(self):
        '{im_prg} {im_opt} -T {im_fmt} <fname>.{im_fmt} -o <fname>.{im_prg}'
        args = self.im_opt + ['-T', self.im_fmt, self.inpfile, '-o', self.outfile]
        if self.cmd(self.im_prg, *args):
            return self.result()


class Ctioga2(Handler):
    '''
    sudo apt-get install ctioga2
    http://ctioga2.sourceforge.net
    '''
    cmdmap = {'ctioga2': 'ctioga2'}
    im_fmt = 'pdf'

    def image(self):
        'ctioga2 {im_opt} -f <fname>.ctioga2'
        args = self.im_opt + ['-f', self.inpfile]
        if self.cmd(self.im_prg, *args):
            return self.result()


class Ditaa(Handler):
    '''
    sudo apt-get install ditaa
    http://ditaa.sourceforge.net
    '''
    cmdmap = {'ditaa': 'ditaa'}

    def image(self):
        'ditaa <fname>.ditaa <fname>.{im_fmt} {im_opt}'
        args = [self.inpfile, self.outfile] + self.im_opt
        if self.cmd(self.im_prg, *args):
            return self.result()


class Figlet(Handler):
    '''
    sudo apt-get install figlet
    http://www.figlet.org
    '''
    # - saves code-text to <fname>.figlet
    # - saves stdout to <fname>.figled
    cmdmap = {'figlet': 'figlet'}
    im_fmt = 'figled'

    def image(self):
        'figlet {im_opt} < code-text'
        # silently ignore any request for an 'image'
        self.im_out = [x for x in self.im_out if x not in ['img']]

        args = self.im_opt
        if self.cmd(self.im_prg, stdin=self.code, *args):
            if self.stdout:
                # save figlet's stdout to outfile for next time around
                self.write('w', to_str(self.stdout), self.outfile)
            else:
                self.stdout = self.read('r', self.outfile)
            return self.result()


class Flydraw(Handler):
    '''
    sudo apt-get install flydraw
    http://manpages.ubuntu.com/manpages/precise/man1/flydraw.1.html
    notes:
    - graphic data is printed to stdout
    - so 'stdout' in im_out option is silently ignored
    '''
    # - flydraw reads its commands from stdin & produces output on stdout
    cmdmap = {'flydraw': 'flydraw'}

    def image(self):
        'flydraw {im_opt} < code-text'
        # override im_fmt/outfile since, despite the manual, it insists on gif
        self.im_fmt = 'gif'
        self.outfile = self.basename + '.%s' % self.im_fmt
        self.msg(4, "im_fmt", self.im_fmt)
        self.msg(4, "im_opt", self.im_opt)
        # remove stdout from im_out, it contains graphic output, not text
        self.im_out = [x for x in self.im_out if x not in ['stdout']]
        args = self.im_opt
        if self.cmd(self.im_prg, stdin=self.code, *args):
            if self.stdout:
                self.write('wb', self.stdout, self.outfile)
            return self.result()


class Gle(Handler):
    '''
    sudo apt-get install gle-graphics
    http://glx.sourceforge.net
    '''
    cmdmap = {'gle': 'gle'}

    def image(self):
        'gle {im_opt} -verbosity 0 -output <fname>.{im_fmt} <fname>.gle'
        args = self.im_opt
        args += ['-verbosity', '0', '-output', self.outfile, self.inpfile]
        # gle leaves im_dir-images/.gle lying around ...
        if self.cmd(self.im_prg, *args):
            return self.result()


class GnuPlot(Handler):
    '''
    sudo apt-get install gnuplot
    http://www.gnuplot.info
    notes:
    - graphic data is printed to stdout
    - so 'stdout' in im_out option is silently ignored
    '''
    cmdmap = {'gnuplot': 'gnuplot'}

    def image(self):
        'gnuplot {im_opt} <fname>.gnuplot > <fname>.{im_fmt}'
        # stdout captures the graphic image
        self.im_out = [x for x in self.im_out if x not in ['stdout']]
        args = self.im_opt + [self.inpfile]
        if self.cmd(self.im_prg, *args):
            if self.stdout:
                self.write('wb', self.stdout, self.outfile)
            return self.result()


class Graph(Handler):
    '''
    sudo apt-get install plotutils
    https://www.gnu.org/software/plotutils
    notes:
    - graphic data is printed to stdout
    - so 'stdout' in im_out option is silently ignored
    '''
    cmdmap = {'graph': 'graph'}

    def image(self):
        'graph -T png {im_opt} <fname>.graph'
        # stdout is used to capture graphic image data
        self.im_out = [x for x in self.im_out if x not in ['stdout']]
        args = ['-T', self.im_fmt] + self.im_opt + [self.inpfile]
        if self.cmd(self.im_prg, *args):
            self.write('wb', self.stdout, self.outfile)
            return self.result()


class Graphviz(Handler):
    '''
    sudo apt-get install graphviz
    http://graphviz.org
    '''
    progs = ['dot', 'neato', 'twopi', 'circo', 'fdp', 'sfdp']
    cmdmap = dict(zip(progs, progs))
    cmdmap['graphviz'] = 'dot'
    im_fmt = 'svg'  # override Handler's png default

    def image(self):
        '{im_prg} {im_opt} -T{im_fmt} <fname>.{im_prg} <fname>.{im_fmt}'
        args = self.im_opt + ['-T%s' % self.im_fmt, self.inpfile, 
                '-o', self.outfile]

        if self.cmd(self.im_prg, *args):
            return self.result()


class Gri(Handler):
    '''
    sudo apt-get install gri imagemagick
    http://gri.sourceforge.net
    Notes
    - insists on creating a <fname>.ps in current working directory
    - requires `convert` from imagemagick
    - ImageMagick's security policy might need massaging
    '''
    # cannot convince gri to output intermediate ps in pd-images/..
    # so we move it there.
    # Repair ImageMagick's ability to manipulate ps files:
    # nvim /etc/ImageMagick-6/policy.xml
    #  <policy domain="coder" rights="read|write" pattern="PS" />
    #  <policy domain="coder" rights="read|write" pattern="PS2" />
    #  <policy domain="coder" rights="read|write" pattern="PS3" />
    #  <policy domain="coder" rights="read|write" pattern="EPS" />
    #  <policy domain="coder" rights="read|write" pattern="PDF" />
    #  <policy domain="coder" rights="read|write" pattern="XPS" />

    cmdmap = {'gri': 'gri'}

    def image(self):
        'gri {im_opt} -c 0 -b <fname>.gri'
        # -> <x>.ps -> <x>.{im_fmt} -> Para(Img(<x>.{im_fmt}))'
        args = self.im_opt + ['-c', '0', '-b', self.inpfile]
        if self.cmd(self.im_prg, *args):
            # gri insists on producing a .ps in current working dir
            dstfile = self.inpfile.replace('.gri', '.ps')
            srcfile = os.path.split(dstfile)[-1]   # the temp ps in working dir
            if os.path.isfile(srcfile):
                self.msg(3, 'moving', srcfile, dstfile)
                os.rename(srcfile, dstfile)
            if self.cmd('convert', dstfile, self.outfile):
                return self.result()
            else:
                self.msg(2, "could not convert gri's ps to", self.im_fmt)
        else:
            # relay gri's complaints on stdout to stderr.
            for line in self.stdout.splitlines():
                self.msg(1, '>>:', line)


class Imagine(Handler):
    '''
    pip install pandoc-imagine
    https://github.com/hertogp/imagine
    '''
    cmdmap = {'imagine': 'imagine'}

    def image(self):
        'returns documentation in a CodeBlock'
        # CodeBlock value = [(Identity, [classes], [(key, val)]), code]
        if not self.code:
            return pf.CodeBlock(('', [], []), __doc__)
        elif self.code == 'classes':
            classes = wrap(', '.join(sorted(Handler.workers.keys())), 78)
            return pf.CodeBlock(('', [], []), '\n'.join(classes))

        doc = []
        for name in self.code.splitlines():
            name = name.lower()
            worker = self.workers.get(name, None)
            doc.append("Codeblock class: " + name)
            if worker is None:
                doc.append('No worker found for %s' % name)
                continue
            if worker.__doc__:
                doc.append(worker.__doc__)
                doc.append("    runs:")
                doc.append('    > ' + worker.image.__doc__)
            else:
                doc.append('No help available.')

            doc.append("\n    class->cmd")
            for k,v in worker.cmdmap.items():
                doc.append("      {} -> {}".format(k,v))

            # -- document class metadata options
            klass_opts, glob_opts = [], []
            for k,v in self.md_opts.items():
                if k not in self.workers:
                    glob_opts.append("    imagine.{}: {}".format(k,v))
                else: # elif k == name:
                    for kk,vv in self.md_opts.get(name, {}).items():
                        klass_opts.append("    imagine.{}.{}: {}".format(k,
                            kk,vv))
            if klass_opts or glob_opts:
                doc.append("\nMetadata options")
                # doc.append("    ---")
                doc.extend(glob_opts + klass_opts)
                # doc.append("    ...")

            doc.append('\n')

        return pf.CodeBlock(('', [], []), '\n'.join(doc))


class Mermaid(Handler):
    '''
    sudo npm install mermaid.cli
    https://github.com/mermaidjs/mermaid.cli
    '''
    cmdmap = {'mermaid': 'mmdc'}

    def image(self):
        'mmdc -i <fname>.mermaid -o <fname>.<fmt> {im_opt}'
        args = ['-i', self.inpfile, '-o', self.outfile] + self.im_opt
        if self.cmd(self.im_prg, *args):
            return self.result()


class MscGen(Handler):
    '''
    sudo apt-get install mscgen
    http://www.mcternan.me.uk/mscgen
    '''
    cmdmap = {'mscgen': 'mscgen'}

    def image(self):
        'mscgen -T {im_fmt} -o <fname>.{im_fmt} <fname>.mscgen'
        args = self.im_opt
        args += ['-T', self.im_fmt, '-o', self.outfile, self.inpfile]
        if self.cmd(self.im_prg, *args):
            return self.result()


class Octave(Handler):
    '''
    sudo apt-get install octave
    https://www.gnu.org/software/octave
    '''
    cmdmap = {'octave': 'octave'}

    def image(self):
        'octage --no-gui -q {im_opt} <fname>.octave <fname>.{im_fmt}'
        args = ['--no-gui', '-q'] + self.im_opt + [self.inpfile, self.outfile]
        if self.cmd(self.im_prg, *args):
            return self.result()


class Pic2Plot(Handler):
    '''
    sudo apt-get install plotutils
    https://www.gnu.org/software/plotutils
    notes:
    - graphic data is printed to stdout
    - so 'stdout' in im_out option is silently ignored
    '''
    cmdmap = {'pic2plot': 'pic2plot', 'pic': 'pic2plot'}

    def image(self):
        'pic2plot -T png {im_opt} <fname>.pic2plot'
        args = ['-T', self.im_fmt] + self.im_opt + [self.inpfile]
        if self.cmd(self.im_prg, *args):
            self.write('wb', self.stdout, self.outfile)
            return self.result()


class PlantUml(Handler):
    '''
    sudo apt-get install plantuml
    http://plantuml.com
    '''
    cmdmap = {'plantuml': 'plantuml'}

    def image(self):
        'plantuml -t{im_fmt} <fname>.plantuml {im_opt}'
        args = ['-t' + self.im_fmt, self.inpfile] + self.im_opt
        if self.cmd(self.im_prg, *args):
            return self.result()


class Plot(Handler):
    '''
    sudo apt-get install plotutils
    https://www.gnu.org/software/plotutils
    notes:
    - graphic data is printed to stdout
    - so 'stdout' in im_out option is silently ignored
    '''
    # - code text is filename relative to source.md
    # - write(stdout, <fname>.<fmt>)
    cmdmap = {'plot': 'plot'}

    def image(self):
        'plot -T {im_fmt} {im_opt} <code-text-as-filename>'
        if not os.path.isfile(self.code):
            self.msg(0, 'fail: cannot read file %r' % self.code)
            return
        args = ['-T', self.im_fmt] + self.im_opt + [self.code]
        if self.cmd(self.im_prg, *args):
            self.write('wb', self.stdout, self.outfile)
            return self.result()


class Ploticus(Handler):
    '''
    sudo apt-get install ploticus
    http://ploticus.sourceforge.net/doc/welcome.html
    '''
    cmdmap = {'ploticus': 'ploticus'}

    def image(self):
        'ploticus -{im_fmt} -o <fname>.{im_fmt} {im_opt} <fname>.ploticus'
        args = ['-'+self.im_fmt, '-o', self.outfile] + self.im_opt
        args += [self.inpfile]
        if self.cmd(self.im_prg, *args):
            return self.result()


class Protocol(Handler):
    '''
    cd ~/installs/git-repos
    git clone https://github.com/luismartingarcia/protocol.git
    python setup install
    https://github.com/luismartingarcia/protocol.git
    '''
    cmdmap = {'protocol': 'protocol'}
    im_fmt = 'protocold'
    output = 'stdout'  # i.e. default to stdout

    def image(self):
        'protocol {im_opt} code-text'
        args = self.im_opt + [self.code]
        # silently ignore any request for an 'image'
        self.im_out = [x for x in self.im_out if x not in ['img']]
        if self.cmd(self.im_prg, *args):
            if self.stdout:
                self.write('w', to_str(self.stdout), self.outfile)
            else:
                self.stdout = self.read('r', self.outfile)
            return self.result()


class PyxPlot(Handler):
    '''
    sudo apt-get install pyxplot
    http://pyxplot.org.uk
    '''
    cmdmap = {'pyxplot': 'pyxplot'}

    def image(self):
        'pyxplot {im_opt} <fname>.pyxplot'
        args = self.im_opt + [self.inpfile]
        self.code = '%s\n%s\n%s' % ('set terminal %s' % self.im_fmt,
                                    'set output %s' % self.outfile,
                                    self.code)
        self.write('w', self.code, self.inpfile)
        if self.cmd(self.im_prg, *args):
            return self.result()


class SheBang(Handler):
    '''
    http://www.google.com/search?q=shebang+line
    '''
    # runs fenced code block as a hash-bang system script'
    cmdmap = {'shebang': 'shebang'}

    def image(self):
        '<fname>.shebang {im_opt} <fname>.{im_fmt}'
        os.chmod(self.inpfile, stat.S_IEXEC | os.stat(self.inpfile).st_mode)
        args = self.im_opt + [self.outfile]
        if self.cmd(self.inpfile, *args):
            return self.result()

# use sys.modules[__name__].__doc__ instead of __doc__ directly
# to avoid pylint'rs complaints.
sys.modules[__name__].__doc__ %= \
    {'cmds': '\n    '.join(wrap(', '.join(sorted(Handler.workers.keys()))))}

# for PyPI
def main():
    'main entry point'
    def walker(key, value, fmt, meta):
        'walk down the pandoc AST and invoke workers for CodeBlocks'

        if key == 'CodeBlock':
            return dispatch(value, fmt, meta).image()

    dispatch = Handler(None, None, None)
    pf.toJSONFilter(walker)

if __name__ == '__main__':
    main()
