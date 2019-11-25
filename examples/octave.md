```{.shebang im_out="stdout"}
#!/bin/bash
figlet -c -w 60 octave | boxes -d ian_jones -ph4v1 -i box
```

# [*Octave*](https://www.gnu.org/software/octave)

**Octave seems to suffer from a bug in libosmesa6**

Hints for using `Octave` as batch processor:

- `;` makes statements silent
- `figure(1, "visibility", "off")` prevents pop-up window
- `print(1, argv(){1});` prints to intended output filename
- octave will infer image type from output filename extension
- `imagine` calls `octave --no-gui -q <im_opt> <inpfile> <outfile>`, where
    + `<im_opt>` come from im_opt=".." in the fenced code blocks attributes
    + `<inpfile>` is `pd-images/hashed-name.octave` containing the code text
    + `<outfile>` is `pd-images/hashed-name.png` by default

## Sinus plot

```{.octave im_out="fcb,img" caption="Created by Octave"}
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

```{.octave im_out="fcb,img" caption="Created by Octave"}
figure('visible', 'off');

surf(peaks);
title("peaks");

print(1, argv(){1});
```

## Peaks contour

```{.octave im_out="fcb,img" caption="Created by Octave"}
figure(1, 'visible', 'off');

contourf(peaks);
title("peaks");

print(1, argv(){1});
```

## 3-D wave

```{.octave im_out="fcb,img" caption="Created by Octave"}
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

## Imagine

```imagine
octave
```

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
