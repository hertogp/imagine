```{.shebang imgout="stdout"}
#!/bin/bash
echo "$(figlet -kcf slant Imagine)" | boxes -d ian_jones -p h4
```


## A pandoc filter to process codeblocks into images and/or ascii art

Imagine is a pandoc filter that will turn codeblocks tagged with certain
classes into images or ascii art. The following classes are currently
supported:

```imagine
classes
```


## Examples

### *[Mscgen](http://www.mcternan.me.uk/mscgen/)*

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

### *[Octave](https://www.gnu.org/software/octave)*

```{.octave imgout="fcb,img"}
figure(1, 'visible', 'off');
surf(peaks);
title("peaks");
print(1, argv(){1});
```


### *[Shebang](http://www.google.com/search?q=linux+shebang)* using Python & Pygal

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


### *[boxes](http://boxes.thomasjensen.com)*

```{.shebang imgout="fcb,stdout"}
#!/bin/bash
# I seem to have got myself boxed in!
cat $0 | boxes -d peek -p h4
```

See [sample.pdf](examples/sample.pdf) for more examples.


## Documentation

```imagine
```

## Individual Classes

```{.shebang imgout="stdout"}
#!/usr/bin/env python
import sys
sys.path.append('.')
import pandoc_imagine

classes = set(pandoc_imagine.Handler.workers.values())
for cls in sorted(classes, key=lambda x: x.__name__):
    print cls.__name__
    print cls.__doc__
    print '    Runs', cls.image.__doc__
    print '    Wraps:'
    for klass,cmd in cls.cmdmap.items():
        print '    - ', repr(klass), '->', cmd
    print
```
