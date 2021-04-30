---
imagine.imprg.im_out: stdout,fcb
imagine.imprg.im_log: 4
...

```{.shebang im_out="stdout"}
#!/bin/bash
figlet -c -w 60 ImPrg-class | boxes -d ian_jones -ph4v1 -i box
```

```imagine
imprg
```

Notes:

- first note

\newpage

# ImPrg, without `im_prg` set

```imprg
#!/bin/bash
cat << 'EOF' | boxes -d peek -ph4v1
This codeblock is missing the required `im_prg`
option for the class `imprg`
                      -- Imagine
EOF
```


\newpage

# ImPrg, with `im_prg`

```{.imprg im_prg="nice -n 10"}
#!/bin/bash
cat << 'EOF' | boxes -d peek -ph4v1
 Kindness is how you treat those who
 can do nothing for you.
                       -- Unknown
EOF
```

\newpage

# ImPrg, with `im_prg` plus `im_opt`

```{.imprg im_prg="nice -n 10" im_opt="Mark Twain"}
#!/bin/bash
cat << EOF | boxes -d peek -ph4v1
Don't wait. The time will never be
just right.
                      -- $1 $2
EOF
```

\newpage

# ImPrg, with `im_prg` and python

```{.imprg im_prg="nice -n 10" im_opt="V8 benchmark results" im_out="img,fcb"}
#!/usr/bin/env python3
import sys, pygal

radar_chart = pygal.Radar()
radar_chart.title = " ".join(sys.argv[1:4])
radar_chart.x_labels = ['Richards', 'DeltaBlue', 'Crypto', 'RayTrace',
                        'EarleyBoyer', 'RegExp', 'Splay', 'NavierStokes']
radar_chart.add('Chrome', [6395, 8212, 7520, 7218, 12464, 1660, 2123, 8607])
radar_chart.add('Firefox', [7473, 8099, 11700, 2651, 6361, 1044, 3797, 9450])
radar_chart.add('Opera', [3472, 2933, 4203, 5229, 5810, 1828, 9013, 4669])
radar_chart.add('IE', [43, 41, 59, 79, 144, 136, 34, 102])
# radar_chart.render()
radar_chart.render_to_png(sys.argv[-1])
```

