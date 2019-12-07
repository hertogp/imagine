---
imagine.shebang.im_out: img,fcb
...

```{.shebang im_out="stdout"}
#!/bin/bash
figlet -c -w 60 pygal | boxes -d ian_jones -ph4v1 -i box
```

```imagine
shebang
```

Notes

- see [*pygal*](http://www.pygal.org/)
- use `shebang` to run python3 to create charts with pygal
- depends on cairosvg, tinycss and cssselect (to render to png)
- install `sudo -H pip3 install cairosvg tinycss pygal`
- unfortunately, some librsvg lib versions donot play well with pygal

\newpage

# [*Pygal*](http://pygal.org/en/stable)

## Solid Gauges

```shebang
#!/usr/bin/env python3

import sys
import pygal

gauge = pygal.SolidGauge(inner_radius=0.70)
percent_formatter = lambda x: '{:.10g}%'.format(x)
dollar_formatter = lambda x: '{:.10g}$'.format(x)
gauge.value_formatter = percent_formatter

gauge.add('Series 1', [{'value': 225000, 'max_value': 1275000}],
          formatter=dollar_formatter)
gauge.add('Series 2', [{'value': 110, 'max_value': 100}])
gauge.add('Series 3', [{'value': 3}])
gauge.add(
    'Series 4', [
        {'value': 51, 'max_value': 100},
        {'value': 12, 'max_value': 100}])
gauge.add('Series 5', [{'value': 79, 'max_value': 100}])
gauge.add('Series 6', 99)
gauge.add('Series 7', [{'value': 100, 'max_value': 100}])

gauge.render_to_png(sys.argv[-1])
```

\newpage

## Basic XY line

```shebang
#!/usr/bin/env python3

import sys
import pygal
from math import cos

xy_chart = pygal.XY()
xy_chart.title = 'XY Cosinus'
xy_chart.add('x = cos(y)', [(cos(x / 10.), x / 10.) for x in range(-50, 50, 5)])
xy_chart.add('y = cos(x)', [(x / 10., cos(x / 10.)) for x in range(-50, 50, 5)])
xy_chart.add('x = 1',  [(1, -5), (1, 5)])
xy_chart.add('x = -1', [(-1, -5), (-1, 5)])
xy_chart.add('y = 1',  [(-5, 1), (5, 1)])
xy_chart.add('y = -1', [(-5, -1), (5, -1)])
xy_chart.render_to_png(sys.argv[-1])
```

\newpage

## radar

```shebang
#!/usr/bin/env python3
import sys, pygal

radar_chart = pygal.Radar()
radar_chart.title = 'V8 benchmark results'
radar_chart.x_labels = ['Richards', 'DeltaBlue', 'Crypto', 'RayTrace',
                        'EarleyBoyer', 'RegExp', 'Splay', 'NavierStokes']
radar_chart.add('Chrome', [6395, 8212, 7520, 7218, 12464, 1660, 2123, 8607])
radar_chart.add('Firefox', [7473, 8099, 11700, 2651, 6361, 1044, 3797, 9450])
radar_chart.add('Opera', [3472, 2933, 4203, 5229, 5810, 1828, 9013, 4669])
radar_chart.add('IE', [43, 41, 59, 79, 144, 136, 34, 102])
# radar_chart.render()
radar_chart.render_to_png(sys.argv[-1])
```

# Documentation

See [pygal's website](http://www.pygal.org/en/stable/documentation/index.html)
