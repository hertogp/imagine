#!/bin/bash

echo "updating README .."
pandoc --filter imagine README.md -t markdown -o README
echo "Done!"

