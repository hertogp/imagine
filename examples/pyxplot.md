```{.shebang im_out="stdout"}
#!/bin/bash
figlet -c -w 60 pyxplot | boxes -d ian_jones -ph4v1 -i box
```

```imagine
pyxplot
````


Note:

- no `sudo apt-get install pyxplot` on Ubuntu 18.04 bionic
- to install, download & unpack pyxplot, and:

```
    virtualenv venv -p /usr/bin/python2  # installerscripts need python2
    source venv/bin/activate
    make
    sudo make install
```

\newpage

## Surface

```pyxplot
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

## Numerical integration

```pyxplot
set samples 80
set key bottom right
set xformat r"%s$\pi$"%(x/pi)
set yformat r"%s$\pi$"%(y/pi)
set xrange [-5*pi:5*pi]
set width 7
set key below
plot int_dz(sinc(z),0,x)
```

\newpage

## Surface and contours

```pyxplot
set xlabel "$x$"
set ylabel "$y$"
set zlabel "$x^3/20+y^2$"
set nokey
set size 6 square
set nogrid
plot 3d x**3/20+y**2 with surface col black fillc green, \
        x**3/20+y**2 with contours col black
```

\newpage

# Documentation [*PyxPlot*](http://pyxplot.org.uk)

## pyxplot -h

```{.shebang im_out="stdout"}
#!/bin/bash
pyxplot -h
```

\newpage

## man page

```{.shebang im_out="stdout"}
#!/bin/bash
MANWIDTH=75 man pyxplot | col -bx | iconv -t ascii//TRANSLIT
```
