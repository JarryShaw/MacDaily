#!/usr/bin/env bash

# print a trace of simple commands
set -x

# update version string
python3 setup-version.py

# update manpages
cd contrib
for file in $( ls *.rst ); do
    name=${file%.rst*}
    pipenv run rst2man.py ${file} > "../src/man/${name}.1"
done
cd ..

# duplicate distribution files
mkdir -p release
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
      release/**/.DS_Store \
      release/**/typescript \
      release/**/__pycache__ \
      release/src/res/daemon-*.applescript
cd release/
mv src macdaily

# prepare for PyPI distribution
rm -rf build 2> /dev/null
mkdir eggs \
      sdist \
      wheels 2> /dev/null
mv -f dist/*.egg eggs/ 2> /dev/null
mv -f dist/*.whl wheels/ 2> /dev/null
mv -f dist/*.tar.gz sdist/ 2> /dev/null
rm -rf dist 2> /dev/null

# fetch platform spec
platform=$( python3 -c "import distutils.util; print(distutils.util.get_platform().replace('-', '_').replace('.', '_'))" )

# make Python >=3.6 distribution
python3.7 setup.py bdist_egg bdist_wheel --plat-name="${platform}" --python-tag='cp37'
python3.6 setup.py bdist_egg bdist_wheel --plat-name="${platform}" --python-tag='cp36'

# perform f2format
f2format -n macdaily
ret="$?"
if [[ $ret -ne "0" ]] ; then
    exit $ret
fi

# make Python <3.6 distribution
# for python in /usr/bin/python \
#               /usr/local/Cellar/pypy/*/bin/pypy \
#               /usr/local/Cellar/pypy3/*/bin/pypy3 \
#               /usr/local/Cellar/python/*/bin/python3.? \
#               /usr/local/Cellar/python@2/*/bin/python2.? \
#               /Library/Frameworks/Python.framework/Versions/?.?/bin/python?.?
#               /System/Library/Frameworks/Python.framework/Versions/?.?/bin/python?.? ; do
#     $python setup.py bdist_egg
# done
pypy3 setup.py bdist_wheel --plat-name="${platform}" --python-tag='pp35'
python3.5 setup.py bdist_egg
python3.4 setup.py bdist_egg
python3 setup.py sdist

# distribute to PyPI and TestPyPI
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

# get version string
version=$( cat macdaily/util/const.py | grep "__version__" | sed "s/__version__ = '\(.*\)'/\1/" )
git tag "v${version}" && \
git push --tags

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

# file new release
go run github.com/aktau/github-release release \
    --user JarryShaw \
    --repo MacDaily \
    --tag "v${version}" \
    --name "MacDaily v${version}" \
    --description "$1"

# update Homebrew Formulae
pipenv run python3 setup-formula.py

cd Formula
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
