#!/bin/bash

# print a trace of simple commands
set -x

# duplicate distribution files
rm -rf release/src \
       release/macdaily
cp -r src \
      LICENSE \
      setup.py \
      setup.cfg \
      .gitignore \
      README.rst \
      MANIFEST.in \
      .gitattributes release/
rm -f release/**/dev_* \
      release/**/typescript
cd release/
mv src macdaily

# perform f2format
f2format -n macdaily
if [[ "$?" -ne "0" ]] ; then
    exit 1
fi

# prepare for PyPI distribution
rm -rf build 2> /dev/null
mkdir eggs \
      sdist \
      wheels 2> /dev/null
mv -f dist/*.egg eggs/ 2> /dev/null
mv -f dist/*.whl wheels/ 2> /dev/null
mv -f dist/*.tar.gz sdist/ 2> /dev/null

# distribute to PyPI and TestPyPI
python3 setup.py sdist bdist_wheel
twine upload dist/* -r pypi --skip-existing
twine upload dist/* -r pypitest --skip-existing

# upload to GitHub
git pull
ret="$?"
if [[ $ret -ne "0" ]] ; then
    exit $ret
fi
git add .
if [[ -z "$1" ]] ; then
    git commit -a -S
else
    git commit -a -S -m "$1"
fi
git push

# # archive original files
# for file in $( ls archive ) ; do
#     if [[ -d "archive/${file}" ]] ; then
#         tar -cvzf "archive/${file}.tar.gz" "archive/${file}"
#         rm -rf "archive/${file}"
#     fi
# done

# upload develop environment
cd ..
git pull
ret="$?"
if [[ $ret -ne "0" ]] ; then
    exit $ret
fi
git add .
if [[ -z "$1" ]] ; then
    git commit -a -S
else
    git commit -a -S -m "$1"
fi
git push
