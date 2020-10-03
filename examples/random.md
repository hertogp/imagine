---
imagine.shebang.im_log: 4
imagine.shebang.im_out: stdout,fcb
...


# Unwise unicorn

```shebang
#!/bin/bash
cat $0 | tail -n +3 | boxes -d peek -p h4v1
Never agree with stupid people,
they'll drag you down to their level
and then beat you with experience.
                      -- Mark Twain
```

# Wise unicorn

```shebang
#!/bin/bash
cat << 'EOF' | boxes -d peek -ph4v1
Never agree with stupid people,
they'll drag you down to their level
and then beat you with experience.
                      -- Mark Twain
EOF
```
