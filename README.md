``` {.stdout}
                                          \\\///
                                         / _  _ \
                                       (| (.)(.) |)
                .--------------------.OOOo--()--oOOO.-------------------.
                |                                                       |
                |        ____                          _                |
                |       /  _/____ ___   ____ _ ____ _ (_)____   ___     |
                |       / / / __ `__ \ / __ `// __ `// // __ \ / _ \    |
                |     _/ / / / / / / // /_/ // /_/ // // / / //  __/    |
                |    /___//_/ /_/ /_/ \__,_/ \__, //_//_/ /_/ \___/     |
                |                           /____/                      |
                |                                                       |
                '-------------------.oooO-------------------------------'
                                     (   )   Oooo.
                                      \ (    (   )
                                       \_)    ) /
                                             (_/
```

A pandoc-filter to turn fenced codeblock's into images or ascii art
-------------------------------------------------------------------

``` {.img.__doc__}
Imagine
  A pandoc filter that turns fenced codeblocks into graphics or ascii art by
  wrapping some external command line utilities, such as:

    actdiag, asy, asymptote, blockdiag, boxes, circo, ctioga2, ditaa, dot,
    fdp, figlet, flydraw, gle, gnuplot, graph, graphviz, gri, imagine,
    mermaid, mscgen, neato, nwdiag, octave, packetdiag, pic, pic2plot,
    plantuml, plot, ploticus, protocol, pyxplot, rackdiag, seqdiag, sfdp,
    shebang, twopi

Installation

  1. Put `imagine.py` anywhere along $PATH (pandoc's search path for filters).
  2. % sudo pip install (mandatory):
       - pandocfilters
  3. % sudo apt-get install (1 or more of):

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

     % sudo pip install:
       - blockdiag,     http://blockdiag.com
       - phantomjs,     http://phantomjs.org/ (for mermaid)

     % git clone
       - protocol,      https://github.com/luismartingarcia/protocol.git

     % npm install:
       - -g mermaid, https://knsv.github.io/mermaid (and pip install phantomjs)


Pandoc usage

    % pandoc --filter imagine.py document.md -o document.pdf


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
```
