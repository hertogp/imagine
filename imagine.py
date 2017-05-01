#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-- Candidates:
# o grace (ie gracebat, the batchmode variant; indirect mode?)
#   script files are pretty big.  Perhaps indirectly.  It supports a batch mode
#   via `gracebat`, which symlinks to the real binary executable.
#
# o tizk, needs convert since eps wont go into pdflatex ..

# Notes
# - fix result() so output can be run through --filter imagine again
#   + no imagine classes (dot, imagine, stdout, fcb, etc..
#   + use __stdout__, __fcb__ and/or __img__ only ...?

#-- __doc__

'''\
Imagine
  A pandoc filter to turn fenced codeblocks into graphics or ascii art by
  wrapping some external command line utilities, such as:

    %(cmds)s


Installation

  1. %% sudo pip install pandocfilters
  2. %% sudo pip install pandoc-imagine

     or save `imagine.py` anywhere along $PATH (pandoc's filter search path).


Dependencies

  One (or more) of the packages that provide above utilities.


Pandoc usage

    %% pandoc --filter imagine.py document.md -o document.pdf


Markdown usage

    ```cmd
    code
    ```

  which will run `cmd` to proces the `code` into a png image and replaces the
  fenced code block with an Image in a paragraph of its own or any ascii art in
  its own CodeBlock.

  Alternate, longer form:

    ```{.cmd options=".." imgout=".." prog=<other-cmd>}
    code
    ```

  - options="..." will be passed onto the command line.
    Some classes already provide sane defaults (if required by the command).

  - imgout="...", csv-list of keywords each specifying a certain output
    - img     image in a paragraph
    - fcb     codeblock (class __fcb__) containing the original codeblock
    - stdout, codeblock (class __stdout__) containing stdout output (if any)
    - stderr, codeblock (class __stderr__) containing stderr output (if any)

  - prog=<other-cmd>, overrides class-to-command map.
    Only useful if `cmd` itself is not an appropiate class in your document.

  If the command fails and/or produces no image, the original fenced code block
  is retained unchanged.  Any info on stderr is relayed by Imagine, which might
  be useful for troubleshooting.

  If the command succeeds but produces no image, a line reporting the missing
  Image is included in the output document as output.

  Notes:
  - filenames are based on a hash of the codeblock + its attributes
  - uses subdir `pd-images` to store any input/output files
  - there's no clean up of files stored there
  - if an output filename exists, it is not regenerated but simply linked to.
  - `packetdiag` & `sfdp`s underlying libraries seem to have some problems.
  - when creating a pdf, images are placed `nearest` to their fenced code block

  Some commands follow a slightly different pattern:
  - 'img' directive is ignored by commands that only produce ascii
  - ctioga2 defaults to pdf instead of png
  - flydraw produces a gif, not png
  - gle also creates a pd-images/.gle subdir
  - gri produces a ps, which is `convert`ed to png
  - imagine reads its codeblock as help-topics for which a codeblock is returned
  - plot reads its codeblock as the relative path to the file to process
  - pyxplot will have `set terminal` & `set output` prepended to its `code`
  - shebang runs its codeblock as a script with <fname>.png as its argument.
    - use {.shebang imgout="stdout"} for text instead of an png


Security

  Imagine just hands the fenced codeblocks to plotting tools to process or
  simply runs them as system scripts as-is.

  Most of the plotting tools, implement their own 'little' language which can
  create beautiful images but can also cause harm.

  There is no way to check for 'side effects' in advance, so make sure to check
  the fenced codeblocks before running them through the filter.


Imagine class

The imagine class puts documentation of topics at your fingertips, like so:

    ```imagine
    class
    ```

  to quickly get some information on a particular class of interest. Use
  `imagine` to get the module's docstring.
'''

__version__ = '1.0'

import os
import sys
import stat
from textwrap import wrap
from subprocess import Popen, check_output, CalledProcessError, STDOUT, PIPE

import pandocfilters as pf

#-- globs
IMG_BASEDIR = 'pd'
IMG_OUTPUTS = ['fcb', 'img', 'stdout', 'stderr']

# Notes:
# - if walker does not return anything, the element is kept
# - if walker returns a block element, it'll replace current element
# - block element = {'c': <value>, 't': <block_type>}

class HandlerMeta(type):
    def __init__(cls, name, bases, dct):
        'register worker classes by cmdmap handled'
        for klass in dct.get('cmdmap', {}):
            cls.workers[klass.lower()] = cls

class Handler(object):
    'baseclass for image/ascii art generators'
    severity  = 'error warn note info debug'.split()
    workers = {}    # dispatch mapping for Handler
    klass = None    # assigned when worker is dispatched
    _output = IMG_OUTPUTS[1]  # i.e. default img
    __metaclass__ = HandlerMeta

    cmdmap = {}     # worker subclass must override, klass -> cli-program
    level = 2       # log severity level, see above
    outfmt = 'png'  # default output format for a worker

    def __call__(self, codec):
        'Return worker class or self (Handler keeps CodeBlock unaltered)'
        # A worker class with cmdmap={'': cmd} replaces Handler as default
        # CodeBlock's value = [(Identity, [classes], [(key, val)]), code]
        self.msg(4, 'Handler __call__ codec', codec[0])
        try:
            _, klasses, keyvals = codec[0]
        except Exception as e:
            self.msg(0, 'Invalid codec passed in', codec)
            raise e

        # try dispatching by class attribute first
        for klass in klasses:
            worker = self.workers.get(klass.lower(), None)
            if worker is not None:
                worker.klass = klass.lower()
                self.msg(4, codec[0], 'dispatched by class to', worker)
                return worker(codec)

        # try dispatching via 'cmd' named by prog=cmd key-value
        if len(keyvals) == 0:  # pf.get_value barks if keyvals == []
            self.msg(4, codec[0], 'dispatched by default', self)
            return self

        prog, _ = pf.get_value(keyvals, 'prog', '')
        worker = self.workers.get(prog.lower(), None)
        if worker is not None:
            self.msg(4, codec[0], 'dispatched by prog to', worker)
            return worker(codec)

        self.msg(4, codec[0], 'dispatched by default to', self)
        return self

    def __init__(self, codec):
        'init by decoding the CodeBlock-s value'
        # codeblock attributes: {#Identity .class1 .class2 k1=val1 k2=val2}
        self.codec = codec
        self._name = self.__class__.__name__  # the default inpfile extension
        self.output = '' # catches stdout by self.cmd, if any
        self.stderr = '' # catches stderr by self.cmd, if any

        if codec is None: return  # initial dispatch creation

        (self.id_, self.classes, self.keyvals), self.code = codec
        self.caption, self.typef, self.keyvals = pf.get_caption(self.keyvals)

        # `Extract` Imagine keywords/keyvals from codeblock's attributes
        # - also remove any and all Imagine classes
        self.classes = [k for k in self.classes if k not in self.workers]
        self.options, self.keyvals = pf.get_value(self.keyvals, u'options', '')
        self.options = self.options.split()
        self.prog, self.keyvals = pf.get_value(self.keyvals, u'prog', None)
        imgout, self.keyvals = pf.get_value(self.keyvals,
                                            u'imgout',
                                            self._output)
        self.imgout = imgout.lower().replace(',',' ').split()

        # prog=cmd key-value trumps .cmd class attribute
        self.prog = self.prog if self.prog else self.cmdmap.get(self.klass, None)
        if self.prog is None:
            self.msg(0, self.klass, 'not listed in', self.cmdmap)
            raise Exception('worker has no cli command for %s' % self.klass)

        self.basename = pf.get_filename4code(IMG_BASEDIR, str(codec))
        self.outfile = self.basename + '.%s' % self.outfmt
        self.inpfile = self.basename + '.%s' % self._name.lower()

        self.codetxt = self.code.encode(sys.getfilesystemencoding())
        if not os.path.isfile(self.inpfile):
            self.write('w', self.codetxt, self.inpfile)

    def disallow(self, src, disallow=[]):
        'whilst preserving order, limit list of src elements to those allowed'
        # helper for managing imgout lists
        rv = []
        for elm in src:
            if elm in rv or elm in disallow: continue # no duplicates
            rv.append(elm)
        return rv

    def read(self, src):
        try:
            with open(src, 'r') as f:
                return f.read()
        except Exception as e:
            self.msg(0, 'fail: could not read %s' % src)
            return ''
        return ''


    def write(self, mode, dta, dst):
        if len(dta) == 0:
            self.msg(3, 'skipped writing 0 bytes to', dst)
            return False
        try:
            with open(dst, mode) as f:
                f.write(dta)
            self.msg(3, 'wrote', len(dta), 'bytes to', dst)
        except Exception as e:
            self.msg(0, 'fail: could not write', len(dta), 'bytes to', dst)
            self.msg(0, '>>: exception', e)
            return False
        return True

    def msg(self, level, *a):
        if level > self.level: return
        level %= len(self.severity)
        msg = '%s[%9s:%-5s] %s' % ('Imagine',
                                self._name,
                                self.severity[level],
                                ' '.join(str(s) for s in a))
        print >> sys.stderr, msg
        sys.stderr.flush()

    def fmt(self, fmt, **specials):
        '(re)set image file extension based on output document format'
        self.outfmt = pf.get_extension(fmt, self.outfmt, **specials)
        self.outfile = self.basename + '.%s' % self.outfmt

    def Url(self):
        'return an Image link for existing/new output image-file'
        # Since pf.Image is an Inline element, its usually wrapped in a pf.Para
        return pf.Image([self.id_, self.classes, self.keyvals],
                        self.caption, [self.outfile, self.typef])


    def AnonCodeBlock(self):
        'reproduce the original CodeBlock inside an anonymous CodeBlock'
        (id_, klasses, keyvals), code = self.codec
        id_ = '#' + id_ if id_ else id_
        klasses = ' '.join('.%s' % c for c in klasses)
        keyvals = ' '.join('%s="%s"' % (k,v) for k,v in keyvals)
        attr = '{%s}' % ' '.join(a for a in [id_, klasses, keyvals] if a)
        # prefer ```cmd over ```{.cmd}
        attr = attr if attr.find(' ')>-1 else attr[2:-1]
        return pf.CodeBlock(['',[],[]], '```%s\n%s\n```'% (attr, self.code))

    def result(self):
        'return FCB, Para(Url()) and/or CodeBlock(stdout) as ordered'
        rv = []
        for output_elm in self.imgout:
            if output_elm == 'img':
                if os.path.isfile(self.outfile):
                    rv.append(pf.Para([self.Url()]))
                else:
                    msg = '?? missing %s' % self.outfile
                    self.msg(1, '>>:', msg)
                    rv.append(pf.Para([pf.Str(msg)]))

            elif output_elm == 'fcb':
                rv.append(self.AnonCodeBlock())

            elif output_elm == 'stdout':
                if len(self.output):
                    attr = ['', self.classes + ['stdout'], self.keyvals]
                    rv.append(pf.CodeBlock(attr, self.output))
                else:
                    self.msg(1, '>>:', 'stdout requested, but saw nothing')

            elif output_elm == 'stderr':
                if len(self.stderr):
                    attr = ['', self.classes + ['stderr'], self.keyvals]
                    rv.append(pf.CodeBlock(attr, self.stderr))
                else:
                    self.msg(1, '>>:', 'stderr requested, but saw nothing')

        if len(rv) == 0: return None  # no results -> None keeps original FCB
        if len(rv) > 1: return rv     # multiple results
        return rv[0]                  # just 1 block level element

    def cmd(self, *args, **kwargs):
        'run, possibly forced, a cmd and return success indicator'
        forced = kwargs.get('forced', False) # no need to pop
        stdin = kwargs.get('stdin', None)

        if os.path.isfile(self.outfile) and forced is False:
            self.msg(3, 'exists:', *args)
            return True

        try:
            pipes = {'stdin': None if stdin is None else PIPE,
                     'stdout': PIPE,
                     'stderr': PIPE}
            p = Popen(args, **pipes)
            self.output, self.stderr = p.communicate(stdin)

            # print any complaints on stderr
            if len(self.stderr):
                self.msg(1, 'ok?', *args)
                for line in self.stderr.splitlines():
                    self.msg(1, '>>:', line)
            else:
                self.msg(2, 'ok:', *args)

            return p.returncode == 0

        except (OSError, CalledProcessError) as e:
            try: os.remove(self.outfile)
            except: pass
            self.msg(1, 'fail:', *args)
            self.msg(0, '>>:', self.prog , str(e))
            return False

    def image(self, fmt=None):
        'return an Image url or None to keep CodeBlock'
        # workers must override this method
        self.msg(4, self._name, 'keeping CodeBlock as-is (default)')
        return None


class Asy(Handler):
    '''
    See http://asymptote.sourceforge.net
    '''
    cmdmap = {'asy': 'asy', 'asymptote': 'asy'}
    outfmt = 'png'

    def image(self, fmt=None):
        'asy -o <fname>.png [options] <fname>.asy'
        self.fmt(fmt)
        args = ['-o', self.outfile] + self.options + [self.inpfile]
        if self.cmd(self.prog, *args):
            return self.result()


class Boxes(Handler):
    '''
    See http://boxes.thomasjensen.com
    '''
    cmdmap = {'boxes': 'boxes'}
    outfmt = 'boxed'
    _output = IMG_OUTPUTS[2]  # i.e. default to stdout

    def image(self, fmt=None):
        'boxes [options] <fname>.boxes'
        # silently ignore 'img', default to stdout if needed
        self.imgout = self.disallow(self.imgout, ['img'])
        args = self.options + [self.inpfile]
        if self.cmd(self.prog, *args):
            if len(self.output):
                self.write('w', self.output, self.outfile)
            else:
                self.output = self.read(self.outfile)
            return self.result()
            return self.CodeBlock(self.codec[0], self.output)


class BlockDiag(Handler):
    '''
    See http://blockdiag.com
    '''
    progs = 'blockdiag seqdiag rackdiag nwdiag packetdiag actdiag'.split()
    cmdmap = dict(zip(progs,progs))

    def image(self, fmt=None):
        'cmd -T png <fname>.txt -o <fname>.png'
        args = ['-T', self.outfmt, self.inpfile, '-o', self.outfile]
        if self.cmd(self.prog, *args):
            return self.result()


class Ctioga2(Handler):
    '''
    See http://ctioga2.sourceforge.net
    '''
    cmdmap = {'ctioga2': 'ctioga2'}
    outfmt = 'pdf'

    def image(self, fmt=None):
        'ctioga2 [options] -f <fname>.ctioga2'
        self.fmt(fmt)
        args = self.options + ['-f', self.inpfile]
        if self.cmd(self.prog, *args):
            return self.result()


class Ditaa(Handler):
    'See http://ditaa.sourceforge.net'
    cmdmap = {'ditaa': 'ditaa'}

    def image(self, fmt=None):
        'ditaa <fname>.ditaa <fname>.png -T [options]'
        args = [self.inpfile, self.outfile, '-T'] + self.options
        if self.cmd(self.prog, *args):
            return self.result()


class Figlet(Handler):
    '''
    See http://www.figlet.org
    '''
    # - saves code-text to <fname>.figlet
    # - saves stdout to <fname>.figled
    cmdmap = {'figlet': 'figlet'}
    outfmt = 'figled'
    _output = IMG_OUTPUTS[2]  # i.e. default to stdout

    def image(self, fmt=None):
        'figlet [options] < code-text'
        # silently ignore any request for an 'image'
        self.imgout = self.disallow(self.imgout, ['img'])
        args = self.options
        if self.cmd(self.prog, stdin=self.codetxt, *args):
            if len(self.output):
                # save figlet's stdout to outfile for next time around
                self.write('w', self.output, self.outfile)
            else:
                self.output = self.read(self.outfile)
            return self.result()


class Flydraw(Handler):
    '''
    See http://manpages.ubuntu.com/manpages/precise/man1/flydraw.1.html
    '''
    # - flydraw reads its commands from stdin & produces output on stdout
    # - seems to insist on producing GIF files, despite claims in the manual
    cmdmap = {'flydraw': 'flydraw'}
    outfmt = 'gif'

    def image(self, fmt=None):
        'flydraw [options] < code-text'
        # ignore any request for img
        self.imgout = self.disallow(self.imgout, ['img'])
        args = self.options
        if self.cmd(self.prog, stdin=self.codetxt, *args):
            if len(self.output):
                self.write('w', self.output, self.outfile)
            return self.result()


class Gle(Handler):
    '''
    See http://glx.sourceforge.net
    '''
    cmdmap = {'gle': 'gle'}

    def image(self, fmt=None):
        'gle -verbosity 0 -output <fname>.<fmt> <fname>.gle'
        args = self.options
        args += ['-verbosity', '0', '-output', self.outfile, self.inpfile]
        # gle leaves IMG_BASEDIR-images/.gle lying around ...
        if self.cmd(self.prog, *args):
            return self.result()


class GnuPlot(Handler):
    '''
    See http://www.gnuplot.info
    '''
    cmdmap = {'gnuplot': 'gnuplot'}

    def image(self, fmt=None):
        'gnuplot [options] <fname>.gnuplot > <fname>.png'
        self.fmt(fmt)
        # stdout captures the graphic image
        self.imgout = self.disallow(self.imgout, ['stdout'])
        args = self.options + [self.inpfile]
        if self.cmd(self.prog, *args):
            if len(self.output):
                self.write('wb', self.output, self.outfile)
            return self.result()


class Graph(Handler):
    '''
    See https://www.gnu.org/software/plotutils
    '''
    cmdmap = {'graph': 'graph'}

    def image(self, fmt=None):
        'graph -T png [options] <fname>.graph'
        # stdout is used to capture graphic image data
        self.imgout = self.disallow(self.imgout, ['stdout'])
        args = ['-T', self.outfmt] + self.options + [self.inpfile]
        if self.cmd(self.prog, *args):
            self.write('wb', self.output, self.outfile)
            return self.result()


class Graphviz(Handler):
    '''
    See http://graphviz.org
    '''
    progs = ['dot', 'neato', 'twopi', 'circo', 'fdp', 'sfdp']
    cmdmap = dict(zip(progs,progs))
    cmdmap['graphviz'] = 'dot'

    def image(self, fmt=None):
        'cmd [options] -T<fmt> <fname>.dot <fname>.<fmt>'
        self.fmt(fmt)
        args = self.options
        args += ['-T%s' % self.outfmt, self.inpfile, '-o', self.outfile]
        if self.cmd(self.prog, *args):
            return self.result()


class Gri(Handler):
    '''
    See http://gri.sourceforge.net
    - requires `convert` from imagemagick
    '''
    # cannot convince gri to output intermediate ps in pd-images/..
    # so we move it there.
    cmdmap = {'gri': 'gri'}

    def image(self, fmt=None):
        'gri -c 0 -b <fname>.gri'
        # -> <x>.ps -> <x>.png -> Para(Img(<x>.png))'
        args = self.options + ['-c', '0', '-b', self.inpfile]
        if self.cmd(self.prog, *args):
            # gri insists on producing a .ps in current working dir
            dstfile = self.inpfile.replace('.gri','.ps')
            srcfile = os.path.split(dstfile)[-1]   # the temp ps in working dir
            if os.path.isfile(srcfile):
                self.msg(3, 'moving', srcfile, dstfile)
                os.rename(srcfile, dstfile)
            if self.cmd('convert', dstfile, self.outfile):
                return self.result()
            else:
                self.msg(2, "could not convert gri's ps to", self.outfmt)
        else:
            # relay gri's complaints on stdout to stderr.
            for line in self.output.splitlines():
                self.msg(1, '>>:', line)


class Imagine(Handler):
    '''
    See https://github.com/hertogp/imagine
    '''
    cmdmap = {'imagine': 'imagine'}

    def image(self, fmt=None):
        'return documentation in a CodeBlock'
        # CodeBlock value = [(Identity, [classes], [(key, val)]), code]
        if len(self.codetxt) == 0:
            return pf.CodeBlock(('',['__doc__'],[]), __doc__)
        elif self.codetxt == 'classes':
            classes = wrap(', '.join(sorted(Handler.workers.keys())), 78)
            return pf.CodeBlock(('',['__doc__'],[]), '\n'.join(classes))

        doc = []
        for name in self.codetxt.splitlines():
            worker = self.workers.get(name, None)
            doc.append(name)
            if worker is None:
                doc.append('No worker found for %s' % name)
                continue
            if worker.__doc__:
                doc.append(worker.__doc__)
                doc.append('    ' + worker.image.__doc__)
            else:
                doc.append('No help available.')
            doc.append('\n')

        return pf.CodeBlock(('', ['__doc__'], []), '\n'.join(doc))


class Mermaid(Handler):
    '''
    See https://knsv.github.io/mermaid (needs phantomjs)
    - requires phantomjs.
    '''
    cmdmap = {'mermaid': 'mermaid'}

    def image(self, fmt=None):
        'mermaid -o <basedir> [options] <fname>.mermaid'
        args = ['-o', IMG_BASEDIR+'-images'] + self.options + [self.inpfile]
        if self.cmd(self.prog, *args):
            # latex seems to choke on <fname>.mermaid.png
            tmpfile = self.inpfile + '.' + self.outfmt
            if os.path.isfile(tmpfile):
                os.rename(self.inpfile+'.'+self.outfmt, self.outfile)
            return self.result()

class MscGen(Handler):
    '''
    See http://www.mcternan.me.uk/mscgen
    '''
    cmdmap = {'mscgen': 'mscgen'}

    def image(self, fmt=None):
        'mscgen -T png -o <fname>.png <fname>.mscgen'
        args = self.options
        args += ['-T', self.outfmt, '-o', self.outfile, self.inpfile]
        if self.cmd(self.prog, *args):
            return self.result()


class Octave(Handler):
    '''
    See https://www.gnu.org/software/octave
    '''
    cmdmap = {'octave': 'octave'}

    def image(self, fmt=None):
        'octage --no-gui -q [options] <fname>.octave <fname>.png'
        args = ['--no-gui', '-q'] + self.options + [self.inpfile, self.outfile]
        if self.cmd(self.prog, *args):
            return self.result()


class Pic2Plot(Handler):
    '''
    See https://www.gnu.org/software/plotutils
    '''
    cmdmap = {'pic2plot': 'pic2plot', 'pic': 'pic2plot'}

    def image(self, fmt=None):
        'pic2plot -T png [options] <fname>.pic2plot'
        self.fmt(fmt)
        args = ['-T', self.outfmt] + self.options + [self.inpfile]
        if self.cmd(self.prog, *args):
            self.write('wb', self.output, self.outfile)
            return self.result()


class PlantUml(Handler):
    '''
    See http://plantuml.com
    '''
    cmdmap = {'plantuml': 'plantuml'}

    def image(self, fmt=None):
        'plantuml -t png <fname>.plantuml'
        args = ['-t' + self.outfmt, self.inpfile]
        if self.cmd(self.prog, *args):
            return self.result()


class Plot(Handler):
    '''
    See https://www.gnu.org/software/plotutils
    '''
    # - code text is filename relative to source.md
    # - write(stdout, <fname>.<fmt>)
    cmdmap = {'plot': 'plot'}

    def image(self, fmt=None):
        'plot -T png [options] <code-text-as-filename>'
        self.fmt(fmt)
        if not os.path.isfile(self.codetxt):
            self.msg(0, 'fail: cannot read file %r' % self.codetxt)
            return
        args = ['-T', self.outfmt] + self.options + [self.codetxt]
        if self.cmd(self.prog, *args):
            self.write('wb', self.output, self.outfile)
            return self.result()


class Ploticus(Handler):
    '''
    See http://ploticus.sourceforge.net/doc/welcome.html
    '''
    cmdmap = {'ploticus': 'ploticus'}

    def image(self, fmt=None):
        'ploticus -png -o <fname>.png [options] <fname>.ploticus'
        args = ['-'+self.outfmt, '-o', self.outfile] + self.options
        args += [self.inpfile]
        if self.cmd(self.prog, *args):
            return self.result()


class Protocol(Handler):
    '''
    See https://github.com/luismartingarcia/protocol.git
    '''
    cmdmap = {'protocol': 'protocol'}
    outfmt = 'protocold'
    _output = IMG_OUTPUTS[2]  # i.e. default to stdout

    def image(self, fmt=None):
        'protocol [options] code-text'
        args = self.options + [self.codetxt]
        # silently ignore any request for an 'image'
        self.imgout = self.disallow(self.imgout, ['img'])
        if self.cmd(self.prog, *args):
            if len(self.output):
                self.write('w', self.output, self.outfile)
            else:
                self.output = self.read(self.outfile)
            return self.result()


class PyxPlot(Handler):
    '''
    See http://pyxplot.org.uk
    '''
    # need to set output format and output filename in the script...
    # .. write('set terminal <fmt>\n' +
    #          'set output <fname>.<fmt>\n' +
    #           code,
    #          <fname>.pyxplot)
    # <= Para(Image)
    cmdmap = {'pyxplot': 'pyxplot'}

    def image(self, fmt=None):
        'pyxplot [options] <fname>.pyxplot'
        self.fmt(fmt)
        args = self.options + [self.inpfile]
        self.codetxt = '%s\n%s\n%s' % ('set terminal %s' % self.outfmt,
                                       'set output %s' % self.outfile,
                                       self.codetxt)
        self.write('w', self.codetxt, self.inpfile)
        if self.cmd(self.prog, *args):
            return self.result()


class SheBang(Handler):
    '''
    See http://www.google.com/search?q=shebang+line
    '''
    # runs fenced code block as a hash-bang system script'
    cmdmap = {'shebang': 'shebang'}

    def image(self, fmt=None):
        '<fname>.shebang [options] <fname>.png'
        os.chmod(self.inpfile, stat.S_IEXEC | os.stat(self.inpfile).st_mode)
        args = self.options + [self.outfile]
        if self.cmd(self.inpfile, *args):
            return self.result()


__doc__ = __doc__ % {'cmds':'\n    '.join(wrap(', '.join(sorted(Handler.workers.keys()))))}


def walker(key, value, fmt, meta):
    if key == u'CodeBlock':
        worker = dispatch(value)
        return worker.image(fmt)


if __name__ == '__main__':
    dispatch = Handler(None)
    pf.toJSONFilter(walker)

