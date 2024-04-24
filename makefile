SRCDIR = .
PYTHON = python3

run:
	$(PYTHON) app.py

install:
	$(PYTHON) -m pip install -U pip wheel setuptools;
	pip install -r $(SRCDIR)/req.txt;
	pip cache purge;
	pip list;

uninstall:
	$(PYTHON) -m pip uninstall -r $(SRCDIR)/req.txt;
	pip list;
	pip cache purge

