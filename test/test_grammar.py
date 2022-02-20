#! /usr/bin/env python3

"""Test grammar against all examples."""
import lark
import os

_GRAMMAR = '../plantuml.lark'


def _slurp(filename: str) -> str:
    with open(filename, 'rt', encoding="UTF-8") as fd:
        return fd.read()

def _test(parser, filename: str) -> None:
    print(filename)
    input = _slurp(filename)
    # print(input)
    (input, expected_result) = input.split("////////////////////////////")
    input = input.strip()
    expected_result = expected_result.strip()

    tree = parser.parse(input)
    pretty = tree.pretty().expandtabs().strip()
    if pretty != expected_result:
        print("FROM:")
        print(input)
        print("EXPECTED:")
        print(expected_result)
        print("GOT:")
        print(pretty)
        exit(1)


_grammar = _slurp(_GRAMMAR)
_parser = lark.Lark(_grammar)

for root, dirs, files in os.walk('.'):
    for file in files:
        if file[-9:] == ".plantuml":
            filename = os.path.join(root, file)
            _test(_parser, filename)
