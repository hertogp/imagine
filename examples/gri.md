```{.shebang im_out="stdout"}
#!/bin/bash
figlet -c -w 60 gri | boxes -d ian_jones -ph4v1 -i box
```

```imagine
gri
```

\newpage

# [*GRI*](http://gri.sf.net)

## Single plot

With the following in `gri-01.dat`

```
1  8 11  9
2 22 21 20
3 11 10  9
4 20 15 10
```

plot the first two columns like so:

```gri
open dta/gri-01.dat
read columns x y
draw curve
draw title "http://gri.sf.net"
```

\newpage

## Multiple curves

```gri
`draw curves' \xname \y1name ...'`
Draw multiple y columns versus an x column.  Assumes
that the datafile is open, and that x is in the first
column, with the y values in one or more following 
columns.


The number of columns is figured out from the options, 
as is the name of the x-axis, and the labels to be 
used on each of the y curves.
{
  # NB. the 3 below lets us skip the words 'draw' 
  # and 'curves', and the name of the x-column.
  .num_of_y_columns. = {rpn wordc 3 -}
  if {rpn .num_of_y_columns. 1 >}
    show "ERROR: 'draw curves' needs at least 1 y column!"
    quit
  end if


  set x name {rpn 2 wordv}
  set y name ""


  # Loop through the columns.
  .col. = 0
  while {rpn .num_of_y_columns. .col. <}
    # The x-values will be in column 1, with y-values
    # in columns 2, 3, ..., of the file.
    .ycol. = {rpn .col. 2 +}
    rewind
    read columns x=1 y=.ycol.
    # At this point, you may want to change line thickness,
    # thickness, color, dash-type, etc.  For illustration,
    # let's set dash type to the column number.
    set dash .col.
    draw curve
    draw label for last curve {rpn .col. 3 + wordv}
    .col. += 1
  end while
}


open dta/gri-01.dat
draw curves time y1 y2 y3 y4
```

\newpage

# Documentation

## gri -h

```{.shebang im_out="stdout"}
#!/bin/bash
gri -h
```

\newpage

## man page

```{.shebang im_out="stdout"}
#!/bin/bash
MANWIDTH=75 man gri | col -bx | iconv -t ascii//TRANSLIT
```
