```{.shebang im_out="stdout"}
#!/bin/bash
figlet -c -w 60 boxes | boxes -d ian_jones -p h4v1 -i box
```

# [boxes](http://boxes.thomasjensen.com)

```{.boxes im_opt="-h"}
```

# Examples

## boxes class

```{.boxes im_opt="-d peek -p h4v1" im_out="fcb,stdout"}
I seem to have got myself boxed in!
```

## shebang

Another method is to use the `shebang` class

```{.shebang im_out="fcb,stdout"}
#!/bin/bash
# I seem to have got myself boxed in!
cat $0 | boxes -d peek -p h4v1
```


# Documentation

## Imagine

```imagine
boxes
```

## man page

```{.shebang im_out="fcb,stdout"}
#!/bin/bash
MANWIDTH=75 man boxes | col -bx | iconv -t ascii//TRANSLIT
```

## boxes -h

```{.boxes im_opt="-h"}
boxes
```

## boxes -l

```{.boxes im_opt="-l"}
boxes
```


