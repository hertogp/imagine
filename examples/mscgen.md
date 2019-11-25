```{.shebang im_out="stdout"}
#!/bin/bash
figlet -c -w 60 mscgen | boxes -d ian_jones -ph4v1 -i box
```


# [*Mscgen*](http://www.mcternan.me.uk/mscgen/)

## example w/ boxes

```{.mscgen im_out="fcb,img" caption="Created by mscgen"}
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

## client-server interaction

```{.mscgen im_out="fcb,img" caption="Created by mscgen"}
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

## Imagine

```imagine
mscgen
```

## mscgen -h

```{.shebang im_out="stdout"}
#!/bin/bash
mscgen 2>&1 | grep -vE "^-T"
```

## man page

```{.shebang im_out="stdout"}
#!/bin/bash
MANWIDTH=75 man mscgen | col -bx | iconv -t ascii//TRANSLIT
```
