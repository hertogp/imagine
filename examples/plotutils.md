```{.shebang im_out="stdout"}
#!/bin/bash
figlet -c -w 60 plotutils | boxes -d ian_jones -ph4v1 -i box
```

# [*Plotutils*](https://www.gnu.org/software/plotutils)

It includes:

- GNU *`graph`*, which plots 2-D datasets or data streams in real time.
- GNU *`plot`*, which translates GNU Metafile format to any of the other formats.
- GNU *`tek2plot`*, for translating legacy Tektronix data to any of the above
  formats.
- GNU *`pic2plot`*, for translating the pic language (a scripting language for
  designing box-and-arrow diagrams) to any of the above formats. The pic language
  was designed at Bell Labs as an enhancement to the troff text formatter. 
- GNU *`plotfont`*, for displaying character maps of the fonts that are available
  in the above formats.
- GNU *`spline`*, which does spline interpolation of data. It normally uses either
  cubic spline interpolation or exponential splines in tension, but it can
  function as a real-time filter under some circumstances.
- GNU *`ode`*, which numerically integrates a system consisting of one or more
  ordinary differential equations.

Note:

- Imagine only wraps `plot` and `pic2plot` (`pic` is an alias for `pic2plot`).

## graph

Each invocation of
[graph](https://www.gnu.org/software/plotutils/manual/en/html_node/graph-Invocation.html#graph-Invocation)
reads one or more datasets from files named on the command line or from
standard input, and prepares a plot. There are many command-line options for
adjusting the visual appearance of the plot. The following sections explain how
to use the most frequently used options, by giving examples.

```{.graph im_opt="-X x-axis -Y y-axis -f 0.1 --bitmap-size 200x200" im_out="fcb,img"
caption="PlotUtil's graph"}
0.0  0.0
1.0  0.2
2.0  0.0
3.0  0.4
4.0  0.2
5.0  0.6
```

## plot

The GNU *`plot`* filter displays GNU graphics metafiles or translates them to
other formats. It will take input from files specified on the command line or
from standard input. The ‘-T’ option is used to specify the desired output
format. Supported output formats include "X", "png", "pnm", "gif", "svg", "ai",
"ps", "cgm", "fig", "pcl", "hpgl", "regis", "tek", and "meta" (the default).

The metafile format is a device-independent format for storage of vector
graphics. By default, it is a binary rather than a human-readable format (see
Metafiles). Each of the graph, pic2plot, tek2plot, and plotfont utilities will
write a graphics metafile to standard output if no ‘-T’ option is specified on
its command line. The GNU libplot graphics library may also be used to produce
metafiles. Metafiles may contain arbitrarily many pages of graphics, but each
metafile produced by graph contains only a single page.

*`plot`*, like the metafile format itself, is useful if you wish to preserve a
vector graphics file, and display or edit it with more than one drawing editor.

```{.plot im_opt="--bitmap-size 300x200" im_out="fcb,img" caption="Created by plot"}
dta/input.meta
```


## pic2plot

*From the gnu website*:

The [pic language](
https://www.gnu.org/software/plotutils/manual/en/html_node/pic2plot-Introduction.html#pic2plot-Introduction)
is a 'little language' that was developed at Bell Laboratories for creating
box-and-arrow diagrams of the kind frequently found in technical papers and
textbooks. A directory containing documentation on the pic language is
distributed along with the plotting utilities. On most systems it is installed
as /usr/share/pic2plot or /usr/local/share/pic2plot. The directory includes
Brian Kernighan's original technical report on the language, Eric S. Raymond's
[tutorial](http://floppsie.comp.glam.ac.uk/Glamorgan/gaius/web/pic.html) on the
GNU implementation, and some sample pic macros contributed by the late W.
Richard Stevens.


```{.pic im_out=img width=80% caption="Created by pic"}
.PS
box "START"; arrow; circle dashed filled; arrow
circle diam 2 thickness 3 "This is a" "big, thick" "circle" dashed; up
arrow from top of last circle; ellipse "loopback" dashed
arrow dotted from left of last ellipse to top of last box
arc cw radius 1/2 from top of last ellipse; arrow
box "END"
.PE
```


# Documentation

## Imagine

```imagine
graph
```

```imagine
plot
```

```imagine
pic
```


## graph --help

```{.shebang im_out="stdout"}
#!/bin/bash
graph --help
```

## pic --help

```{.shebang im_out="stdout"}
#!/bin/bash
pic --help
```

## plot --help


```{.shebang im_out="stdout"}
#!/bin/bash
plot --help
```

## man pages

### man graph

```{.shebang im_out="stdout"}
#!/bin/bash
MANWIDTH=75 man graph | col -bx | iconv -t ascii//TRANSLIT
```

### man pic

```{.shebang im_out="stdout"}
#!/bin/bash
MANWIDTH=75 man pic | col -bx | iconv -t ascii//TRANSLIT
```

### man plot

```{.shebang im_out="stdout"}
#!/bin/bash
MANWIDTH=75 man plot | col -bx | iconv -t ascii//TRANSLIT
```
