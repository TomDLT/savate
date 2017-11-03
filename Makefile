# simple makefile to simplify repetetive build env management tasks

PYTHON ?= python

in: inplace

inplace:
	$(PYTHON) setup.py build_ext -i

install:
	$(PYTHON) setup.py install

develop:
	$(PYTHON) setup.py develop
