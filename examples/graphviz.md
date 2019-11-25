```{.shebang im_out="stdout"}
#!/bin/bash
figlet -c -w 60 graphviz | boxes -d ian_jones -ph4v1 -i box
```

# [*graphviz.org*](http://www.graphviz.org)

## `dot` is the default for `graphviz` class

```{im_prg=dot im_opt="-Gsize=4,1.5" caption="FSM layout by dot" im_out="fcb,img"}

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

```{.graphviz im_prg=fdp im_opt="-Gsize=2,3" caption="Created by fdp" im_out="fcb,img"}

digraph {
 blockcode -> fdp;
 fdp -> image;
 image -> blockcode;
 }

```

\newpage

## `sfdp`

```{.graphviz im_out="fcb,img" im_prg=sfdp caption="Created by sfdp"}
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

```{.graphviz im_prg=neato caption="Created by neato" im_out="fcb,img"}
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

The same, but by `twopi`:

```{.graphviz im_prg=twopi caption="Created by twopi" im_out="fcb,img"}
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

```{.graphviz im_prg=circo caption="created by circo" im_out="fcb,img"}

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

## Imagine

```imagine
graphviz
```

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
