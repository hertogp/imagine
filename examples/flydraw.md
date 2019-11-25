```{.shebang im_out="stdout"}
#!/bin/bash
figlet -c -w 60 flydraw | boxes -d ian_jones -ph4v1 -i box
```


# [*Flydraw*](http://manpages.ubuntu.com/manpages/precise/man1/flydraw.1.html)

Notes:

- seems to only want to produce GIF, despite the manual's mention of PNG.
- only reads from stdin

## frenchman

```{.flydraw im_out="fcb,img"}
comment : from KhanAcademy
new 200,200
comment ears
fellipse 24, 100, 30, 40,255, 211, 178
fellipse 174, 100, 30, 40,255, 211, 178
ellipse 24, 100, 30, 40,black
ellipse 174, 100, 30, 40,black
comment face
fellipse 100, 100, 150, 150,255, 211, 178
ellipse 100, 100, 150, 150,black
comment nose
ellipse 100, 128, 17, 10,black
comment beret
fellipse 125, 25, 20, 20,red
fellipse 100, 45, 142, 50, red
comment mouth
fellipse 100, 152, 32, 10,red
linewidth 16
point 63, 115,black
point 135, 115 ,black
linewidth 8
line 80, 142, 96, 137, black
line 120, 142, 104, 137,black
```

## hexagons

```{.flydraw im_out="fcb,img"}
comment x=horizontal, x=0 is left
comment y=vertical,   y=0 is top
new 300,300
x0=150
y0=150
r=100
t1=0
t2=t1+2*pi
linewidth=1
plotstep 8
trange t1,t2
plot red,r*cos(t)+x0,r*sin(t)+y0
plot green,r*0.5*cos(t)+x0,r*0.5*sin(t)+y0
```

## plotting a function

```{.flydraw im_out="fcb,img"}
w=360
h=150
new w,h
linewidth=1
plotstep=9000
r=-2+h/2
y0=h/2
plot red,y0-r*sin(2*pi*x/w)
linewidth=2
rect 1,1, w-1,h-1, black
line 0,y0,w,y0, black
text green,3,h-16,normal,"flydraw"
```

# Documentation

## Imagine

```imagine
flydraw
```

## flydraw -h

```{.shebang im_out="stdout"}
#!/bin/bash
flydraw -h
```

## man page

```{.shebang im_out="stdout"}
#!/bin/bash
MANWIDTH=75 man flydraw | col -bx | iconv -t ascii//TRANSLIT
```
