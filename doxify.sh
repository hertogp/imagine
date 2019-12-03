#!/bin/bash
cd ~/dev/imagine

echo "creating README.md"
# pay_the_pypir replaces the image-links to point to github rawcontent
# since (test.)pypi.org won't host/show images.

# pandoc --filter ./pandoc_imagine.py _readme.md -t markdown -o README.md
pandoc --filter ./pandoc_imagine.py _readme.md -t markdown | awk -f pay_the_pypir > README.md

echo "creating README.rst"
pandoc --filter ./pandoc_imagine.py _readme.md -t rst | awk -f pay_the_pypir > README.rst

# echo "updating sample.pdf"
# cd examples
# pandoc --filter ../pandoc_imagine.py sample.md -o sample.pdf
# cd ..

echo "Done!"
