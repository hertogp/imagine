---
imagine.shebangvia.im_log: 4
imagine.shebangvia.im_out: stdout,fcb
...

# Standard unicorn

```shebangvia
#!/bin/bash
cat << 'EOF' | boxes -d peek -ph4v1
Never agree with stupid people,
they'll drag you down to their level
and then beat you with experience.
                      -- Mark Twain
EOF
```


# Via Nice Unicorn

```{.shebangvia im_prg="nice -n 10"}
#!/bin/bash
cat << 'EOF' | boxes -d peek -ph4v1
Never agree with stupid people,
they'll drag you down to their level
and then beat you with experience.
                      -- Mark Twain
EOF
```
