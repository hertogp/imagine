#!/bin/bash
cd ~/dev/imagine

echo "creating README.md"
pandoc --filter ./pandoc_imagine.py _readme.md -t markdown -o README.md

echo "creating README.rst"
pandoc --filter ./pandoc_imagine.py _readme.md -t rst | awk -f pay_the_pypir > README.rst

echo "updating sample.pdf"
cd examples
pandoc --filter ../pandoc_imagine.py sample.md -o sample.pdf
cd ..

echo "Done!"
