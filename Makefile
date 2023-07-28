SHELL := /bin/bash
.ONESHELL:

.PHONY: test install uninstall
TGT := $$HOME/.local/bin/playbook-linter

test:
	./playbook-linter.py --playbook=./test/playbook.yml --source_dir=./test

format:
	black ./playbook-linter.py
	isort ./playbook-linter.py

# Deployment
$(TGT): ./playbook-linter.py
	cp ./playbook-linter.py $(TGT)

install: $(TGT)
	python3 -m pip install -r ./requirements.txt

uninstall:
	rm $(TGT)

