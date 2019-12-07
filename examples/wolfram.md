---
imagine.shebang.im_out: img,fcb
...

```{.shebang im_out="stdout"}
#!/bin/bash
figlet -c -w 75 WolframScript | boxes -d ian_jones -ph4v1 -i box
```

```imagine
shebang
```

Notes

- sudo -H bash ~/installs/wolfram/WolframEngine_12.0.1_LINUX.sh
- create account on https://account.wolfram.com & get a free license
- first invoke `wolframscript` to activate the wolfram kernel & set license
- use `$ScriptCommandLine[[2]]` to pickup the destination filename

\newpage

# Examples

Examples from
[*wolfram cloud*](https://reference.wolframcloud.com/language/)

## WienerProcess (png)

```shebang
#!/usr/bin/env wolframscript
Export[$ScriptCommandLine[[2]],
ListLinePlot[RandomFunction[WienerProcess[],{0,10,0.01},10]]
]
```

Notes:

- `png` is imagine's default output format

\newpage

## Nearby words

```{.shebang im_fmt=gif im_out=img,fcb,stdout,stderr, im_log=4}
#!/usr/bin/env wolframscript
words = DictionaryLookup["pand*"];
g = Graph[Flatten[Map[(Thread[# \[DirectedEdge]
                      DeleteCases[Nearest[words, #, 3], #]]) &, words]],
    VertexLabels -> "Name", ImageSize -> 450
];
Export[$ScriptCommandLine[[2]], GraphPlot[g]]
```

\newpage

## Meixner (svg)

```{.shebang im_fmt=svg}
#!/usr/bin/env wolframscript
Export[$ScriptCommandLine[[2]],
Plot[Table[
PDF[MeixnerDistribution[2, b, 0, 1], x], {b, {-2, 0, 1.5}}] //
Evaluate, {x, -8, 8}, Exclusions -> None, Filling -> Axis]
]
```

## Meixner again

```{.shebang im_fmt=svg}
#!/usr/bin/env wolframscript

dist = MeixnerDistribution[2, b, 0, 1]; 
cdf = Function[{x, b}, Evaluate[CDF[dist, x]]];
ql = {0.025, 0.10, 0.25, 0.5, 0.75, 0.90, 0.975};
cl = Table[ColorData["Rainbow"][q], {q, Join[{0.0}, ql]}];

Export[$ScriptCommandLine[[2]],
Legended[Plot3D[PDF[dist, x], {x, -5, 5}, {b, -1, 2},
PlotTheme -> "Marketing", MeshFunctions -> {cdf}, Mesh -> {ql},
MeshStyle -> GrayLevel[0.8], MeshShading -> cl,
AxesLabel -> Automatic, BaseStyle -> Opacity[0.9], ImageSize -> 400,
PlotRange -> All, Exclusions -> None, PlotPoints -> 50],
BarLegend["Rainbow", ql, LegendLabel -> "prob"]]
]
```

\newpage

## Queueing properties

```{.shebang im_fmt=svg}
#!/usr/bin/env wolframscript
\[Gamma] = {0, 0, 0, 0};
r = {{0, 0.5, 0.3, 0.2}, {1, 0, 0, 0}, {1, 0, 0, 0}, {1, 0, 0, 0}};
\[Mu] = {1, 0.5, 1, 2}; c = {1, 1, 1, 1}; k = 7;

\[ScriptCapitalN] = QueueingNetworkProcess[\[Gamma], r, \[Mu], c, k];

data = RandomFunction[\[ScriptCapitalN], {0, 10^4}];
Export[$ScriptCommandLine[[2]],
{QueueProperties[{\[ScriptCapitalN], 2}], QueueProperties[{data, 2}]}
]
```

\newpage

## 3D plot

```{.shebang im_fmt=svg}
#!/usr/bin/env wolframscript
Export[$ScriptCommandLine[[2]],
  GraphPlot3D[
  SimpleGraph[Table[i \[UndirectedEdge] Mod[i^2, 75], {i, 75}]],
  EdgeShapeFunction -> ({Cylinder[#1, 0.1]} &),
  VertexShapeFunction -> ({Sphere[#, 0.3]} &)]
]
```

\newpage

# Documentation

## wolfram -h

```{.shebang im_out=stdout}
#!/bin/bash
wolframscript -h
```

\newpage

## man page

```{.shebang im_out=stdout}
#!/bin/bash
MANWIDTH=75 man wolframscript | col -bx | iconv -t ascii//TRANSLIT
```
