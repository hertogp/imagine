---
imagine.shebang.im_out: stdout,fcb
imagine.im_log: 4
...

# Nice unicorn

```{.shebang im_prg="nice -n 10"}
#!/bin/bash
cat << 'EOF' | boxes -d peek -ph4v1
Never agree with stupid people,
they'll drag you down to their level
and then beat you with experience.
                      -- Mark Twain
EOF
```
