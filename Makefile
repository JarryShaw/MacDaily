.PHONY: clean dist manpages release pipenv pypi setup

export PIPENV_VENV_IN_PROJECT=1

SHELL   := /usr/local/bin/bash
DIR     ?= $(shell pwd)

# get version string
version ?= $(shell pipenv run python -c "import pkg_resources, time; print(pkg_resources.parse_version(time.strftime('%Y.%m.%d')))")
VERSION := $(shell pipenv run python -c "import pkg_resources; print(pkg_resources.parse_version('$(version)'))")
# commit message
message ?= ""

# fetch platform spec
platform       = $(shell pipenv run python -c "import distutils.util; print(distutils.util.get_platform().replace('-', '_').replace('.', '_'))")
python_version = $(shell pipenv run python -c "import sys; print('%s%s' % sys.version_info[:2])")
implementation = $(shell pipenv run python -c "import sys; print(sys.implementation.name[:2])")
archive        = "/tmp/macdaily-$(VERSION)-$(implementation)$(python_version)-none-$(platform).whl"

clean: clean-pyc clean-misc clean-pypi
dist: dist-all
manpages: clean-manpages update-manpages
release: release-master release-devel
pipenv: update-pipenv
pypi: dist-pypi dist-upload
setup: setup-version setup-formula setup-emoji

# setup pipenv
setup-pipenv: clean-pipenv
	pipenv install --dev

# update version string
setup-version:
	pipenv run python setup-version.py $(VERSION)

# update Homebrew Formulae
setup-formula: update-pipenv
	pipenv run python setup-formula.py

# update emoji mappings
setup-emoji:
	pipenv run python setup-emoji.py

# remove *.pyc
clean-pyc:
	find $(DIR) -iname __pycache__ | xargs rm -rf
	find $(DIR) -iname '*.pyc' | xargs rm -f

# remove devel files
clean-misc: clean-pyc
	find $(DIR) -iname 'dev_*' | xargs rm -f
	find $(DIR) -iname .DS_Store | xargs rm -f
	find $(DIR) -iname typescript | xargs rm -f
	find $(DIR) -iname 'daemon-*.applescript' | xargs rm -f

# remove pipenv
clean-pipenv:
	pipenv --rm

# remove manpages
clean-manpages:
	rm -rf src/man
	mkdir -p src/man

# prepare for PyPI distribution
.ONESHELL:
clean-pypi:
	set -ex
	cd $(DIR)
	mkdir -p dist sdist eggs wheels
	find dist -iname '*.egg' -exec mv {} eggs \;
	find dist -iname '*.whl' -exec mv {} wheels \;
	find dist -iname '*.tar.gz' -exec mv {} sdist \;
	rm -rf build dist *.egg-info

# update pipenv
update-pipenv:
	pipenv update
	pipenv install --dev
	pipenv clean

# update manpages
.ONESHELL:
update-manpages:
	set -ex
	cd contrib
	for file in $$( ls *.rst ); do \
	    name=$${file%.rst*}; \
	    pipenv run rst2man.py $${file} > "../src/man/$${name}.8"; \
	done

# update maintenance information
update-maintainer:
	go run github.com/gaocegege/maintainer changelog
	go run github.com/gaocegege/maintainer contributor
	go run github.com/gaocegege/maintainer contributing

# make PyPI distribution
dist-pypi: clean-pypi dist-pypi-new dist-pypi-old

# make Python >=3.6 distribution
.ONESHELL:
dist-pypi-new:
	set -ex
	cd $(DIR)
	~/.pyenv/versions/3.8-dev/bin/python3.8 setup.py bdist_egg bdist_wheel --plat-name="$(platform)" --python-tag='cp38'
	~/.pyenv/versions/3.7.4/bin/python3.7 setup.py bdist_egg bdist_wheel --plat-name="$(platform)" --python-tag='cp37'
	~/.pyenv/versions/3.6.9/bin/python3.6 setup.py bdist_egg bdist_wheel --plat-name="$(platform)" --python-tag='cp36'
	~/.pyenv/versions/pypy3.6-7.1.1/bin/pypy3 setup.py bdist_egg bdist_wheel --plat-name="$(platform)" --python-tag='pp36'
	# docker run -v$(shell pwd):/wd -w/wd --entrypoint="python3.7" -eFAKE_ENV=true python:3.7 setup.py bdist_egg bdist_wheel --plat-name="$(platform)" --python-tag='cp37'
	# docker run -v$(shell pwd):/wd -w/wd --entrypoint="python3.6" -eFAKE_ENV=true python:3.6 setup.py bdist_egg bdist_wheel --plat-name="$(platform)" --python-tag='cp36'
	# docker run -v$(shell pwd):/wd -w/wd --entrypoint="pypy3" -eFAKE_ENV=true pypy:3.6 setup.py bdist_wheel --plat-name="$(platform)" --python-tag='pp36'

# perform f2format
dist-f2format:
	pipenv run f2format -n $(DIR)/macdaily

# make Python <3.6 distribution
.ONESHELL:
dist-pypi-old: dist-f2format
	set -ex
	cd $(DIR)
	~/.pyenv/versions/3.5.7/bin/python3.5 setup.py bdist_egg bdist_wheel --plat-name="$(platform)" --python-tag='cp35'
	~/.pyenv/versions/3.4.10/bin/python3.4 setup.py bdist_egg bdist_wheel --plat-name="$(platform)" --python-tag='cp34'
	~/.pyenv/versions/pypy3.5-7.0.0/bin/pypy3 setup.py bdist_egg bdist_wheel --plat-name="$(platform)" --python-tag='pp35'
	# docker run -v$(shell pwd):/wd -w/wd --entrypoint="python3.5" -eFAKE_ENV=true python:3.5 setup.py bdist_egg bdist_wheel --plat-name="$(platform)" --python-tag='cp35'
	# docker run -v$(shell pwd):/wd -w/wd --entrypoint="python3.4" -eFAKE_ENV=true python:3.4 setup.py bdist_egg bdist_wheel --plat-name="$(platform)" --python-tag='cp34'
	# docker run -v$(shell pwd):/wd -w/wd --entrypoint="pypy3" -eFAKE_ENV=true pypy:3.5 setup.py bdist_wheel --plat-name="$(platform)" --python-tag='pp35'
	pipenv run python setup.py sdist

# upload PyPI distribution
.ONESHELL:
dist-upload:
	set -ex
	cd $(DIR)
	twine check dist/*
	twine upload dist/* -r pypi --skip-existing
	twine upload dist/* -r pypitest --skip-existing

# duplicate distribution files
dist-prep:
	mkdir -p release
	rm -rf release/src \
	       release/macdaily
	cp -r .gitattributes \
	      .gitignore \
	      LICENSE \
	      MANIFEST.in \
	      README.rst \
	      src \
	      setup.py \
	      setup.cfg release/
	mv release/src release/macdaily

# add tag
.ONESHELL:
git-tag:
	set -ex
	cd $(DIR)
	if [[ -z "$(message)" ]] ; then \
	    git tag --sign "v$(VERSION)" ; \
	else \
	    git tag --sign "v$(VERSION)" --message "$(message)" ; \
	fi

# upload to GitHub
.ONESHELL:
git-upload:
	set -ex
	cd $(DIR)
	git pull
	git add .
	if [[ -z "$(message)" ]] ; then \
	    git commit --all --gpg-sign ; \
	else \
	    git commit --all --gpg-sign --message "$(message)" ; \
	fi
	git push

# upload after distro
git-aftermath:
	git pull
	git add .
	git commit --all --gpg-sign --message "Regular update after distribution"
	git push

# file new release on master
release-master:
	go run github.com/aktau/github-release release \
	    --user JarryShaw \
	    --repo MacDaily \
	    --tag "v$(VERSION)" \
	    --name "MacDaily v$(VERSION)" \
	    --description "$$(git log -1 --pretty=%B)"

# file new release on devel
release-devel: release-download
	go run github.com/aktau/github-release release \
	    --user JarryShaw \
	    --repo MacDaily \
	    --tag "v$(VERSION).$$(shasum -a256 $(archive) | cut -c -6)-devel" \
	    --name "MacDaily v$(VERSION).$$(shasum -a256 $(archive) | cut -c -6)-devel" \
	    --description "$$(git log -1 --pretty=%B)" \
	    --target "devel" \
	    --pre-release

release-download:
	pipenv run python -m pip download macdaily \
	    --platform=$(platform) \
	    --python-version=$(python_version) \
	    --implementation=$(implementation) \
	    --dest=/tmp \
	    --no-deps

# run pre-distribution process
dist-pre: setup-version manpages

# run post-distribution process
dist-post:
	$(MAKE) message="$(message)" DIR=release \
	    clean pypi git-tag git-upload
	$(MAKE) message="$(message)" \
	    git-upload release setup-formula
	$(MAKE) message="macdaily: $(VERSION)" DIR=Tap \
	    git-upload
	$(MAKE) message="$(message)" \
	    update-maintainer git-aftermath

# run full distribution process
dist-all: dist-pre dist-prep dist-post

# run distro process in devel
dist-devel: dist-pre git-upload

# run distro process in master
dist-master: dist-prep dist-post
