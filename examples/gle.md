```{.shebang im_out="stdout"}
#!/bin/bash
figlet -c -w 60 gle | boxes -d ian_jones -ph4v1 -i box
```

# [*GLE*](http://gle.sf.net)

## Baudrate

Notes:

- ../test.dat is relative to the input file in pd-images ...


```{.gle im_out="fcb,img" caption="Created by GLE"}
size 18 19

amove 2 1
box 15 16 fill gray60
rmove -1 1
box 15 16 fill white
rmove 2 4
box 11 8 fill gray5

set font texcmr hei 0.6

begin graph
	fullsize
	size 11 8
	title "BAUD Rate = 9600 bit/sec"
	xtitle "Seconds"
	ytitle "Bits"
	data "../dta/test.dat"
	d1 line marker wsquare
	xaxis min -1 max 6
	yaxis min 0 max 11
end graph

```


## simple 2D

```{.gle im_out="fcb,img" caption="Created by GLE"}
size 12 10

set font texcmr
begin graph
   math
   title "f(x) = sin(x)"
   xaxis min -2*pi max 2*pi ftick -2*pi dticks pi/2 format "pi"
   yaxis dticks 0.25 format "frac"
   let d1 = sin(x)
   d1 line color red
end graph
```

## Semi-transparant fills

Needs the `-cairo` option.

```{.gle im_opt="-cairo" im_out="fcb,img" caption="Created by GLE"}
size 10 7

set texlabels 1

begin graph
   scale auto
   title  "Semi-Transparent Fills"
   xtitle "Time"
   ytitle "Output"
   xaxis min 0 max 9
   yaxis min 0 max 6 dticks 1
   let d1 = sin(x)*1.5+1.5 from 0 to 10
   let d2 = 1/x from 0.01 to 10
   let d3 = 10*(1/sqrt(2*pi))*exp(-2*(sqr(x-4)/sqr(2))) from 0 to 10
   key background gray5
   begin layer 300
      fill x1,d1 color rgba255(255,0,0,80)
      d1 line color red key "$1.5\sin(x)+1.5$"
   end layer
   begin layer 301
      fill x1,d2 color rgba255(0,128,0,80)
      d2 line color green key "$1/x$"
   end layer
   begin layer 302
      fill x1,d3 color rgba255(0,0,255,80)
      d3 line color blue key "$\frac{10}{\sqrt{2\pi}}\exp\left(\frac{-2(x-4)^2}{2^2}\right)$"
   end layer
end graph
```

## saddle up

The following GLE script creates saddle.dta, which we want to be put in the dta directory
so the file name is given relative to the pd-images directory.

```{.gle im_out="fcb,img" caption="Created by GLE"}
size 10 9

set font texcmr hei 0.5 just tc

begin letz
   data "../dta/saddle.z"
   z = 3/2*(cos(3/5*(y-1))+5/4)/(1+(((x-4)/3)^2))
   x from 0 to 20 step 0.5
   y from 0 to 20 step 0.5
end letz

amove pagewidth()/2 pageheight()-0.1
write "Saddle Plot (3D)"

begin object saddle
   begin surface
      size 10 9
      data "../dta/saddle.z"
      xtitle "X-axis" hei 0.35 dist 0.7
      ytitle "Y-axis" hei 0.35 dist 0.7
      ztitle "Z-axis" hei 0.35 dist 0.9
      top color blue
      zaxis ticklen 0.1 min 0 hei 0.25
      xaxis hei 0.25 dticks 4 nolast nofirst
      yaxis hei 0.25 dticks 4
   end surface
end object

amove pagewidth()/2 0.2
draw "saddle.bc"
```

## An electronic circuit

```{.gle im_out="fcb,img" caption="Created by GLE"}
! An H-Bridge

size 13 11
include "electronics.gle"

set lwidth 0.05 cap round font psh

! Draw a grid if the line below is uncommented
drawgrid 1

! Top left of diagram
amove 2.0 9.0

! Battery leg
gsave
rline 0 -0.5
cell_v "E_1"
rline 0 -3.5
rline 5 0
rresistor_h R_4
grestore

rresistor_h R_1

gsave
rresistor_v R_2
cell_v "E_2"
grestore

rline 5 0
rresistor_v R_3
rline 0 -4
```

\newpage

\newpage

# Documentation

## Imagine

```imagine
gle
```

## gle --help

```{.shebang im_out="stdout"}
#!/bin/bash
gle --help 2>&1
```


## man page

```{.shebang im_out="stdout"}
#!/bin/bash
MANWIDTH=75 man gle | col -bx | iconv -t ascii//TRANSLIT
```
