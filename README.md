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

A pandoc filter to process codeblocks into images and/or ascii art
------------------------------------------------------------------

Imagine is a pandoc filter that will turn codeblocks tagged with certain
classes into images or ascii art. The following are currently supported:

``` {.__doc__}
actdiag, asy, asymptote, blockdiag, boxes, circo, ctioga2, ditaa, dot, fdp,
figlet, flydraw, gle, gnuplot, graph, graphviz, gri, imagine, mermaid, mscgen,
neato, nwdiag, octave, packetdiag, pic, pic2plot, plantuml, plot, ploticus,
protocol, pyxplot, rackdiag, seqdiag, sfdp, shebang, twopi
```

Examples
--------

### [Mscgen](http://www.mcternan.me.uk/mscgen/)

```` {.fcb}
```{.mscgen imgout="fcb,img"}
msc {
 hscale="1.3", arcgradient = "8";

 a [label="Client"],b [label="Server"];

 a=>b [label="data1"];
 a-xb [label="data2"];
 a=>b [label="data3"];
 a<=b [label="ack1, nack2"];
 a=>b [label="data2", arcskip="1"];
 |||;
 a<=b [label="ack3"];
 |||;
}
```
````

![](pd-images/48e1334a80a0ac5f5854e139f328920f9e7d67c4.png)

### [Octave](https://www.gnu.org/software/octave)

```` {.fcb}
```{.octave imgout="fcb,img"}
figure(1, 'visible', 'off');
surf(peaks);
title("peaks");
print(1, argv(){1});
```
````

![](pd-images/97a5ccef8c2f73c2897bc3f07ebe27fb971d957b.png)

### [Shebang](http://www.google.com/search?q=linux+shebang) using Python & Pygal

```` {.fcb}
```{.shebang imgout="fcb,img"}
#!/usr/bin/env python3
import sys
import pygal
from math import cos
xy_chart = pygal.XY()
xy_chart.title = 'XY Cosinus'
xy_chart.add('x = cos(y)', [(cos(x / 10.), x / 10.) for x in range(-50, 50, 5)])
xy_chart.add('y = cos(x)', [(x / 10., cos(x / 10.)) for x in range(-50, 50, 5)])
xy_chart.render_to_png(sys.argv[-1])
```
````

![](pd-images/8296b8c4e66da192e78d37c805a731fa3374e1c8.png)

### [boxes](http://boxes.thomasjensen.com)

```` {.fcb}
```{.shebang imgout="fcb,stdout"}
#!/bin/bash
# I seem to have got myself boxed in!
cat $0 | boxes -d peek -p h4
```
````

``` {.stdout}
/*       _\|/_
         (o o)
 +----oOO-{_}-OOo------------------------------+
 |    #!/bin/bash                              |
 |    # I seem to have got myself boxed in!    |
 |    cat $0 | boxes -d peek -p h4             |
 +--------------------------------------------*/
```

More [examples](https://github.com/hertogp/imagine/examples) in
sample.pdf

Documentation
-------------

``` {.__doc__}
Imagine
  A pandoc filter to turn fenced codeblocks into graphics or ascii art by
  wrapping some external command line utilities, such as:

    actdiag, asy, asymptote, blockdiag, boxes, circo, ctioga2, ditaa, dot,
    fdp, figlet, flydraw, gle, gnuplot, graph, graphviz, gri, imagine,
    mermaid, mscgen, neato, nwdiag, octave, packetdiag, pic, pic2plot,
    plantuml, plot, ploticus, protocol, pyxplot, rackdiag, seqdiag, sfdp,
    shebang, twopi


Installation

    % sudo pip install pandoc-imagine

    or simply save `pandoc-imagine.py` anywhere along $PATH


Dependencies

    % sudo pip install pandocfilters

    and one (or more) of the packages that provide above utilities.


Pandoc usage

    % pandoc --filter pandoc-imagine.py document.md -o document.pdf


Markdown usage

    ```cmd
    code
    ```

  which will run `cmd` (if known) to proces the `code` into a png image and
  replaces the fenced code block with an Image in a paragraph of its own or any
  ascii art in its own CodeBlock.

  Alternate, longer form:

    ```{.cmd options=".." imgout=".." prog=<other-cmd>}
    code
    ```

  - options="..." will be passed onto the command line.
    Some classes already provide some defaults (as required by the command).

  - imgout="...", csv-list of keywords each specifying a certain output
    - img     image in a paragraph
    - fcb     codeblock (class fcb)    containing the original codeblock
    - stdout, codeblock (class stdout) containing stdout output (if any)
    - stderr, codeblock (class stderr) containing stderr output (if any)

  - prog=<other-cmd>, overrides class-to-command map.
    Only useful if `cmd` itself is not an appropiate class in your document.

  If the command fails, the original fenced code block is retained unchanged.
  Any info on stderr is relayed by Imagine, which might be useful for
  troubleshooting.

  If the command succeeds but produces no image, a line reporting the missing
  image is included in the output document.

  Notes:
  - filenames are based on a hash of the codeblock + its attributes
  - uses subdir `pd-images` to store any input/output files
  - there's no clean up of files stored there
  - if an output filename exists, it is not regenerated but simply linked to.
  - `packetdiag` & `sfdp`s underlying libraries seem to have some problems.

  Some commands follow a slightly different pattern:
  - 'img' directive is ignored by commands that only produce ascii
  - ctioga2 defaults to pdf instead of png
  - flydraw produces a gif, not png
  - gle also creates a .gle subdir inside the images-dir
  - gri produces a ps, which is `convert`ed to png
  - imagine reads its codeblock as help-topics for which a codeblock is returned
  - plot reads its codeblock as the relative path to the file to process
  - pyxplot will have `set terminal` & `set output` prepended to its `code`
  - shebang runs its codeblock as a script with <fname>.png as its argument.
    - use {.shebang imgout="stdout"} for text instead of an png


Security

  Imagine just hands the fenced codeblocks to plotting tools to process or
  simply runs them as system scripts, as-is.

  Shebang's are inherently unsafe and most of the plotting tools implement their
  own 'little' languages, which can create beautiful images, but can also cause
  harm.

  There is no way to check for 'side effects' in advance, so make sure to check
  the fenced codeblocks before running them through the filter.


Imagine class

The imagine class puts documentation of topics at your fingertips, like so:

    ```imagine
    class
    ```

  Use `imagine` as class to get the module's docstring (ie this text) and/or one
  or more of the commands you're interested in, each on a separate line.
```

Individual Classes
------------------

``` {.stdout}
Asy

    sudo-apt-get install asymptote
    http://asymptote.sourceforge.net/
    
    Runs asy -o <fname>.png [options] <fname>.asy
    Wraps:
    -  'asymptote' -> asy
    -  'asy' -> asy

BlockDiag

    sudo pip install blockdiag nwdiag actdiag seqdiag
    http://blockdiag.com/
    
    Runs cmd -T png <fname>.txt -o <fname>.png
    Wraps:
    -  'actdiag' -> actdiag
    -  'blockdiag' -> blockdiag
    -  'rackdiag' -> rackdiag
    -  'seqdiag' -> seqdiag
    -  'packetdiag' -> packetdiag
    -  'nwdiag' -> nwdiag

Boxes

    sudo apt-get install boxes
    http://boxes.thomasjensen.com
    
    Runs boxes [options] <fname>.boxes
    Wraps:
    -  'boxes' -> boxes

Ctioga2

    sudo apt-get install ctioga2
    http://ctioga2.sourceforge.net
    
    Runs ctioga2 [options] -f <fname>.ctioga2
    Wraps:
    -  'ctioga2' -> ctioga2

Ditaa

    sudo apt-get install ditaa
    http://ditaa.sourceforge.net
    
    Runs ditaa <fname>.ditaa <fname>.png -T [options]
    Wraps:
    -  'ditaa' -> ditaa

Figlet

    sudo apt-get install figlet
    http://www.figlet.org
    
    Runs figlet [options] < code-text
    Wraps:
    -  'figlet' -> figlet

Flydraw

    sudo apt-get install flydraw
    http://manpages.ubuntu.com/manpages/precise/man1/flydraw.1.html
    notes:
    - graphic data is printed to stdout
    - so 'stdout' in imgout option is silently ignored
    
    Runs flydraw [options] < code-text
    Wraps:
    -  'flydraw' -> flydraw

Gle

    sudo apt-get install gle-graphics
    http://glx.sourceforge.net
    
    Runs gle -verbosity 0 -output <fname>.<fmt> <fname>.gle
    Wraps:
    -  'gle' -> gle

GnuPlot

    sudo apt-get install gnuplot
    http://www.gnuplot.info
    notes:
    - graphic data is printed to stdout
    - so 'stdout' in imgout option is silently ignored
    
    Runs gnuplot [options] <fname>.gnuplot > <fname>.png
    Wraps:
    -  'gnuplot' -> gnuplot

Graph

    sudo apt-get install plotutils
    https://www.gnu.org/software/plotutils
    notes:
    - graphic data is printed to stdout
    - so 'stdout' in imgout option is silently ignored
    
    Runs graph -T png [options] <fname>.graph
    Wraps:
    -  'graph' -> graph

Graphviz

    sudo apt-get install graphviz
    http://graphviz.org
    
    Runs cmd [options] -T<fmt> <fname>.dot <fname>.<fmt>
    Wraps:
    -  'twopi' -> twopi
    -  'graphviz' -> dot
    -  'fdp' -> fdp
    -  'circo' -> circo
    -  'neato' -> neato
    -  'dot' -> dot
    -  'sfdp' -> sfdp

Gri

    sudo apt-get install gri imagemagick
    http://gri.sourceforge.net
    - requires `convert` from imagemagick
    
    Runs gri -c 0 -b <fname>.gri
    Wraps:
    -  'gri' -> gri

Imagine

    pip install pandoc-imagine
    https://github.com/hertogp/imagine
    
    Runs return documentation in a CodeBlock
    Wraps:
    -  'imagine' -> imagine

Mermaid

    sudo nmp install mermaid
    https://knsv.github.io/mermaid (needs phantomjs)
    
    Runs mermaid -o <basedir> [options] <fname>.mermaid
    Wraps:
    -  'mermaid' -> mermaid

MscGen

    sudo apt-get install mscgen
    http://www.mcternan.me.uk/mscgen
    
    Runs mscgen -T png -o <fname>.png <fname>.mscgen
    Wraps:
    -  'mscgen' -> mscgen

Octave

    sudo apt-get install octave
    https://www.gnu.org/software/octave
    
    Runs octage --no-gui -q [options] <fname>.octave <fname>.png
    Wraps:
    -  'octave' -> octave

Pic2Plot

    sudo apt-get install plotutils
    https://www.gnu.org/software/plotutils
    notes:
    - graphic data is printed to stdout
    - so 'stdout' in imgout option is silently ignored
    
    Runs pic2plot -T png [options] <fname>.pic2plot
    Wraps:
    -  'pic2plot' -> pic2plot
    -  'pic' -> pic2plot

PlantUml

    sudo apt-get install plantuml
    http://plantuml.com
    
    Runs plantuml -t png <fname>.plantuml
    Wraps:
    -  'plantuml' -> plantuml

Plot

    sudo apt-get install plotutils
    https://www.gnu.org/software/plotutils
    notes:
    - graphic data is printed to stdout
    - so 'stdout' in imgout option is silently ignored
    
    Runs plot -T png [options] <code-text-as-filename>
    Wraps:
    -  'plot' -> plot

Ploticus

    sudo apt-get install ploticus
    http://ploticus.sourceforge.net/doc/welcome.html
    
    Runs ploticus -png -o <fname>.png [options] <fname>.ploticus
    Wraps:
    -  'ploticus' -> ploticus

Protocol

    git clone https://github.com/luismartingarcia/protocol.git .
    python setup install
    https://github.com/luismartingarcia/protocol.git
    
    Runs protocol [options] code-text
    Wraps:
    -  'protocol' -> protocol

PyxPlot

    sudo apt-get install pyxplot
    http://pyxplot.org.uk
    
    Runs pyxplot [options] <fname>.pyxplot
    Wraps:
    -  'pyxplot' -> pyxplot

SheBang

    http://www.google.com/search?q=shebang+line
    
    Runs <fname>.shebang [options] <fname>.png
    Wraps:
    -  'shebang' -> shebang

```
