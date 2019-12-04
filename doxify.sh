#!/bin/bash
cd ~/dev/imagine

echo "
Creating README.md
 + runs imagine filter on _readme.md -> README.md
 + uses Github-Flavored Markdown (-t gfm) as target format
 + uses pay_the_pypir to fix image links so they're absolute links pointing
   to github raw content, since pypi.org won't host the images.

"

pandoc --filter ./pandoc_imagine.py _readme.md -t gfm | awk -f pay_the_pypir > README.md

echo "\
Creating source distribution in ./dist
"

python3 setup.py sdist

echo "\

TEST:
 +--> twine upload --repository-url https://test.pypi.org/legacy/ ./dist/*

PYPI:
 + BEFORE uploading to pypi.org
 +  nvim pandoc_imagine.py --> remove -rcy from __version__ = '0.1.x-rcy'
 +
 + UPDATE GIT w/ tags
 +  git add *
 +  git commit 'release message'
 +  git tag   # to see current tags
 +  git tag 0.1.x -m 'version 0.1.x'
 +  git push --tags origin master
 +
 + NEW SDIST
 +  python3 setup.py sdat
 +
 + UPLOAD
 +--> twine upload --repository-url https://pypi.org/legacy/ ./dist*

"

