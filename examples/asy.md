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

```{.asy im_out="fcb,img" caption="2D example by Asymptote"}
settings.outformat="png";
settings.prc=false;
settings.render=0;
import graph;

size(200,100,IgnoreAspect);

markroutine marks() {
  return new void(picture pic=currentpicture, frame f, path g) {
    path p=scale(1mm)*unitcircle;
    for(int i=0; i <= length(g); ++i) {
      pair z=point(g,i);
      frame f;
      if(i % 4 == 0) {
        fill(f,p);
        add(pic,f,z);
      } else {
        if(z.y > 50) {
          pic.add(new void(frame F, transform t) {
              path q=shift(t*z)*p;
              unfill(F,q);
              draw(F,q);
            });
        } else {
          draw(f,p);
          add(pic,f,z);
        }
      }
    }
  };
}

pair[] f={(5,5),(40,20),(55,51),(90,30)};

draw(graph(f),marker(marks()));

scale(true);

xaxis("$x$",BottomTop,LeftTicks);
yaxis("$y$",LeftRight,RightTicks);
```

## elevation

```{.asy im_out="fcb,img" im_fmt="png"}
settings.outformat="png";
settings.prc=false;
settings.render=0;

import graph3;
import grid3;
import palette;

currentprojection=orthographic(0.8,1,1);
size(400,300,IgnoreAspect);
defaultrender.merge=true;
real f(pair z) {return cos(2*pi*z.x)*sin(2*pi*z.y);}
surface s=surface(f,(-1/2,-1/2),(1/2,1/2),50,Spline);
draw(s,mean(palette(s.map(zpart),Rainbow(40))),black);
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
