```{.shebang im_out="stdout"}
#!/bin/bash
figlet -c -w 60 ctioga2 | boxes -d ian_jones -ph4v1 -i box
```

```imagine
ctioga2
```

\newpage

# [*ctioga2*](http://ctioga2.sourceforge.net)

## Parabolas, filling & intersection

```{.ctioga2 caption="Created by ctioga2" width=60%}
title "Intersection of two parabolas"
math
plot x*x /fill=top /fill-transparency 0.8 /legend '$x^2$'
plot 50-x*x /fill=bottom /fill-transparency 0.8 /legend '$50 - x^2$'
```

## a grid system

```{.ctioga2 caption="Created by ctioga2" width=60%}
define-axis-style '.grid-non-left axis.left' /decoration=ticks /axis-label-text=' '
define-axis-style '.grid-non-bottom axis.bottom' /decoration=ticks /axis-label-text=' '
define-background-style '.grid-odd-column background' /background-color Blue!15
define-axis-style '.grid-2-0 axis' /decoration=None

setup-grid 3x2 /top=1mm /right=2mm /dy=2mm /dx=2mm
math 
    

inset grid:next
  plot sin(x)
next-inset grid:next
  plot cos(x)
next-inset grid:next
  plot -cos(x)
next-inset grid:next
  plot x**2
next-inset grid:next
  plot 10*x
next-inset grid:next
  plot 0.1*x**3
end
```

## plotting data

The data file's name `../dta/cr2-ex01.dat` is relative to where the fenced code
block contents was saved, usually in ./pd-images although you can change that
via the `im_dir` option.

```{.ctioga2 caption="Created by ctioga2" width=60%}
draw-line -15,0 15,0 /style=Dashes /color=Gray
plot ../dta/ct2-ex01.dat
plot ../dta/ct2-ex01.dat@1:3
title '\centering This is a very long title about sine waves'  \
      /text-width=5cm /shift=1.3
xlabel 'My $x$ label'
ylabel 'My $y$ label'
plot ../dta/ct2-ex01.dat@'$1:$2*0.5'
plot ../dta/ct2-ex01.dat@'$1:0.5*($2-$3)'
```

\newpage

# Documentation

## ctioga2 -h

```{.shebang im_out="stdout"}
#!/bin/bash
ctioga2 -h
```

\newpage

## man page

```{.shebang im_out="stdout"}
#!/bin/bash
MANWIDTH=75 man ctioga2 | col -bx | iconv -t ascii//TRANSLIT
```
