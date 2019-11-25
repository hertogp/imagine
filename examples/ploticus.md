```{.shebang im_out="stdout"}
#!/bin/bash
figlet -c -w 60 ploticus | boxes -d ian_jones -ph4v1 -i box
```

# [*Ploticus*](http://ploticus.sourceforge.net/doc/welcome.html)

## prefab

Ploticus scripts are pretty verbose, it also has a `prefab` method of quickly
creating a graphic from a data-file, but that is not supported at the moment.


## Curves script

```{.ploticus im_out="fcb,img" caption="Created by Ploticus"}
#proc getdata
  data:
  0 1
  1 4
  2 2
  3 5
  4 7 
  5 10
  6 7
  7 8
  8 4
  9 8
  10 7
  11 3

#proc areadef
  rectangle: 1 1 4 3
  xrange: 0 12
  yrange: 0 12
  xaxis.stubs: inc
  yaxis.stubs: inc

#proc lineplot
  xfield: 1
  yfield: 2
  pointsymbol: radius=0.03 shape=square style=filled
  linedetails: color=gray(0.8) width=0.5
  legendlabel: Raw data points
  legendsampletype: line+symbol

#proc curvefit
  xfield: 1
  yfield: 2
  curvetype: movingavg
  order: 5
  linedetails: color=blue width=0.5
  legendlabel: Moving average (5 points)

#proc curvefit
  xfield: 1
  yfield: 2
  curvetype: regression
  linedetails: color=green width=0.5
  legendlabel: Linear regression

#proc curvefit
  xfield: 1
  yfield: 2
  curvetype: bspline
  order: 5
  linedetails: color=red width=0.5
  legendlabel: Bspline, order=5

#proc curvefit
  xfield: 1
  yfield: 2
  curvetype: average
  order: 5
  linedetails: color=black width=0.5
  legendlabel: Average (5 points)

#proc curvefit
  xfield: 1
  yfield: 2
  curvetype: interpolated
  linedetails: color=orange width=0.5 
  legendlabel: Interpolated

#proc legend
  location: max+0.5 max

```

## Heatmap (script)

```{.ploticus im_out="fcb,img" caption="Created by Ploticus"}
#set SYM = "radius=0.08 shape=square style=filled"
#setifnotgiven CGI = "http://ploticus.sourceforge.net/cgi-bin/showcgiargs"


// read in the SNP map data file..
#proc getdata
file: dta/snpmap.dat
fieldnameheader: yes

// group into bins 4 cM wide..
filter:
   ##set A = $numgroup( @@2, 4, mid )
   @@1 @@A

// set up the plotting area
#proc areadef
rectangle: 1 1 6 3
areacolor: gray(0.2)
yscaletype: categories
clickmapurl: @CGI?chrom=@@YVAL&cM=@@XVAL
ycategories: 
	1
	2
	3
	4
	5
	6
	7
	X
	
yaxis.stubs: usecategories
// yaxis.stubdetails: adjust=0.2,0
//yaxis.stubslide: 0.08
yaxis.label: chromosome
yaxis.axisline: no
yaxis.tics: no
yaxis.clickmap: xygrid

xrange: -3 120
xaxis.label: position (cM)
xaxis.axisline: no
xaxis.tics: no
xaxis.clickmap: xygrid
xaxis.stubs: inc 10
xaxis.stubrange: 0
// xaxis.stubdetails: adjust=0,0.15

// set up legend for color gradients..
#proc legendentry
sampletype: color
details: yellow 
label: >20
tag: 21

#proc legendentry
sampletype: color
details: orange 
label: 11-20
tag: 11 
  
#proc legendentry
sampletype: color
details: red 
label: 6 - 10
tag: 6

#proc legendentry
sampletype: color
details: lightpurple 
label: 1 - 5
tag: 1

#proc legendentry
sampletype: color
details: gray(0.2)
label: 0
tag: 0
 

// use proc scatterplot to count # of instances and pick appropriate color from legend..
#proc scatterplot
yfield: chr
xfield: cM
cluster: yes
dupsleg: yes
rectangle: 4 1 outline
  

// display legend..
#proc legend
location: max+0.7 min+0.8
textdetails: size=6

```

\newpage

# Documentation

## Imagine

```imagine
ploticus
```

## ploticus usage

```{.shebang im_out="stdout"}
#!/bin/bash
ploticus
```

## man page

```{.shebang im_out="stdout"}
#!/bin/bash
MANWIDTH=75 man ploticus | col -bx | iconv -t ascii//TRANSLIT
```
