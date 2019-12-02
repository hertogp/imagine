---
imagine.figlet.im_out: stdout,fcb
...

```{.shebang im_out="stdout"}
#!/bin/bash
figlet -c -w 60 figlet | boxes -d ian_jones -ph4v1 -i box
```

```imagine
figlet
```

\newpage

# [*Figlet*](http://www.figlet.org)

## figlet

```{.figlet im_opt="-f slant" caption="Figlet"}
figlet
```

\newpage

## hello, world!

```figlet
hello, world!
```

\newpage

## Figlet again.

```{.figlet im_opt="-f bubble"}
Figlet again
```

\newpage

# Documentation

## figlet -h

```{.shebang im_out="stdout"}
#!/bin/bash
figlet -h 2>&1 | grep -iv invalid
```

\newpage

## man page

```{.shebang im_out="stdout"}
#!/bin/bash
MANWIDTH=75 man figlet | col -bx | iconv -t ascii//TRANSLIT
```
