---
imagine.protocol.im_out: stdout,fcb
...

```{.shebang im_out="stdout"}
#!/bin/bash
figlet -c -w 60 protocol | boxes -d ian_jones -ph4v1 -i box
```

```imagine
protocol
```

\newpage

# Local installation

```{.shebang im_out="stdout"}
#!/bin/bash
uname -o
uname -rv
echo "cat ~/installs/protocol/setup.py"
echo ""
cat ~/installs/protocol/setup.py
```

\newpage

# [*Protocol*](https://github.com/luismartingarcia/protocol)

## ip

```protocol
ip
```

\newpage

## tcp

```protocol
tcp
```

\newpage

## udp

```protocol
udp
```

\newpage

## Custom packet

and even custom layouts:

```{.protocol im_opt="--no-numbers"}
Source:16,TTL:8,Reserved:40
```

\newpage

# Documentation

## protocol -h

```{.shebang im_out="stdout"}
#!/bin/bash
protocol -h
```

## man page

There's no man page, but here are the supported protocols last seen on the
website:

```
  "ethernet"            : Ethernet
  "8021q"               : IEEE 802.1q
  "dot1q"               : IEEE 802.1q
  "tcp"                 : Transmission Control Protocol (TCP)
  "udp"                 : User Datagram Protocol (TCP)
  "ip"                  : Internet Protocol (IP), version 4.
  "ipv6"                : Internet Protocol (IP), version 6.
  "icmp"                : Internet Control Message Protocol (ICMP)
  "icmp-destination":   : ICMP Destination Unreachable
  "icmp-time"           : ICMP Time Exceeded
  "icmp-parameter"      : ICMP Parameter Problem
  "icmp-source"         : ICMP Source Quench
  "icmp-redirect"       : ICMP Redirect
  "icmp-echo"           : ICMP Echo Request/Reply
  "icmp-timestamp"      : ICMP Timestamp Request/Reply
  "icmp-information"    : ICMP Information Request/Reply
  "icmpv6"              : Internet Control Message Protocol for IPv6 (ICMPv6)
  "icmpv6-destination"  : ICMPv6 Destination Unreachable
  "icmpv6-big"          : ICMPv6 Packet Too Big
  "icmpv6-time"         : ICMPv6 Time Exceeded
  "icmpv6-parameter"    : ICMPv6 Parameter Problem
  "icmpv6-echo"         : ICMPv6 Echo Request/Reply
  "icmpv6-rsol"         : ICMPv6 Router Solicitation
  "icmpv6-radv"         : ICMPv6 Router Advertisement
  "icmpv6-nsol"         : ICMPv6 Neighbor Solicitation
  "icmpv6-nadv"         : ICMPv6 Neighbor Advertisement
  "icmpv6-redirect"     : ICMPv6 Redirect
```
