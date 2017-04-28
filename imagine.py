#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-- Candidates:
# o grace (ie gracebat, the batchmode variant; indirect mode?)
#   script files are pretty big.  Perhaps indirectly.  It supports a batch mode
#   via `gracebat`, which symlinks to the real binary executable.
#
# o tizk, needs convert since eps wont go into pdflatex ..

#-- __doc__

'''Imagine
  A pandoc filter that turns fenced codeblocks into graphics or ascii art by
  wrapping some external command line utilities, such as:

    %(cmds)s

Installation

  1. Put `imagine.py` anywhere along $PATH (pandoc's search path for filters).
  2. %% sudo pip install (mandatory):
       - pandocfilters
  3. %% sudo apt-get install (1 or more of):

       - asymptote,     http://asymptote.sourceforge.net
       - boxes,         http://boxes.thomasjensen.com
       - ctioga2,       http://ctioga2.sourceforge.net
       - ditaa,         http://ditaa.sourceforge.net
       - figlet,        http://www.figlet.org
       - flydraw,       http://manpages.ubuntu.com/manpages/precise/man1/flydraw.1.html
       - gle-graphics,  http://glx.sourceforge.net
       - gnuplot,       http://www.gnuplot.info
       - graphviz,      http://graphviz.org
       - gri,           http://gri.sourceforge.net
       - imagemagick,   http://www.imagemagick.org (gri needs `convert`)
       - mscgen,        http://www.mcternan.me.uk/mscgen
       - octave,        https://www.gnu.org/software/octave
       - plantuml,      http://plantuml.com
       - ploticus,      http://ploticus.sourceforge.net/doc/welcome.html
       - plotutils,     https://www.gnu.org/software/plotutils
       - pyxplot,       http://pyxplot.org.uk

     %% sudo pip install:
       - blockdiag,     http://blockdiag.com
       - phantomjs,     http://phantomjs.org/ (for mermaid)

     %% git clone
       - protocol,      https://github.com/luismartingarcia/protocol.git

     %% npm install:
       - -g mermaid, https://knsv.github.io/mermaid (and pip install phantomjs)


Pandoc usage

    %% pandoc --filter imagine.py document.md -o document.pdf


Markdown usage

  Imagine takes a Fenced Code Block and runs the associated `cmd` on it:

  ```cmd  ||  {.cmd options=".." keep=true prog=<other-cmd>}
  code
  ```
  =>  cmd <fname>.<cmd> [<options>] <fname>.<fmt>
  <= [ FCB, Para[Image[<fname>.ext]], CodeBlock[stdout]]

  For most of the commands, the FCB's code is stored in <fname>.cmd and it tries
  to run the command as shown.  Any options are passed on the command line,
  while an image filename is suggested via <fname>.<fmt>.

  <fname> is derived from a hash on the entire FCB, so should be specific to
  each individual FCB. Any changes to the codeblock or its attributes should
  lead to new files being created.

  - options=".." will be passed onto the command as shown above
    Defaults to ""

  - keep=true, will retain the original FCB in an anonymous CodeBlock.
    Defaults to false.

  - prog=<other-cmd>, will set the cmd to use.
    Only useful if `cmd` itself is not an appropiate class.

  If the command fails and/or produces no image, the FCB is always retained.
  Any info on stderr is relayed by Imagine, which might be useful for
  troubleshooting.

  Notes:
  - subdir `pd-images` is used to store any input/output files
  - if an output filename exists, it is not regenerated but simply linked to.
  - `packetdiag` & `sfdp`s underlying libraries seem to have some problems.
  - when creating a pdf, images are placed `nearest` to their fenced code block
  - There's no clean up of files in the temp subdir.

  Some commands follow a slightly different pattern:
  - `figlet` or `boxes` produce no images, just text on stdout.  In these cases,
     a CodeBlock with stdout is included.
  - `plot` takes the code as the filename of the image.meta filename to convert
     to an image.


Shebang

  The Imagine filter also features a `shebang` class for fenced code blocks.
  In this case, (fenced) code is saved to disk, the executable flag is set and
  the script is run with the target image filename as its sole argument.

  Any output on stdout is added after the image (if any) in a anonymous
  codeblock. A returncode other than 0 (zero) means the original FCB is
  retained.

  That means that you can use any interpreter and its plotting libraries to
  create your images and/or plots or simply generate text.


Security

  Imagine just hands the fenced code blocks to system commands or simply runs
  them as system scripts themselves (shebang class).  Note that a lot of these
  plotting tools, implement their own 'little' languages which can create
  beautiful images but can also do *great* harm.

  There is no way to check for 'side effects' in advance, so make sure the
  fenced code blocks don't do something devious to your system when running
  them through the Imagine filter.


Imagine command

  Finally, a quick way to read this help text again, is to include a fenced
  codeblock in your markdown document as follows:

    ```imagine
    ```

  or on one or more of the commands supported by Imagine:

    ```imagine
    boxes
    asy
    ```

  That's it!
'''

__version__ = 0.6

import os
import sys
import stat
from textwrap import wrap
from subprocess import Popen, check_output, CalledProcessError, STDOUT, PIPE

import pandocfilters as pf

#-- globs
IMG_BASEDIR = 'pd'
IMG_OUTPUTS = ['fcb', 'img', 'stdout']

# Notes:
# - if walker does not return anything, the element is kept
# - if walker returns a block element, it'll replace current element
# - block element = {'c': <value>, 't': <block_type>}

class HandlerMeta(type):
    def __init__(cls, name, bases, dct):
        'register worker classes by codecs handled'
        for klass in dct.get('codecs', {}):
            cls.workers[klass.lower()] = cls

class Handler(object):
    'baseclass for image/ascii art generators'
    severity  = 'error warn note info debug'.split()
    workers = {}    # dispatch mapping for Handler
    klass = None    # assigned when worker is dispatched
    _output = IMG_OUTPUTS[1]  # i.e. default img
    __metaclass__ = HandlerMeta

    codecs = {}     # worker subclass must override, klass -> cli-program
    level = 2       # log severity level, see above
    outfmt = 'png'  # default output format for a worker

    def __call__(self, codec):
        'Return worker class or self (Handler keeps CodeBlock unaltered)'
        # A worker class with codecs={'': cmd} replaces Handler as default
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
        self.output = '' # catches output by self.cmd, if any

        if codec is None: return  # initial dispatch creation

        (self.id_, self.classes, self.keyvals), self.code = codec
        self.caption, self.typef, self.keyvals = pf.get_caption(self.keyvals)

        # `Extract` Imagine's keyvals from codeblock's attributes
        self.options, self.keyvals = pf.get_value(self.keyvals, u'options', '')
        self.options = self.options.split()
        self.prog, self.keyvals = pf.get_value(self.keyvals, u'prog', None)
        imgout, self.keyvals = pf.get_value(self.keyvals,
                                            u'imgout',
                                            self._output)
        imgout = imgout.lower().replace(',',' ').split()
        self.imgout = self.retain(imgout, IMG_OUTPUTS)

        # prog=cmd key-value trumps .cmd class attribute
        self.prog = self.prog if self.prog else self.codecs.get(self.klass, None)
        if self.prog is None:
            self.msg(0, self.klass, 'not listed in', self.codecs)
            raise Exception('worker has no cli command for %s' % self.klass)

        self.basename = pf.get_filename4code(IMG_BASEDIR, str(codec))
        self.outfile = self.basename + '.%s' % self.outfmt
        self.inpfile = self.basename + '.%s' % self._name.lower()

        self.codetxt = self.code.encode(sys.getfilesystemencoding())
        if not os.path.isfile(self.inpfile):
            self.write('w', self.codetxt, self.inpfile)

    def retain(self, src, allowed):
        'whilst preserving order, limit list of src elements to those allowed'
        # helper for managing imgout lists
        rv = []
        for elm in src:
            if elm in rv: continue # no duplicates
            if elm in allowed:
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
            self.msg(0, 'exception', e)
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

    # def Para(self):
    #     'return Para containing an Image link to the generated image'
    #     retval = pf.Para([self.Url()])
    #     if self.keep:
    #         return [self.AnonCodeBlock(), retval]
    #     return retval

    # def CodeBlock(self, attr, code):
    #     'return a CodeBlock'
    #     retval = pf.CodeBlock(attr, code)
    #     if self.keep:
    #         return [self.AnonCodeBlock(), retval]
    #     return retval

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
                    rv.append(pf.Para([pf.Str('?? missing %s' % self.outfile)]))

            elif output_elm == 'fcb':
                rv.append(self.AnonCodeBlock())

            elif output_elm == 'stdout':
                attr = ['', ['Imagine', 'stdout'], []]
                rv.append(pf.CodeBlock(attr, self.output))

        if len(rv) == 0: return None  # no results -> None keeps original FCB
        if len(rv) > 1: return rv     # multiple results
        return rv[0]                  # just 1 block level element

    def cmd(self, *args, **kwargs):
        'run, possibly forced, a cmd and return success indicator'
        forced = kwargs.get('forced', False) # no need to pop
        stdinput = kwargs.get('stdinput', None)

        if os.path.isfile(self.outfile) and forced is False:
            self.msg(3, 'exists:', *args)
            return True

        try:
            pipes = {'stdin': None if stdinput is None else PIPE,
                     'stdout': PIPE,
                     'stderr': PIPE}
            p = Popen(args, **pipes)
            self.output, err = p.communicate(stdinput)

            # print any complaints on stderr
            if len(err):
                self.msg(1, 'ok?', *args)
                for line in err.splitlines():
                    self.msg(1, '>>:', line)
            else:
                self.msg(2, 'ok:', *args)

            return p.returncode == 0

        except (OSError, CalledProcessError) as e:
            try: os.remove(self.outfile)
            except: pass
            self.msg(1, 'fail:', *args)
            self.msg(0, self.prog , str(e))
            return False

    def image(self, fmt=None):
        'return an Image url or None to keep CodeBlock'
        # workers must override this method
        self.msg(4, self._name, 'keeping CodeBlock as-is (default)')
        return None


class Asy(Handler):
    '''
    ```asy
    code
    ```
    =>  asy -o <fname>.<fmt> [<options>] <fname>.asy
    <=  Para(Image)
    '''

    codecs = {'asy': 'asy', 'asymptote': 'asy'}
    outfmt = 'png'

    def image(self, fmt=None):
        self.fmt(fmt)
        args = ['-o', self.outfile] + self.options + [self.inpfile]
        # args.extend([self.inpfile])
        # args.extend(self.options)
        # args = self.options + [self.inpfile]
        if self.cmd(self.prog, *args): #'-o', self.outfile, *args):
            return self.result()


class Boxes(Handler):
    '''
    ```boxes
    text
    ```
    => boxes [options] <fname>.boxed
    <= CodeBlock(stdout)
    '''
    codecs = {'boxes': 'boxes'}
    outfmt = 'boxed'
    _output = IMG_OUTPUTS[2]  # i.e. default to stdout

    def image(self, fmt=None):
        'return FCB and/or CodeBlock(stdout)'
        # silently ignore 'img', default to stdout if needed
        self.imgout = self.retain(self.imgout, ['fcb', 'stdout'])
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
    ```cmd
    text
    ```
    => cmd -T <fmt> <fname>.txt -o <fname>.ext
    <= Para(Image)

    where cmd is one of:
      blockdiag, segdiag, rackdiag, nwdiag, packetdiag or actdiag

    '''
    progs = 'blockdiag seqdiag rackdiag nwdiag packetdiag actdiag'.split()
    codecs = dict(zip(progs,progs))

    def image(self, fmt=None):
        self.fmt(fmt)
        if self.cmd(self.prog, '-T', self.outfmt, self.inpfile,
                    '-o', self.outfile):
            return self.result()


class Ctioga2(Handler):
    '''
    ```ctioga2
    code
    ```
    => ctioga2 [options] -f <fname>.ctioga2
    -> <fname>.pdf
    <= Para(Image)
    '''
    codecs = {'ctioga2': 'ctioga2'}
    outfmt = 'pdf'

    def image(self, fmt=None):
        self.fmt(fmt)
        args = self.options + ['-f', self.inpfile]
        if self.cmd(self.prog, *args):
            return self.result()


class Ditaa(Handler):
    codecs = {'ditaa': 'ditaa'}

    def image(self, fmt=None):
        self.fmt(fmt)
        args = [self.inpfile, self.outfile, '-T'] + self.options
        if self.cmd(self.prog, *args):
            return self.result()


class Figlet(Handler):
    'figlet `codetxt` -> CodeBlock(ascii art)'
    codecs = {'figlet': 'figlet'}
    outfmt = 'figled'
    _output = IMG_OUTPUTS[2]  # i.e. default to stdout

    def image(self, fmt=None):
        # silently ignore any request for an 'image'
        self.imgout = self.retain(self.imgout, ['fcb', 'stdout'])
        args = self.options
        if self.cmd(self.prog, stdinput=self.codetxt, *args):
            if len(self.output):
                # save figlet's stdout to outfile for next time around
                self.write('w', self.output, self.outfile)
            else:
                self.output = self.read(self.outfile)
            return self.result()


class Flydraw(Handler):
    '''
    ```flydraw
    code
    ```
    => flydraw < code > Image
    <= Para(Image)

    - flydraw reads its command from stdin
    - produces output on stdout, which is saved to <fname>.gif
    - insists on producing GIF files, despite claims in the manual
    '''
    codecs = {'flydraw': 'flydraw'}
    outfmt = 'gif'

    def image(self, fmt=None):
        # silently ignore any request for stdout
        self.imgout = self.retain(self.imgout, ['fcb', 'img'])
        args = self.options
        if self.cmd(self.prog, stdinput=self.codetxt, *args):
            if len(self.output):
                self.write('w', self.output, self.outfile)
            return self.result()


class Gle(Handler):
    'gle -verbosity 0 -output <fname>.<fmt> <fname>.gle'
    codecs = {'gle': 'gle'}

    def image(self, fmt=None):
        self.outfmt = self.fmt(fmt)
        args = self.options + ['-verbosity', '0',
                               '-output', self.outfile,
                               self.inpfile]
        # gle leaves IMG_BASEDIR-images/.gle lying around ...
        if self.cmd(self.prog, *args):
            return self.result()


class GnuPlot(Handler):
    '''
    ```gnuplot
    code
    ```
    => gnuplot [options] <fname>.gnuplot -> image data on stdout
    -> write(stdout, <fname>.fmt)
    <= Para(Image)
    '''
    codecs = {'gnuplot': 'gnuplot'}

    def image(self, fmt=None):
        self.fmt(fmt)
        # stdout captures the graphic image
        self.imgout = self.retain(self.imgout, ['fcb', 'img'])
        args = self.options + [self.inpfile]
        if self.cmd(self.prog, *args):
            if len(self.output):
                self.write('wb', self.output, self.outfile)
            return self.result()


class Graph(Handler):
    '''
    ```graph
    code
    ```
    => graph -T fmt [options] <fname>.graph
    -> write(stdout, <fname>.<fmt>)
    <= Para(Image(<fname>.<fmt>))
    '''
    codecs = {'graph': 'graph'}

    def image(self, fmt=None):
        self.fmt(fmt)
        # stdout is used to capture graphic image data
        self.imgout = self.retain(self.imgout, ['fcb', 'img'])
        args = ['-T', self.outfmt] + self.options + [self.inpfile]
        if self.cmd(self.prog, *args):
            self.write('wb', self.output, self.outfile)
            return self.result()


class Graphviz(Handler):
    '''
    ```graphviz
    code
    ```
    => dot [options] -T<fmt> <fname>.dot <fname>.<fmt>
    '''
    progs = ['dot', 'neato', 'twopi', 'circo', 'fdp', 'sfdp']
    codecs = dict(zip(progs,progs))
    codecs['graphviz'] = 'dot'

    def image(self, fmt=None):
        self.fmt(fmt)
        args = self.options
        args += ['-T%s' % self.outfmt, self.inpfile, '-o', self.outfile]
        if self.cmd(self.prog, *args):
            return self.result()


class Gri(Handler):
    'gri -c 0 -b <x>.gri -> <x>.ps -> <x>.png -> Para(Img(<x>.png))'
    # cannot convince gri to output intermediate ps in pd-images/..
    # so we move it there.
    codecs = {'gri': 'gri'}

    def image(self, fmt=None):
        # args = self.options # + ['-c','0','-b',self.inpfile]
        # args.extend(['-c', '0'])
        # args.extend(['-b', self.inpfile])
        args = self.options + ['-c', '0', '-b', self.inpfile]
        if self.cmd(self.prog, *args):
            # since gri insists on producing a .ps in current working dir
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
    '''wraps self, yields new codeblock w/ Imagine __doc__ string'''
    codecs = {'imagine': 'imagine'}

    def image(self, fmt=None):
        # CodeBlock value = [(Identity, [classes], [(key, val)]), code]
        if len(self.codetxt) == 0:
            return pf.CodeBlock(('',['imagine'],[]), __doc__)
        sep = '-'*60
        doc = []
        for name in self.codetxt.splitlines():
            worker = self.workers.get(name, None)
            doc.append('# %s - %s' % (name, str(worker)))
            if worker.__doc__: doc.append(worker.__doc__)
            else:              doc.append('No help available.')
            doc.append('\n')
        return pf.CodeBlock(('', ['imagine'], []), '\n'.join(doc))


class Mermaid(Handler):
    '''
    ```mermaid
    code
    ```
    => mermaid -o <basedir> [options] <fname>.mermaid
    -> <fname>.mermaid.fmt -> <fname>.fmt
    <= Para(Image)
    '''
    codecs = {'mermaid': 'mermaid'}

    def image(self, fmt=None):
        self.fmt(fmt)
        args = ['-o', IMG_BASEDIR+'-images'] + self.options + [self.inpfile]
        if self.cmd(self.prog, *args):
            # latex chokes on filename.txt.png
            try: os.rename(self.inpfile+'.'+self.outfmt, self.outfile)
            except: pass
            return self.result()

class MscGen(Handler):
    codecs = {'mscgen': 'mscgen'}

    def image(self, fmt=None):
        self.fmt(fmt)
        args = self.options
        args += ['-T', self.outfmt, '-o', self.outfile, self.inpfile]
        if self.cmd(self.prog, *args):
            return self.result()


class Octave(Handler):
    codecs = {'octave': 'octave'}

    def image(self, fmt=None):
        self.fmt(fmt)
        args = ['--no-gui', '-q'] + self.options + [self.inpfile, self.outfile]
        if self.cmd(self.prog, *args):
            # if os.path.isfile(self.outfile):
            return self.result()


class Pic2Plot(Handler):
    '''
    ```pic[2plot]
    code
    ```
    => pic2plot -T <fmt> [options] <fname>.pic2plot
    -> write(stdout, <fname>.<fmt>)
    <= Para(Image)
    '''
    codecs = {'pic2plot': 'pic2plot', 'pic': 'pic2plot'}

    def image(self, fmt=None):
        self.fmt(fmt)
        args = ['-T', self.outfmt] + self.options + [self.inpfile]
        if self.cmd(self.prog, *args):
            self.write('wb', self.output, self.outfile)
            return self.result()


class PlantUml(Handler):
    codecs = {'plantuml': 'plantuml'}

    def image(self, fmt=None):
        self.fmt(fmt)
        args = ['-t' + self.outfmt, self.inpfile]
        if self.cmd(self.prog, *args):
            return self.result()


class Plot(Handler):
    '''
    ```plot
    filename
    ```
    -> test filename exists (is relative to source.md)
    => plot -T <fmt> [options] filename
    -> write(stdout, <fname>.<fmt>)
    <= Para(Image)
    '''
    codecs = {'plot': 'plot'}

    def image(self, fmt=None):
        'fcb code is input filename of meta graphics file'
        self.fmt(fmt)
        if not os.path.isfile(self.codetxt):
            self.msg(0, 'fail: cannot read file %r' % self.codetxt)
            return
        args = ['-T', self.outfmt] + self.options + [self.codetxt]
        if self.cmd(self.prog, *args):
            self.write('wb', self.output, self.outfile)
            return self.result()


class Ploticus(Handler):
    codecs = {'ploticus': 'ploticus'}

    def image(self, fmt=None):
        self.fmt(fmt)
        args = ['-'+self.outfmt, '-o', self.outfile] + self.options
        args += [self.inpfile]
        if self.cmd(self.prog, *args):
            return self.result()


class Protocol(Handler):
    'protocol `codetxt` -> CodeBlock(packet format in ascii)'
    codecs = {'protocol': 'protocol'}
    outfmt = 'protocold'
    _output = IMG_OUTPUTS[2]  # i.e. default to stdout

    def image(self, fmt=None):
        args = self.options + [self.codetxt]
        self.imgout = self.retain(self.imgout, ['fcb', 'stdout'])
        if self.cmd(self.prog, *args):
            if len(self.output):
                self.write('w', self.output, self.outfile)
            else:
                self.output = self.read(self.outfile)
            return self.result()


class PyxPlot(Handler):
    '''
    ```pyxplot
    code
    ```
    .. write('set terminal <fmt>\n' +
              'set output <fname>.<fmt>\n' +
              code,
             <fname>.pyxplot)
    => pyxplot [options] <fname>.pyxplot
    <= Para(Image)
    '''
    codecs = {'pyxplot': 'pyxplot'}

    # need to set output format and output filename in the script...
    def image(self, fmt=None):
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
    ```shebang
    code
    ```
    .. write(code, <fname>.shebang)
    .. chmod u+x <fname>.shebang
    => <fname>.shebang <fname>.<fmt>
    <= Para(Image)
    '''
    'run fenced code block as a hash-bang system script'
    codecs = {'shebang': 'shebang'}

    def image(self, fmt=None):
        self.fmt(fmt)
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

