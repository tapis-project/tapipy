# Makefile for local development

.PHONY: down clean

build:	
	rm -rf dist
	poetry build

test: build
	docker build -t tapis/tapipy-tests -f Dockerfile-tests .
	docker run -it --rm  tapis/tapipy-tests

pull_specs:
	python3 repo_spec_pull_script.py
	python3 repo_spec_creation_script.py