```{.shebang im_out="stdout"}
#!/bin/bash
figlet -c -w 60 gnuplot | boxes -d ian_jones -ph4v1 -i box
```


# [*Gnuplot*](http://gnuplot.sourceforge.net)

Note:

- Imagine catches gnuplot's output on stdout and saves it to an output file.
  So don't `set output <name>` or Imagine will get confused and die miserably.


## Line

```{.gnuplot im_out="fcb,img" height=50% caption="Created by GnuPlot"}
set terminal pngcairo transparent enhanced font "arial,10" fontscale 1.0 size 500, 350 
set key inside left top vertical Right noreverse enhanced autotitles box linetype -1 linewidth 1.000
set samples 200, 200
plot [-30:20] besj0(x)*0.12e1 with impulses, (x**besj0(x))-2.5 with points
```

## Real sine

```{.gnuplot im_out="fcb,img" height=50% caption="Created by GnuPlot"}
set terminal pngcairo transparent enhanced font "arial,10" fontscale 1.0 size 500, 350
set key inside left top vertical Right noreverse enhanced autotitles box linetype -1 linewidth 1.000
set samples 400, 400
plot [-10:10] real(sin(x)**besj0(x))
```

## Surface

```{.gnuplot im_out="fcb,img" caption="Another GnuPlot example"}
set terminal pngcairo transparent enhanced font "arial,10" fontscale 1.0 size 500, 350 
set border 4095 front linetype -1 linewidth 1.000
set view 130, 10, 1, 1
set samples 50, 50
set isosamples 50, 50
unset surface
set title "set pm3d scansbackward: correctly looking surface" 
set pm3d implicit at s
set pm3d scansbackward
splot sin(sqrt(x**2+y**2))/sqrt(x**2+y**2)
```

Surface revisted, but now with svg-output.

```{.gnuplot im_out="fcb,img" im_fmt="svg" caption="Surface via svg"}
set terminal svg
set border 4095 front linetype -1 linewidth 1.000
set view 130, 10, 1, 1
set samples 50, 50
set isosamples 50, 50
unset surface
set title "set pm3d scansbackward: correctly looking surface" 
set pm3d implicit at s
set pm3d scansbackward
splot sin(sqrt(x**2+y**2))/sqrt(x**2+y**2)
```

## Interlocking Tori

```{.gnuplot im_fmt="png" im_out="fcb,img" caption="Gnuplot's interlocking Tori example"}
set terminal png
set dummy u,v
set key bmargin center horizontal Right noreverse enhanced autotitles nobox
set parametric
set view 50, 30, 1, 1
set isosamples 50, 20
set hidden3d back offset 1 trianglepattern 3 undefined 1 altdiagonal bentover
set ticslevel 0
set title "Interlocking Tori" 
set urange [ -3.14159 : 3.14159 ] noreverse nowriteback
set vrange [ -3.14159 : 3.14159 ] noreverse nowriteback
splot cos(u)+.5*cos(u)*cos(v),sin(u)+.5*sin(u)*cos(v),.5*sin(v) with lines, 1+cos(u)+.5*cos(u)*cos(v),.5*sin(v),sin(u)+.5*sin(u)*cos(v) with lines
```

```{.gnuplot im_fmt="svg" im_out="fcb,img" caption="Gnuplot's interlocking Tori example"}
set terminal svg
set dummy u,v
set key bmargin center horizontal Right noreverse enhanced autotitles nobox
set parametric
set view 50, 30, 1, 1
set isosamples 50, 20
set hidden3d back offset 1 trianglepattern 3 undefined 1 altdiagonal bentover
set ticslevel 0
set title "Interlocking Tori" 
set urange [ -3.14159 : 3.14159 ] noreverse nowriteback
set vrange [ -3.14159 : 3.14159 ] noreverse nowriteback
splot cos(u)+.5*cos(u)*cos(v),sin(u)+.5*sin(u)*cos(v),.5*sin(v) with lines, 1+cos(u)+.5*cos(u)*cos(v),.5*sin(v),sin(u)+.5*sin(u)*cos(v) with lines
```

# Documentation

## Imagine

```imagine
gnuplot
```

## gnuplot -h

```{.shebang im_out="stdout"}
#!/bin/bash
gnuplot -h
```

## man page

```{.shebang im_out="stdout"}
#!/bin/bash
MANWIDTH=75 man gnuplot | col -bx | iconv -t ascii//TRANSLIT
```
