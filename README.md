# playbook-linter

Tool for finding unused or missing variables in ansible playbooks

## Usage

Example:

```bash
playbook-linter --playbook=./test/playbook.yml --source_dir=./test
```

Help:

```
usage: playbook-linter [-h] -p PLAYBOOK -s SOURCE_DIR

options:
  -h, --help            show this help message and exit
  -p PLAYBOOK, --playbook PLAYBOOK
                        The playbook
  -s SOURCE_DIR, --source_dir SOURCE_DIR
                        Directory containing playbook and other playbooks or
                        templates that supply or depend on variables
```

## Installation
Assuming you are running linux, this will install the python requirements into your
active python environment and copy the script into the search path at `$HOME/.local/bin/playbook-linter`

```bash
git clone git@github.com:zachwaite/playbook-linter.git
cd playbook-linter
make install
```

## Uninstallation

```bash
cd playbook-linter && make uninstall
```

OR

```bash
rm $HOME/.local/bin/playbook-linter
```


