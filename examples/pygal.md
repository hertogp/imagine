```{.shebang im_out="stdout"}
#!/bin/bash
figlet -c -w 60 pygal | boxes -d ian_jones -ph4v1 -i box
```


# [*Pygal*](http://pygal.org/en/stable)

Notes
- uses python3
- depends on cairosvg, tinycss and cssselect (to render to png)

Install
- sudo -H pip3 install pygal
- sudo -H pip3 install cairosvg
- sudo -H pip3 install tinycss


## Solid Gauges

```{.shebang im_out="fcb,img" caption="Created by Pygal"}
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

## Basic XY line

```{.shebang im_out="fcb,img" caption="Created by Pygal"}
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

