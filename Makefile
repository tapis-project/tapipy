# Makefile for local development

ifdef in_jenkins
unexport interactive
else
export interactive := -it
endif


build:	
	rm -rf dist
	poetry build

install: build
	pip3 uninstall tapipy -y
	pip3 install dist/*.whl

test: build
	docker build -t tapis/tapipy-tests -f Dockerfile-tests .
	docker run -e username=cgarcia -e password=Fuckoff12. $$interactive --rm  tapis/tapipy-tests

pull_specs:
	python3 repo_spec_pull_script.py
	@echo ""
	@echo ""
	python3 repo_spec_creation_script.py