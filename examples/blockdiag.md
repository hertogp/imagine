```{.shebang im_out="stdout"}
#!/bin/bash
figlet -c -w 60 blockdiag | boxes -d ian_jones -ph4v1 -i box
```

# [*blockdiag*](http://blockdiag.com)


## blockdiag command

```{.blockdiag im_prg=blockdiag im_out="fcb,img" width=100% caption="Created by Blockdiag"}
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


## seqdiag

```{.seqdiag im_out="fcb,img" width=80% height=50% caption="Created by seqdiag"}
{
browser -> webserver [label = "GET /index.html"];
browser <-- webserver;
browser -> webserver [label = "POST /blog/comment"];
webserver -> database [label = "INSERT comment"];
webserver <- database;
browser <- webserver;
}

```

## nwdiag

```{.nwdiag im_out="fcb,img" caption="Created by nwdiag"}
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

## actdiag

```{.actdiag im_out="fcb,img" height=60% caption="Created by actdiag"}
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

## rackdiag


```{.rackdiag im_out="fcb,img" height=80% caption="Created by rackdiag"}
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


# Documentation

```imagine
blockdiag
```

## blockdiag -h

```{.shebang im_out="stdout"}
#!/bin/bash
blockdiag -h
```

## seqdiag -h

```{.shebang im_out="stdout"}
#!/bin/bash
seqdiag -h
```

## actdiag -h

```{.shebang im_out="stdout"}
#!/bin/bash
actiag -h
```

## rackdiag

```{.shebang im_out="stdout"}
#!/bin/bash
rackdiag -h
```

