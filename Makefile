MAINTAINER="Frederik Petersen <fp@abusix.com>"

all: clean package

clean:
	rm -f *.deb
	rm -fr build
	rm -fr *.egg-info
	rm -fr dist
	find . -name '*.pyc' -delete
	rm -fr dist_eggs

package: clean
	python setup.py bdist_egg --exclude-source-files

release: clean
	python setup.py bdist_egg --exclude-source-files sdist upload -r http://releases.abusix.local

register:
	python setup.py register -r http://releases.abusix.local

.PHONY: clean package release register
