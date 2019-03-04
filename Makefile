.PHONY: clean dist manpages release pipenv pypi setup

SHELL := /usr/local/bin/bash
DIR   ?= .

# fetch platform spec
platform = $(shell python3 -c "import distutils.util; print(distutils.util.get_platform().replace('-', '_').replace('.', '_'))")
# get version string
version  = $(shell cat macdaily/util/const/macro.py | grep "VERSION" | sed "s/VERSION = '\(.*\)'/\1/")
# commit message
message  ?= ""

clean: clean-pyc clean-misc clean-pypi
dist: dist-all
manpages: clean-manpages update-manpages
release: release-master release-devel
pipenv: update-pipenv
pypi: dist-pypi dist-upload
setup: setup-version setup-formula

# setup pipenv
setup-pipenv: clean-pipenv
	pipenv install --dev

# update version string
setup-version:
	python3 setup-version.py

# update Homebrew Formulae
setup-formula: update-pipenv
	pipenv run python3 setup-formula.py

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
	mkdir -p sdist eggs wheels
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
		pipenv run rst2man.py $${file} > "../src/man/$${name}.1"; \
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
	python3.7 setup.py bdist_egg bdist_wheel --plat-name="$(platform)" --python-tag='cp37'
	python3.6 setup.py bdist_egg bdist_wheel --plat-name="$(platform)" --python-tag='cp36'

# perform f2format
dist-f2format:
	f2format -n $(DIR)/macdaily

# make Python <3.6 distribution
.ONESHELL:
dist-pypi-old: dist-f2format
	set -ex
	cd $(DIR)
	python3.5 setup.py bdist_egg bdist_wheel --plat-name="$(platform)" --python-tag='cp35'
	python3.4 setup.py bdist_egg bdist_wheel --plat-name="$(platform)" --python-tag='cp34'
	pypy3 setup.py bdist_wheel --plat-name="$(platform)" --python-tag='pp35'
	python3 setup.py sdist

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
		git tag --sign "v$(version)" ; \
	else \
		git tag --sign "v$(version)" --message "$(message)" ; \
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
		--tag "v$(version)" \
		--name "MacDaily v$(version)" \
		--description "$(message)"

# file new release on devel
release-devel:
	go run github.com/aktau/github-release release \
		--user JarryShaw \
		--repo MacDaily \
		--tag "v$(version).devel" \
		--name "MacDaily v$(version).devel" \
		--description "$(message)" \
		--target "devel" \
		--pre-release

# run pre-distribution process
dist-pre: setup-version manpages

# run post-distribution process
dist-post:
	$(MAKE) message="$(message)" DIR=release \
		clean pypi git-tag git-upload
	$(MAKE) message="$(message)" \
		git-upload release setup-formula
	$(MAKE) message="macdaily: $(version)" DIR=Tap \
		git-upload
	$(MAKE) message="$(message)" \
		update-maintainer git-aftermath

# run full distribution process
dist-all: dist-pre dist-prep dist-post

# run distro process in devel
dist-devel: dist-pre git-upload

# run distro process in master
dist-master: dist-prep dist-post
