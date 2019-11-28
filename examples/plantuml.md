---
pandoc_imagine:
    plantuml.im_out: img,fcb
    plantuml.im_opt: "width=60%"
    shebang.im_out: stdout
...

```shebang
#!/bin/bash
figlet -c -w 60 plantuml | boxes -d ian_jones -ph4v1 -i box
```

# [*Plantuml*](http://plantuml.com/)

## sequence diagrams

```{.plantuml width=60% caption="Created by plantuml code:"}
@startuml
autonumber "<b>[000]"
Bob -> Alice : Authentication Request
Bob <- Alice : Authentication Response

autonumber 15 "<b>(<u>##</u>)"
Bob -> Alice : Another authentication Request
Bob <- Alice : Another authentication Response

autonumber 40 10 "<font color=red><b>Message 0  "
Bob -> Alice : Yet another authentication Request
Bob <- Alice : Yet another authentication Response

@enduml
```

## class diagrams

```{.plantuml width=60% caption="Created by plantuml"}
@startuml
Class01 <|-- Class02
Class03 *-- Class04
Class05 o-- Class06
Class07 .. Class08
Class09 -- Class10
@enduml
```

## larger plantuml

```{.plantuml im_out="fcb,img" caption="Created by plantuml"}
@startuml
scale 580*690
title Servlet Container
(*) --> "ClickServlet.handleRequest()"
--> "new Page"
if "Page.onSecurityCheck" then
->[true] "Page.onInit()"
if "isForward?" then
->[no] "Process controls"
if "continue processing?" then
-->[yes] ===RENDERING===
else
-->[no] ===REDIRECT_CHECK===
endif
else
-->[yes] ===RENDERING===
endif
if "is Post?" then
-->[yes] "Page.onPost()"
--> "Page.onRender()" as render
--> ===REDIRECT_CHECK===
else
-->[no] "Page.onGet()"
--> render
endif
else
-->[false] ===REDIRECT_CHECK===
endif
if "Do redirect?" then
->[yes] "redirect request"
--> ==BEFORE_DESTROY===
else
if "Do Forward?" then
-left->[yes] "Forward request"
--> ==BEFORE_DESTROY===
else
-right->[no] "Render page template"
--> ==BEFORE_DESTROY===
endif
endif
--> "Page.onDestroy()"
-->(*)
@enduml
```

\newpage

# Documentation

## Imagine

```imagine
plantuml
```

## plantuml -h

```{.shebang im_out="stdout"}
#!/bin/bash
plantuml -h
```

## man page

```{.shebang im_out="stdout"}
#!/bin/bash
MANWIDTH=75 man plantuml | col -bx | iconv -t ascii//TRANSLIT
```
