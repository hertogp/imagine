#!/bin/bash
cd ~/dev/imagine
echo "updating README.md"
pandoc --filter ./pandoc_imagine.py _readme.md -t markdown -o README.md
echo "updating README.rst"
pandoc --filter ./pandoc_imagine.py _readme.md -o README.rst
echo "Done!"
cd ~/dev/imagine/examples
echo
echo "updating sample.pdf"
pandoc --filter ../pandoc_imagine.py sample.md -o sample.pdf
echo "Done!"
cd ~/dev/imagine

