#!/usr/bin/awk -f
BEGIN {
    local_link = "pd-images"
    github_link = "https://raw.githubusercontent.com/hertogp/imagine/master/pd-images"
}

# fix unknown 'roles'
/^.. code::/ {
    print ".. code::"
    next
}
# fix image links
/image::\s+pd-images\// {
    sub( local_link, github_link, $0)
    print $0
    next
}

# ok, this one is fine
{ print }
