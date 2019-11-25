```{.shebang im_out="stdout"}
#!/bin/bash
figlet -c -w 60 asy | boxes -d ian_jones -ph4v1 -i box
```

# *[Asymptote](http://asymptote.sourceforge.net/)*

Notes:

- eps formatted images don't go well together with pandoc.


## a plot

```{.asy im_out="fcb,img" caption="Plot created by Asymptote"}
settings.outformat="png";
settings.prc=false;
settings.render=0;
import three;
size(6cm,0);
draw(O--2X ^^ O--2Y ^^ O--2Z);
triple circleCenter = (Y+Z)/sqrt(2) + X;
path3 mycircle = circle(c=circleCenter, r=1, normal=Y+Z);
draw(plane(O=sqrt(2)*Z, 2X, 2*unit(Y-Z)), gray + 0.1cyan);
draw(mycircle, blue);
draw(shift(circleCenter) * (O -- Y+Z), green, arrow=Arrow3());
```

## a sphere

```{.asy im_out="fcb,img" caption="Sphere created by Asymptote"}
settings.outformat="png";
settings.prc=false;
settings.render=0;
import graph3;
size(8cm,0);
path3 myarc = rotate(18,Z) * Arc(c=O, normal=X, v1=-Z, v2=Z, n=10);
surface backHemisphere = surface(myarc, angle1=0, angle2=180, c=O, axis=Z, n=10);
surface frontHemisphere = surface(myarc, angle1=180, angle2=360, c=O, axis=Z, n=10);
draw(backHemisphere, surfacepen=material(white+opacity(0.8), ambientpen=white), meshpen=gray(0.4));
draw(O--X, blue+linewidth(1pt));
```

## elevation

```{.asy im_out="fcb,img" im_fmt="png"}
settings.outformat="png";
settings.prc=false;
settings.render=0;
import graph3;
import grid3;
import palette;

currentprojection=orthographic(0.8,1,2);
size(400,300,IgnoreAspect);

real f(pair z) {return cos(2*pi*z.x)*sin(2*pi*z.y);}

surface s=surface(f,(-1/2,-1/2),(1/2,1/2),50,Spline);

surface S=planeproject(unitsquare3)*s;
S.colors(palette(s.map(zpart),Rainbow()));
draw(S,nolight);
draw(s,lightgray+opacity(0.7));

grid3(XYZgrid);
```

# Documentation

## Imagine

```imagine
asy
```

## asy -h
```{.shebang im_out="stdout"}
#!/bin/bash
asy -h
```

## man page

```{.shebang im_out="stdout"}
#!/bin/bash
MANWIDTH=75 man asy | col -bx | iconv -t ascii//TRANSLIT
```
