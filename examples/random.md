---
imagine.shebang.im_out: stdout,fcb
...


# Unwise unicorn

```shebang
#!/bin/bash
cat $0 | tail -n +3 | boxes -d peek -p h4v1
# Never agree with stupid people,
# they'll drag you down to their level
# and then beat you with experience.
#                      -- Mark Twain
```

# Wise unicorn

```{.shebang im_prg="nice -n 10"}
#!/bin/bash
cat << 'EOF' | boxes -d peek -ph4v1
Never agree with stupid people,
they'll drag you down to their level
and then beat you with experience.
                      -- Mark Twain
EOF
```

# Bewildered unicorn

```shebang
#!/usr/bin/env -S nice -n 10 /bin/bash
cat << 'EOF' | boxes -d peek -ph4v1
Never agree with stupid people,
they'll drag you down to their level
and then beat you with experience.
                      -- Mark Twain
EOF
```

# Unbewildered unicorn

```{.shebang im_prg="nice" im_opt="-n 10"}
cat << 'EOF' | boxes -d peek -ph4v1
Never agree with stupid people,
they'll drag you down to their level
and then beat you with experience.
                      -- Mark Twain
EOF
```
