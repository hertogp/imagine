---
imagine.graphviz.im_fmt: svg
imagine.fdp.im_fmt: svg
...

```{.shebang im_out="stdout"}
#!/bin/bash
figlet -c -w 60 graphviz | boxes -d ian_jones -ph4v1 -i box
```

```imagine
graphviz
```

Notes

- `graphviz` class defaults to `dot`

\newpage

# [*graphviz*](http://www.graphviz.org) examples

## `Graphviz` (svg)

```{.graphviz im_opt="-Gsize=4,1.5" caption="Created by Graphviz"}

digraph finite_state_machine {
  rankdir=LR;
  size="6,3"
  node [shape = doublecircle]; LR_0 LR_3 LR_4 LR_8;
  node [shape = circle];
  LR_0 -> LR_2 [ label = "SS(B)" ];
  LR_0 -> LR_1 [ label = "SS(S)" ];
  LR_1 -> LR_3 [ label = "S($end)" ];
  LR_2 -> LR_6 [ label = "SS(b)" ];
  LR_2 -> LR_5 [ label = "SS(a)" ];
  LR_2 -> LR_4 [ label = "S(A)" ];
  LR_5 -> LR_7 [ label = "S(b)" ];
  LR_5 -> LR_5 [ label = "S(a)" ];
  LR_6 -> LR_6 [ label = "S(b)" ];
  LR_6 -> LR_5 [ label = "S(a)" ];
  LR_7 -> LR_8 [ label = "S(b)" ];
  LR_7 -> LR_5 [ label = "S(a)" ];
  LR_8 -> LR_6 [ label = "S(b)" ];
  LR_8 -> LR_5 [ label = "S(a)" ];
}

```

\newpage

## `fdp`

```{.fdp im_opt="-Gsize=2,3" caption="Created by fdp"}

digraph {
 blockcode -> fdp;
 fdp -> image;
 image -> blockcode;
 }

```

\newpage

## `sfdp`

```{.sfdp caption="Created by sfdp"}
graph G {
size="8,4"
run -- intr;
intr -- runbl;
runbl -- run;
run -- kernel;
kernel -- zombie;
kernel -- sleep;
kernel -- runmem;
sleep -- swap;
swap -- runswap;
runswap -- new;
runswap -- runmem;
new -- runmem;
sleep -- runmem;
}
```

\newpage

## `neato`

States in a kernel OS plotted by `neato`:

```{.neato caption="Created by neato"}
graph G {
size="3,2"
run -- intr;
intr -- runbl;
runbl -- run;
run -- kernel;
kernel -- zombie;
kernel -- sleep;
kernel -- runmem;
sleep -- swap;
swap -- runswap;
runswap -- new;
runswap -- runmem;
new -- runmem;
sleep -- runmem;
}
```

\newpage

## `twopi`

```{.twopi caption="Created by twopi"}
graph G {
size="3,2"
run -- intr;
intr -- runbl;
runbl -- run;
run -- kernel;
kernel -- zombie;
kernel -- sleep;
kernel -- runmem;
sleep -- swap;
swap -- runswap;
runswap -- new;
runswap -- runmem;
new -- runmem;
sleep -- runmem;
}
```

\newpage

## `circo`

Again, the same but by `circo`:

```{.circo caption="created by circo"}

graph G {
size="3,2"
run -- intr;
intr -- runbl;
runbl -- run;
run -- kernel;
kernel -- zombie;
kernel -- sleep;
kernel -- runmem;
sleep -- swap;
swap -- runswap;
runswap -- new;
runswap -- runmem;
new -- runmem;
sleep -- runmem;
}
```

\newpage

# Documentation

## dot -h

```{.shebang im_out="stdout"}
#!/bin/bash
dot -?
```

## man page

```{.shebang im_out="stdout"}
#!/bin/bash
MANWIDTH=75 man graphviz | col -bx | iconv -t ascii//TRANSLIT
```
