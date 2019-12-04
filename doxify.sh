#!/bin/bash
cd ~/dev/imagine

echo "creating README.md"
# pay_the_pypir replaces the image-links to point to github rawcontent
# since (test.)pypi.org won't host images.

# pandoc --filter ./pandoc_imagine.py _readme.md -t markdown -o README.md
# PYPI supports git-flavored markdown
pandoc --filter ./pandoc_imagine.py _readme.md -t gfm | awk -f pay_the_pypir > README.md

#echo "creating README.rst"
#pandoc --filter ./pandoc_imagine.py _readme.md -t rst | awk -f pay_the_pypir > README.rst

# echo "updating sample.pdf"
# cd examples
# pandoc --filter ../pandoc_imagine.py sample.md -o sample.pdf
# cd ..

echo ""
echo "Creating source distribution in ./dist"
python3 setup.py sdist

echo "\

TEST upload +-> twine upload --repository-url https://test.pypi.org/legacy/ ./dist/*

PYPI
 - BEFORE uploading to pypi.org:
 + git add *
 + git commit 'release message'
 + git tag   # to see current tags
 + git tag 0.1.x -m 'version 0.1.x'
 + git push --tags origin master
 + python3 setup.py sdat
 |
 +-> twine upload --repository-url https://pypi.org/legacy/ ./dist*

