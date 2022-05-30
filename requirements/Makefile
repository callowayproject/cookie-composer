.PHONY: all check clean

objects = $(wildcard *.in)
outputs := $(objects:.in=.txt)

all: $(outputs)

%.txt: %.in
	pip-compile --verbose --output-file $@ $<

prod.txt: cookiecutter.txt

test.txt: prod.txt

dev.txt: test.txt docs.txt

check:
	@which pip-compile > /dev/null

clean: check
	- rm *.txt
