#! /usr/bin/env python3

import argparse
import itertools
import re
from pathlib import Path
from typing import Any

import yaml
from typing_extensions import Self
from yaml import SafeLoader

Playbook = list[dict[str, Any]]
LinterReport = list[str]


class Linter:
    _playbook: Playbook
    _assignments: set[str]
    _sourcefiles: list[str]
    _usages: set[str]
    _ignorelist: set[str] = {
        "ansible_python_interpreter",
        "repo",
        "branch",
        "origin_build",
        "dest_build",
        "image",
        "pubkey",
        "agefile",
        "localpy",
        "remotepy",
        "item",
    }

    def with_playbook(self, ymlfile: str) -> Self:
        with open(ymlfile, "r") as f:
            raw = f.read()
            self._playbook = yaml.load(raw, Loader=SafeLoader)
            return self

    def extract_variable_assignments(self) -> Self:
        self._assignments = set(
            [
                x
                for x in itertools.chain.from_iterable(
                    [
                        [k for k in play.get("vars", []).keys()]  # type: ignore
                        for play in self._playbook
                    ]
                )
            ]
        )
        return self

    def with_sources(self, sourcefiles: list[str]) -> Self:
        self._sourcefiles = sourcefiles
        return self

    def extract_variable_usages(self) -> Self:
        pat = re.compile(r"\{\{\s?([a-zA-Z0-9_]+)\s?\}\}")
        out = set()
        for path in self._sourcefiles:
            with open(path, "r") as f:
                raw = f.read()
                for m in pat.findall(raw):
                    out.add(m)
        self._usages = out
        return self

    def _compute_unused_variables(self) -> set[str]:
        return self._assignments - self._usages - self._ignorelist

    def _compute_missing_variables(self) -> set[str]:
        return self._usages - self._ignorelist - self._assignments

    def report(self):
        unused = self._compute_unused_variables()
        missing = self._compute_missing_variables()
        print(
            " ".join(
                [
                    "=" * 35,
                    "Report",
                    "=" * 35,
                ]
            )
        )
        if unused:
            print(f"Unused variables: {unused}")
        if missing:
            print(f"Missing variables: {missing}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--playbook", required=True, help="The playbook")
    parser.add_argument(
        "-s",
        "--source_dir",
        required=True,
        help="Directory containing playbook and other playbooks or templates that supply or depend on variables",
    )
    args = parser.parse_args()
    playbook = Path(args.playbook)
    source_dir = Path(args.source_dir)

    _ = (
        Linter()
        .with_playbook(str(playbook))
        .with_sources([str(f) for f in source_dir.iterdir() if f.name != playbook.name])
        .extract_variable_assignments()
        .extract_variable_usages()
        .report()
    )


if __name__ == "__main__":
    main()
