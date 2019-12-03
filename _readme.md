
```{.shebang im_out="stdout"}
#!/bin/bash
echo "$(figlet -kcf slant Imagine)" | boxes -d ian_jones -p h4v1
```

## A pandoc filter to process codeblocks into images and/or ascii art

Imagine is a pandoc filter that will turn codeblocks tagged with certain
classes into images or ascii art. The following are currently supported:

```imagine
classes
```

## Examples

### [Mscgen](http://www.mcternan.me.uk/mscgen/)

```{.mscgen im_out="img,fcb" im_fmt="png"}
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

### [Mermaid](https://github.com/mermaidjs/mermaid.cli)

```{.mermaid im_opt="-H 300" im_fmt="png" im_out="img,fcb"}
sequenceDiagram
    Alice ->> Bob: Hello Bob, how are you?
    Bob-->>John: How about you John?
    Bob--x Alice: I am good thanks!
    Bob-x John: I am good thanks!
    Note right of John: Bob thinks a long<br/>long time, so long<br/>that the text does<br/>not fit on a row.

    Bob-->Alice: Checking with John...
    Alice->John: Yes... John, how are you?
```

### [Gnuplot](http://www.gnuplot.info)

```{.gnuplot im_fmt="png" im_out="img,fcb"}
set terminal png
set dummy u,v
set key bmargin center horizontal Right noreverse enhanced autotitles nobox
set parametric
set view 50, 30, 1, 1
set isosamples 50, 20
set hidden3d back offset 1 trianglepattern 3 undefined 1 altdiagonal bentover
set ticslevel 0
set title "Interlocking Tori"
set urange [ -3.14159 : 3.14159 ] noreverse nowriteback
set vrange [ -3.14159 : 3.14159 ] noreverse nowriteback
splot cos(u)+.5*cos(u)*cos(v),sin(u)+.5*sin(u)*cos(v),.5*sin(v) \
with lines, 1+cos(u)+.5*cos(u)*cos(v),\
.5*sin(v),sin(u)+.5*sin(u)*cos(v) with lines
```


### [Shebang](http://www.google.com/search?q=linux+shebang) using Python & Pygal

```{.shebang im_fmt="png" im_out="img,fcb"}
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

### [boxes](http://boxes.thomasjensen.com)

```{.shebang im_out="stdout,fcb"}
#!/bin/bash
# I seem to have got myself boxed in!
cat $0 | boxes -d peek -p h4
```

More examples on [github](https://github.com/hertogp/imagine/examples), which
include better formats than `png`.

## Documentation

```imagine
```

## Individual Classes

```{.shebang im_out="stdout"}
#!/usr/bin/env python
import sys
sys.path.append('.')
import pandoc_imagine

classes = set(pandoc_imagine.Handler.workers.values())
for cls in sorted(classes, key=lambda x: x.__name__):
    print(cls.__name__)
    print(cls.__doc__)
    print('    Runs', cls.image.__doc__)
    print('    Wraps:')
    for klass,cmd in cls.cmdmap.items():
        print('    - ', repr(klass), '->', cmd)
    print("")
```
