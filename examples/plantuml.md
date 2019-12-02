---
imagine.plantuml.im_opt: "width=60%"
imagine.plantuml.im_fmt: svg
...

```{.shebang im_out="stdout"}
#!/bin/bash
figlet -c -w 60 plantuml | boxes -d ian_jones -ph4v1 -i box
```

```imagine
plantuml
```

Notes:

- metadata sets plantuml's default output format to `svg`
- local install doesn't seem to support mindmap  
  see `plantuml -language | grep -i @`

\newpage

# Local installation

```{.shebang im_out="stdout"}
#!/bin/bash
uname -o
uname -rv
echo
apt show plantuml
```

\newpage

# Examples

## Sequence diagram (svg)

```plantuml
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

\newpage

## Class diagrams (svg)

```plantuml
@startuml
Class01 <|-- Class02
Class03 *-- Class04
Class05 o-- Class06
Class07 .. Class08
Class09 -- Class10
@enduml
```

\newpage

## Notes (svg)

```plantuml
@startuml
[*] --> NotShooting
state "Not Shooting State" as NotShooting {
state "Idle mode" as Idle
state "Configuring mode" as Configuring
[*] --> Idle
Idle --> Configuring : EvConfig
Configuring --> Idle : EvConfig
}
note right of NotShooting : This is a note on a composite state
@enduml
```

\newpage

# Documentation

## plantuml -h

```{.shebang im_out="stdout"}
#!/bin/bash
plantuml -h
```

\newpage

## man page

```{.shebang im_out="stdout"}
#!/bin/bash
MANWIDTH=75 man plantuml | col -bx | iconv -t ascii//TRANSLIT
```
