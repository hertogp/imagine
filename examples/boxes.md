---
imagine.boxes.im_opt: -d peek -p h4v1
imagine.boxes.im_out: stdout, fcb
imagine.shebang.im_out: stdout,fcb
...

```{.shebang im_out="stdout"}
#!/bin/bash
figlet -c -w 60 boxes | boxes -d ian_jones -p h4v1 -i box
```

# Imagine

```imagine
boxes
```

\newpage

# Local installation

```{.shebang im_out="stdout"}
#!/bin/bash
uname -o
uname -rv
echo
apt show boxes
```

\newpage

# Examples

## boxes class

```boxes
I seem to have got myself boxed in!
```

\newpage

## shebang

Another method is to use the `shebang` class

```shebang
#!/bin/bash
# I seem to have got myself boxed in!
cat $0 | boxes -d peek -p h4v1
```

\newpage

## Wise unicorn

```{.boxes im_opt="-d unicornsay"}
Never argue with stupid people,
they'll drag you down to their level
and then beat you with experience.
                      -- Mark Twain
```

\newpage

# Documentation

## boxes -h

```{.boxes im_opt="-h" im_out="stdout"}
boxes
```

\newpage

## boxes -l

```{.boxes im_opt="-l" im_out="stdout"}
boxes
```

\newpage

## man page

```{.shebang im_out="stdout"}
#!/bin/bash
MANWIDTH=75 man boxes | col -bx | iconv -t ascii//TRANSLIT
```

