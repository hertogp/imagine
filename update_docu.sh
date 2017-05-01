#!/bin/bash
cd ~/dev/imagine
echo "updating README .."
pandoc --filter ./imagine.py _readme.md -t markdown -o README.md
echo "Done!"
cd ~/dev/imagine/examples
echo
echo "updating sample.pdf"
pandoc --filter ../imagine.py sample.md -o sample.pdf
echo "Done!"
cd ~/dev/imagine


