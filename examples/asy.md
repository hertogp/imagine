```{.shebang im_out="stdout"}
#!/bin/bash
figlet -c -w 60 asymptote | boxes -d ian_jones -ph4v1 -i box
```

```Imagine
asy
```

Notes:

- `settings.outformat=<fmt>` should match `im_fmt=<fmt>`-option.
- `settings.libgs="";` stops asy from passing `--libgs` to `dvisvgm`
- `svg` format seems to create an svg file that links to a `png` image, which
  shows up empty in a pdf after pandoc conversion.

\newpage

## Aymptote logo (pdf)

```{.asy im_fmt="pdf" caption="Logo"}
import three;
settings.libgs="";          // workaround for how asy calls dvisvgm
settings.outformat="pdf";
settings.render=1;

size(560,320,IgnoreAspect); // Fullsize
size3(140,80,15);
currentprojection=perspective(-2,20,10,up=Y);
currentlight=White;
viewportmargin=(0,10);

real a=-0.4;
real b=0.95;
real y1=-5;
real y2=-3y1/2;
path A=(a,0){dir(10)}::{dir(89.5)}(0,y2);
path B=(0,y1){dir(88.3)}::{dir(20)}(b,0);
real c=0.5*a;
pair z=(0,2.5);
transform t=scale(1,15);
transform T=inverse(scale(t.yy,t.xx));
path[] g=shift(0,1.979)*scale(0.01)*t*
  texpath(Label("{\it symptote}",z,0.25*E+0.169S,fontsize(24pt)));
pair w=(0,1.7);
pair u=intersectionpoint(A,w-1--w);

real h=0.25*linewidth();
real hy=(T*(h,h)).x;
g.push(t*((a,hy)--(b,hy)..(b+hy,0)..(b,-hy)--(a,-hy)..(a-hy,0)..cycle));
g.push(T*((h,y1)--(h,y2)..(0,y2+h)..(-h,y2)--(-h,y1)..(0,y1-h)..cycle));
g.push(shift(0,w.y)*t*((u.x,hy)--(w.x,hy)..(w.x+hy,0)..(w.x,-hy)--(u.x,-hy)..(u.x-hy,0)..cycle));
real f=0.75;
g.push(point(A,0)--shift(-f*hy,f*h)*A--point(A,1)--shift(f*hy,-f*h)*reverse(A)--cycle);
g.push(point(B,0)--shift(f*hy,-f*h)*B--point(B,1)--shift(-f*hy,f*h)*reverse(B)--cycle);

triple H=-0.1Z;
material m=material(lightgray,shininess=1.0);

for(path p : g)
  draw(extrude(p,H),m);

surface s=surface(g);
draw(s,red,nolight);
draw(shift(H)*s,m);
```

\newpage

## Barnsley's fern (eps)

```{.asy im_fmt="eps" caption="barnsley's fern"}
// Barnsley's fern
// Fougère de Barnsley
size(10cm,0);

real ab=72, ac=-7;
real rc=0.85, rb=0.35;
path trk=(0,0)--(0,1);

transform ta=shift(0,1)*rotate(ab)*scale(rb);
transform tb=shift(0,1)*rotate(-ab)*scale(rb);
transform tc=shift(0,1)*rotate(ac)*scale(rc);
transform td=shift(0,1)*rotate((ab+ac)/2)*scale(rb);
transform te=shift(0,1)*rotate(-(ab+ac)/2)*scale(rb);

picture pic;
draw(pic,trk,red+.8green);

//Construct a fern branch as atractor
int nbit=7;
for(int i=1; i<=nbit; ++i) {
  picture pict;
  add(pict,ta*pic);
  add(pict,tb*pic);
  add(pict,tc*pic);
  draw(pict,(0,0)--(0,1), (2*(i/nbit)^2)*bp+((1-i/nbit)*green+i/nbit*brown));
  pic=pict;
}

//Use the fern branch to construct... a fern branch
picture pict;
add(pict,ta*pic);
add(pict,tb*pic);

pair x=(0,1);
nbit=23;
for(int i=1; i<=nbit; ++i) {
  add(shift(x)*rotate(ac*i)*scale(rc^i)*pict);
  draw(tc^i*((0,0)--(0,1)), 2*(1.5-i/nbit)^2*bp+brown);
  x=tc*x;
}

shipout(bbox(3mm, 2mm+black, FillDraw(paleyellow)));
```

\newpage

# Circle

```{.asy im_fmt=eps}
settings.outformat="eps";
import graph;

size(0,0);
pair O=0;

defaultpen(linewidth(2mm));
draw(arc(O,2cm,0,60),.8red,BeginPenMargin);
draw(arc(O,2cm,60,120),.7blue,PenMargins);
draw(arc(O,2cm,120,360),.7green);

```

\newpage

# Circle 2

```{.asy im_fmt=png}
settings.outformat="png";
import geometry;
size(6cm);

// currentcoordsys=cartesiansystem((1,2),i=(1,0.5),j=(-0.5,.75));
// show(currentcoordsys, xpen=invisible);

point A=(-1,0);
point B=(3,-1);
point C=(0,1);

circle cle=circle(A,C,B);
draw(cle,linewidth(2mm));

draw(arc(cle,A,B), dotsize()+green);
draw(arc(cle,B,C), dotsize()+blue);
draw(arc(cle,C,A), dotsize()+red);

dot(Label("$A$", black), A, 1.5NW, white);
dot(Label("$B$", black), B, E, white);
dot(Label("$C$", black), C, NW, white);
```


\newpage

## 2D example (png)

```{.asy caption="Created by Asymptote"}
settings.outformat="png";
//settings.prc=false;
//settings.render=0;

import graph;
size(4inches,0);

real f1(real x) {return (1+x^2);} 
real f2(real x) {return (4-x);}
xaxis("$x$",LeftTicks,Arrow);
yaxis("$y$",RightTicks,Arrow);
draw("$y=1+x^2$",graph(f1,-2,1)); 
dot((1,f1(1)),UnFill);
draw("$y=4-x$",graph(f2,1,5),LeftSide,red,Arrow);
dot((1,f2(1)),red);
```

\newpage

## 3D example (png)

```asy
settings.outformat="png";  // im_fmt="png" by default

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

\newpage

# Documentation

## asy -h
```{.shebang im_out="stderr"}
#!/bin/bash
asy -h
```

## man page

```{.shebang im_out="stdout"}
#!/bin/bash
MANWIDTH=75 man asy | col -bx | iconv -t ascii//TRANSLIT
```
