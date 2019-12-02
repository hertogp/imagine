```{.shebang im_out="stdout"}
#!/bin/bash
figlet -c -w 60 octave | boxes -d ian_jones -ph4v1 -i box
```

```imagine
octave
```

Notes

- `;` makes statements silent
- `figure(1, "visibility", "off")` prevents pop-up window
- `print(1, argv(){1});` prints to intended output filename
- octave will infer image type from output filename extension
- `imagine` calls `octave --no-gui -q <im_opt> <inpfile> <outfile>`, where
- *Octave seems to suffer from a bug in localhost's libosmesa6*

\newpage

# [*Octave*](https://www.gnu.org/software/octave)

## Sinus plot

```octave
outname = argv(){1}
figure(1, 'visible', 'off');

x = 0:0.01:2*pi;
a = sin(x);
b = cos(2*x);
c = sin(4*x);
d = 2*sin(3*x);
plot(x,a,x,b,x,c,x,d, "linewidth", 2);
set(gca, "xlim", [0,2*pi], "fontsize", 15);
title("sinusoids");

print(1, outname, '-dpng');
```

```octave
outname = argv(){1}
figure(1, "visible", "off");

x=linspace(-2,2,50);
y=linspace(-2,2,50);
[xx,yy]=meshgrid(x,y);
meshc(xx,yy,4-(xx.^2+yy.^2))

print(1, outname, '-dpng');
```

## Peaks surface

```octave
figure('visible', 'off');

surf(peaks);
title("peaks");

print(1, argv(){1});
```

## Peaks contour

```octave
figure(1, 'visible', 'off');

contourf(peaks);
title("peaks");

print(1, argv(){1});
```

## 3-D wave

```octave
outname = argv(){1}
figure(1, 'visible', 'off');

x = 0:0.1:2*pi;
y = 0:0.1:2*pi;
z = sin(x)' * sin(y);
mesh(x, y, z); 
xlabel("x-axis");
ylabel("y-axis");
zlabel("z-axis");
title("3-D waves");

print(1, outname, '-dpng');
```

\newpage

# Documentation

## octave -h

```{.shebang im_out="stdout"}
#!/bin/bash
octave -h
```

## man page

```{.shebang im_out="stdout"}
#!/bin/bash
MANWIDTH=75 man octave | col -bx | iconv -t ascii//TRANSLIT
```
