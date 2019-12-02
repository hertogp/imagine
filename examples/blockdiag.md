---
imagine.actdiag.im_fmt: svg
imagine.blockdiag.im_fmt: svg
imagine.nwdiag.im_fmt: svg
imagine.packetdiag.im_fmt: svg
imagine.rackdiag.im_fmt: svg
imagine.seqdiag.im_fmt: svg
...

```{.shebang im_out="stdout"}
#!/bin/bash
figlet -c -w 60 blockdiag | boxes -d ian_jones -ph4v1 -i box
```

```imagine
blockdiag
nwdiag
```

\newpage

# [*blockdiag*](http://blockdiag.com) examples

## blockdiag

```{.blockdiag width=100% caption="Created by Blockdiag"}
blockdiag {
// standard node shapes
box [shape = "box"];
roundedbox [shape = "roundedbox"];
diamond [shape = "diamond"];
ellipse [shape = "ellipse"];
note [shape = "note"];
cloud [shape = "cloud"];
mail [shape = "mail"];
beginpoint [shape = "beginpoint"];
endpoint [shape = "endpoint"];
minidiamond [shape = "minidiamond"];
actor [shape = "actor"];
dots [shape = "dots"];
box -> roundedbox -> diamond -> ellipse;
cloud -> note -> mail -> actor;
minidiamond -> beginpoint -> endpoint -> dots;
// node shapes for flowcharts
condition [shape = "flowchart.condition"];
database [shape = "flowchart.database"];
input [shape = "flowchart.input"];
loopin [shape = "flowchart.loopin"];
loopout [shape = "flowchart.loopout"];
terminator [shape = "flowchart.terminator"];
condition -> database -> terminator -> input;
loopin -> loopout;
}
```

\newpage

## seqdiag

```{.seqdiag width=80% height=50% caption="Created by seqdiag"}
{
browser -> webserver [label = "GET /index.html"];
browser <-- webserver;
browser -> webserver [label = "POST /blog/comment"];
webserver -> database [label = "INSERT comment"];
webserver <- database;
browser <- webserver;
}

```

\newpage

## nwdiag

```{.nwdiag caption="Created by nwdiag"}
{
  network dmz {
      address = "210.x.x.x/24"

      web01 [address = "210.x.x.1"];
      web02 [address = "210.x.x.2"];
  }
  network internal {
      address = "172.x.x.x/24";

      web01 [address = "172.x.x.1"];
      web02 [address = "172.x.x.2"];
      db01;
      db02;
  }
}
```

\newpage

## actdiag

```{.actdiag height=60% caption="Created by actdiag"}
{
   A -> B -> C -> D;

  lane foo {
    A; B;
  }
  lane bar {
    C; D;
  }
}
```

\newpage

## rackdiag

```{.rackdiag height=70% caption="Created by rackdiag"}
{
  // define 1st rack
  rack {
    16U;

    // define rack items
    1: UPS [2U];
    3: DB Server
    4: Web Server
    5: Web Server
    6: Web Server
    7: Load Balancer
    8: L3 Switch
  }

  // define 2nd rack
  rack {
    12U;

    // define rack items
    1: UPS [2U];
    3: DB Server
    4: Web Server
    5: Web Server
    6: Web Server
    7: Load Balancer
    8: L3 Switch
  }
}
```

\newpage

# Documentation

## actdiag -h

```{.shebang im_out="stdout"}
#!/bin/bash
actdiag -h
```

## blockdiag -h

```{.shebang im_out="stdout"}
#!/bin/bash
blockdiag -h
```

## nwdiag -h
```{.shebang im_out="stdout"}
#!/bin/bash
nwdiag -h
```

## seqdiag -h

```{.shebang im_out="stdout"}
#!/bin/bash
seqdiag -h
```

## rackdiag -h

```{.shebang im_out="stdout"}
#!/bin/bash
rackdiag -h
```

