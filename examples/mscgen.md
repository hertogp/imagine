---
imagine.mscgen.im_fmt: svg
...

```{.shebang im_out="stdout"}
#!/bin/bash
figlet -c -w 60 mscgen | boxes -d ian_jones -ph4v1 -i box
```

```imagine
mscgen
```

Notes:

- metadata sets mscgen's default output format to `svg`

\newpage

# Local installation

```{.shebang im_out="stdout"}
#!/bin/bash
uname -o
uname -rv
echo
apt show mscgen
```

\newpage

# Examples

## Boxes

```mscgen
msc {

   # The entities
   A, B, C, D;

   # Small gap before the boxes
   |||;

   # Next four on same line due to ','
   A box A [label="box"],
   B rbox B [label="rbox"],
   C abox C [label="abox"],
   D note D [label="note"];

   # Example of the boxes with filled backgrounds
   A abox B [label="abox", textbgcolour="#ff7f7f"];
   B rbox C [label="rbox", textbgcolour="#7fff7f"];
   C note D [label="note", textbgcolour="#7f7fff"];
}
```

\newpage

## Client - Server

```mscgen
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

\newpage

# Documentation

## mscgen -h

```{.shebang im_out="stdout"}
#!/bin/bash
mscgen 2>&1 | grep -vE "^-T"
```

\newpage

## man page

```{.shebang im_out="stdout"}
#!/bin/bash
MANWIDTH=75 man mscgen | col -bx | iconv -t ascii//TRANSLIT
```
