PROJECT = feedpipe

all:
	$(error Please pick a target)

test: clean validate
	nosetests --with-xunit -vd --with-doctest

clean:
	rm -rf build dist ${PROJECT}.egg-info nosetests.xml
	find . -name '*.py[co]' -exec rm {} \;

clobber: clean
	rm -rf *.egg

validate:
	flake8 ${PROJECT} tests

jenkins: test

wheel:
	python setup.py bdist_wheel

package: wheel

.PHONY: all test clean validate jenkins wheel package
