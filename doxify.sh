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

echo
if [ $? -eq 0 ]; then
    echo "---- ok, README.md has been created"
else
    echo ">>>> Not ok, failed to create README.md"
    exit 1
fi

echo "\

Creating source distribution in ./dist
 + setup.py retrieves the __version__ number from pandoc_imagine.py
 + generate a single source distribution in ./dist
"

python3 setup.py sdist

echo
if [ $? -eq 0 ]; then
    echo "---- ok, created a source distribution"
    echo
    ls -lpah ./dist/*
    echo
else
    echo ">>>> Not ok, failed to create source distribution!"
    exit 1
fi

echo "\


TEST:
 + upload the test distibution
 | -> remove the *old* src distributions from ./dist
 | -> twine upload --repository-url https://test.pypi.org/legacy/ ./dist/*
 |
 + does it render ok on test.pypi.org?
 |  see https://test.pypi.org/project/pandoc_imagine/0.1.xrcy
 |
 + can you install it from there?
 |  cd ~/sandbox/tmpdir
 |  virtualenv test_imagine
 |  source test_imagine/bin/activate
 |  #> pip3 install -i https://test... won't pull in dependencies
 |  #> you need to install them manually first
 |  #> later on, publish release candidate to pypi.org
 |  #> then re-test (with auto install of dependencies)
 |  #> then upload after removing the rcy from the version .. pff
 |  pip3 install six pandocfilters
 |  pip3 install -i https://test.pypi.org/simple/ pandoc-imagine
 |
 + can you use the filter?
 |  cp ~/dev/imagine/examples/gnuplot.md .
 |  pandoc --filter pandoc-imagine gnuplot.md -o gnuplot.pdf
 |
 v

PYPI:
 + BEFORE uploading to pypi.org
 |  nvim pandoc_imagine.py --> remove rcy from __version__ = '0.1.xrcy'
 |
 + UPDATE GIT w/ tags
 |  git add *
 |  git commit 'release message'
 |  git tag   # to see current tags
 |  git tag 0.1.x -m 'version 0.1.x'
 |  git push --tags origin master
 |
 + NEW SDIST
 |  python3 setup.py sdist
 |
 + UPLOAD
 |  no repo url is needed
 |  -> twine upload ./dist*
 |
 + AFTER
 |  set new version number
 |  nvim pandoc_imagine.py --> __version__ = '0.1.(x+1)rc0'
 v

 Done
"

