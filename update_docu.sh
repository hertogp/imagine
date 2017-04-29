#!/bin/bash
cd ~/dev/imagine
echo "updating README .."
pandoc --filter ./imagine.py README.md -t markdown -o README
echo "Done!"
cd ~/dev/imagine/examples
echo
echo "updating sample.pdf"j
pandoc --filter ../imagine.py sample.md -o sample.pdf
echo "Done!"
cd ~/dev/imagine


