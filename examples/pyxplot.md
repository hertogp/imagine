```{.shebang im_out="stdout"}
#!/bin/bash
figlet -c -w 60 pyxplot | boxes -d ian_jones -ph4v1 -i box
```

# [*PyxPlot*](http://pyxplot.org.uk)

Note:
- sudo apt-get install pyxplot fails on Ubuntu 18.03 bionic
- appears that installing pyxplot from source, requires python2 ... alas!

## ex01

```{.pyxplot im_out="fcb,img" caption="Created by PyxPlot"}
set numerics complex
set xlabel r"$x$"
set ylabel r"$y$"
set zlabel r"$z$"
set xformat r"%s$\pi$"%(x/pi)
set yformat r"%s$\pi$"%(y/pi)
set xtics 3*pi ; set mxtics pi
set ytics 3*pi ; set mytics pi
set ztics 
set key below
set size 6 square
set grid
plot 3d [-6*pi:6*pi][-6*pi:6*pi][-0.3:1] sinc(hypot(x,y)) \
     with surface col black \
     fillcol hsb(atan2($1,$2)/(2*pi)+0.5,hypot($1,$2)/30+0.2,$3*0.5+0.5)
```


\newpage

# Documentation

## Imagine

```imagine
pyxplot
```

## pyxplot -h

```{.shebang im_out="stdout"}
#!/bin/bash
pyxplot -h
```

## man page

```{.shebang im_out="stdout"}
#!/bin/bash
MANWIDTH=75 man pyxplot | col -bx | iconv -t ascii//TRANSLIT
```
