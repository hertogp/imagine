```{.shebang im_out="stdout"}
#!/bin/bash
figlet -c -w 60 figlet | boxes -d ian_jones -ph4v1 -i box
```

# [*Figlet*](http://www.figlet.org)

## figlet

```{#FIGLET .figlet im_opt="-f slant" im_out="fcb,stdout" caption="Figlet"}
figlet
```

\newpage

## hello world.

```{.figlet im_out="fcb,stdout"}
hello, world!
```

## Figlet again.

```{.figlet im_opt="-f bubble" im_out="fcb,stdout"}
Figlet again
```

\newpage

# Documentation

## Imagine

```imagine
figlet
```

## figlet -h

```{.shebang im_out="stdout"}
#!/bin/bash
figlet -h 2>&1 | grep -iv invalid
```

## man page

```{.shebang im_out="stdout"}
#!/bin/bash
MANWIDTH=75 man figlet | col -bx | iconv -t ascii//TRANSLIT
```
