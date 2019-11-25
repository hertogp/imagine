```{.shebang im_out="stdout"}
#!/bin/bash
figlet -c -w 65 chartdirector | boxes -d ian_jones -ph4v1 -i box
```

# [*ChartDirector*](http://www.advsofteng.com/index.html)

The yellow bars below the images created by ChartDirector are because this
is the demo-version without a license.

Notes:

- pip3 search pychartdir came up dry ..., so
- download appropiate zip-file @ https://www.advsofteng.com/download.html
- `cd download-dir`
- `tar xvzf chardir_...._.tar.gz`
- `cd ChartDirector`
- read documenation -> xdg-open doc/cdpython.htm
- `mkdir -p ~/lib/python`
- `cp -R lib/* ~/lib/python`
- add:
    + `import os, sys`
    + `import sys`
    + `sys.path.insert(0, os.environ["HOME"] + "~/lib/python")`

    to the scripts, or update your python's PATH to find modules


## Line Chart

```{.shebang im_out="fcb,img" caption="Created by ChartDirector"}
#!/usr/bin/python
import os, sys
sys.path.insert(0, os.environ["HOME"] + "/lib/python")
from pychartdir import *

data0 = [42, 49, NoValue, 38, 64, 56, 29, 41, 44, 57]
data1 = [65, 75, 47, 34, 42, 49, 73, NoValue, 90, 69, 66, 78]
data2 = [NoValue, NoValue, 25, 28, 38, 20, 22, NoValue, 25, 33, 30, 24]
labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul",
          "Aug", "Sep", "Oct", "Nov", "Dec"]
c = XYChart(600, 360, brushedSilverColor(), Transparent, 2)
c.setRoundedFrame()
title = c.addTitle("Product Line Global Revenue", "timesbi.ttf", 18)
title.setMargin2(0, 0, 6, 6)
c.addLine(10, title.getHeight(), c.getWidth() - 11,
          title.getHeight(), LineColor)
legendBox = c.addLegend(c.getWidth() / 2, title.getHeight(),
                        0, "arialbd.ttf", 10)
legendBox.setAlignment(TopCenter)
legendBox.setBackground(Transparent, Transparent)
c.setPlotArea(70, 75, 460, 240, -1, -1, Transparent, 0x000000, -1)
c.xAxis().setLabels(labels)
c.syncYAxis()
c.yAxis().setTickDensity(30)
c.xAxis().setColors(Transparent)
c.yAxis().setColors(Transparent)
c.yAxis2().setColors(Transparent)
c.xAxis().setMargin(15, 15)
c.xAxis().setLabelStyle("arialbd.ttf", 8)
c.yAxis().setLabelStyle("arialbd.ttf", 8)
c.yAxis2().setLabelStyle("arialbd.ttf", 8)
c.yAxis().setTitle("Revenue in USD millions", "arialbi.ttf", 10)
c.yAxis2().setTitle("Revenue in USD millions", "arialbi.ttf", 10)
layer0 = c.addLineLayer2()
layer0.addDataSet(data0, 0xff0000, "Quantum Computer").setDataSymbol(GlassSphere2Shape, 11)
layer0.setLineWidth(3)
layer1 = c.addLineLayer2()
layer1.addDataSet(data1, 0x00ff00, "Atom Synthesizer").setDataSymbol(GlassSphere2Shape, 11)
layer1.setLineWidth(3)
layer1.setGapColor(c.dashLineColor(0x00ff00))
layer2 = c.addLineLayer2()
layer2.addDataSet(data2, 0xff6600, "Proton Cannon").setDataSymbol(GlassSphere2Shape, 11)
layer2.setLineWidth(3)
layer2.setGapColor(SameAsMainColor)
c.layoutLegend()
c.packPlotArea(15, legendBox.getTopY() + legendBox.getHeight(), c.getWidth() - 16, c.getHeight(
    ) - 25)

c.makeChart(sys.argv[-1])
```

## Surface

```{.shebang im_out="fcb,img" caption="Created by ChartDirector"}
#!/usr/bin/python
import os, sys
sys.path.insert(0, os.environ["HOME"] + "/lib/python")
from pychartdir import *

dataX = [0.5, 1.9, 4.9, 1.0, 8.9, 9.8, 5.9, 2.9, 6.8, 9.0,
         0.0, 8.9, 1.9, 4.8, 2.4, 3.4, 7.9, 7.5, 4.8, 7.5,
         9.5, 0.4, 8.9, 0.9, 5.4, 9.4, 2.9, 8.9, 0.9, 8.9,
         10.0, 1.0, 6.8, 3.8, 9.0, 5.3, 6.4, 4.9, 4.5, 2.0,
         5.4, 0.0, 10.0, 3.9, 5.4, 5.9, 5.8, 0.3, 4.4, 8.3]
dataY = [3.3, 3.0, 0.7, 1.0, 9.3, 4.5, 8.4, 0.1, 0.8, 0.1,
         9.3, 1.8, 4.3, 1.3, 2.3, 5.4, 6.9, 9.0, 9.8, 7.5,
         1.8, 1.4, 4.5, 7.8, 3.8, 4.0, 2.9, 2.4, 3.9, 2.9,
         2.3, 9.3, 2.0, 3.4, 4.8, 2.3, 3.4, 2.3, 1.5, 7.8,
         4.5, 0.9, 6.3, 2.4, 6.9, 2.8, 1.3, 2.9, 6.4, 6.3]
dataZ = [6.6, 12.5, 7.4, 6.2, 9.6, 13.6, 19.9, 2.2, 6.9,
         3.4, 8.7, 8.4, 7.8, 8.0, 9.4, 11.9, 9.6, 15.7,
         12.0, 13.3, 9.6, 6.4, 9.0, 6.9, 4.6, 9.7, 10.6,
         9.2, 7.0, 6.9, 9.7, 8.6, 8.0, 13.6, 13.2, 5.9,
         9.0, 3.2, 8.3, 9.7, 8.2, 6.1, 8.7, 5.6, 14.9,
         9.8, 9.3, 5.1, 10.8, 9.8]
c = SurfaceChart(680, 550, brushedSilverColor(), 0x888888)
c.setRoundedFrame(0xffffff, 20, 0, 20, 0)
title = c.addTitle("Surface Created Using Scattered Data Points", "timesi.ttf", 20)
title.setMargin2(0, 0, 8, 8)
c.addLine(10, title.getHeight(), c.getWidth() - 10, title.getHeight(), 0x000000, 2)
c.setPlotRegion(290, 235, 360, 360, 180)
c.setViewAngle(45, -45)
c.setPerspective(30)
c.setData(dataX, dataY, dataZ)
cAxis = c.setColorAxis(660, 80, TopRight, 200, Right)
cAxis.setTitle("Z Title Placeholder", "arialbd.ttf", 12)
cAxis.setBoundingBox(0xeeeeee, 0x888888)
cAxis.setRoundedCorners(10, 0, 10, 0)
c.setSurfaceAxisGrid(0xcc000000)
c.setContourColor(0x80ffffff)
c.setWallColor(0x000000)
c.setWallGrid(0xffffff, 0xffffff, 0xffffff, 0x888888, 0x888888, 0x888888)
c.setWallThickness(0, 0, 0)
c.setWallVisibility(1, 0, 0)
c.xAxis().setTitle("X Title\nPlaceholder", "arialbd.ttf", 12)
c.yAxis().setTitle("Y Title\nPlaceholder", "arialbd.ttf", 12)
c.makeChart(sys.argv[-1])
```

## Gauge

```{.shebang im_out="fcb,img" caption="Created by ChartDirector"}
#!/usr/bin/python
import os, sys
sys.path.insert(0, os.environ["HOME"] + "/lib/python")
from pychartdir import *

value = 54
colorList = [0x0033dd, 0xaaaa00]
mainColor = colorList[1]
size = 300
outerRadius = int(size / 2 - 2)
scaleRadius = int(outerRadius * 92 / 100)
colorScaleRadius = int(scaleRadius * 43 / 100)
colorScaleWidth = int(scaleRadius * 10 / 100)
tickLength = int(scaleRadius * 10 / 100)
tickWidth = int(scaleRadius * 1 / 100 + 1)
fontSize = int(scaleRadius * 13 / 100)
readOutRadiusRatio = 0.333333333333
readOutFontSize = int(scaleRadius * 24 / 100)
m = AngularMeter(size, size, 0x000000)
m.setColor(TextColor, 0xffffff)
m.setColor(LineColor, 0xffffff)
m.setMeter(size / 2, size / 2, scaleRadius, -180, 90)
bgGradient = [0, mainColor, 0.5, m.adjustBrightness(mainColor, 0.75), 1, m.adjustBrightness(
    mainColor, 0.15)]
m.addRing(0, outerRadius, m.relativeRadialGradient(bgGradient, outerRadius * 0.66))
neonGradient = [0.89, Transparent, 1, mainColor, 1.07, Transparent]
m.addRing(int(scaleRadius * 85 / 100), outerRadius, m.relativeRadialGradient(neonGradient))
m.addRing(scaleRadius, int(scaleRadius + scaleRadius / 80), m.adjustBrightness(mainColor, 2))
m.setScale(0, 100, 10, 5, 1)
m.setLabelStyle("ariali.ttf", fontSize)
m.setTickLength( - tickLength,  - int(tickLength * 80 / 100),  - int(tickLength * 60 / 100))
m.setLineWidth(0, tickWidth, int((tickWidth + 1) / 2), int((tickWidth + 1) / 2))
smoothColorScale = [0, 0x0000ff, 25, 0x0088ff, 50, 0x00ff00, 75, 0xdddd00, 100, 0xff0000]
highColorScale = [70, Transparent, 100, 0xff0000]
m.addColorScale(highColorScale)
m.addPointer2(value, 0xff0000, -1, TriangularPointer2, 0.4, 0.6, 6)
m.setCap2(Transparent, m.adjustBrightness(mainColor, 0.3), m.adjustBrightness(mainColor, 1.5),
    0.75, 0, readOutRadiusRatio, 0.015)
m.addText(size / 2, size / 2, m.formatValue(value, "{value|0}"), "ariali.ttf", readOutFontSize,
    m.adjustBrightness(mainColor, 2.5), Center).setMargin(0)
m.addGlare(scaleRadius)
m.makeChart(sys.argv[-1])
```


# Documentation

See their website or one of the many demo scripts that come with the download.


