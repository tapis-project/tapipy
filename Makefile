# Makefile for local development

ifdef in_jenkins
unexport interactive
else
export interactive := -it
endif


build:	
	rm -rf dist
	poetry build

test: build
	docker build -t tapis/tapipy-tests -f Dockerfile-tests .
	docker run $$interactive --rm  tapis/tapipy-tests

pull_specs:
	python3 repo_spec_pull_script.py
	python3 repo_spec_creation_script.py