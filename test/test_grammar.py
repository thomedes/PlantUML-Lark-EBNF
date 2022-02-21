#! /usr/bin/env python3

"""Test grammar against all examples."""

import os
import sys

import difflib
import lark

_GRAMMAR = '../plantuml.lark'


def _slurp(filename: str) -> str:
    """Get a text file contents in a simple call"""
    with open(filename, 'rt', encoding="UTF-8") as fd:
        return fd.read()

def _cleanup(text: str) -> str:
    '''Removes empty lines at the start and end and removes trailing space'''
    lines = text.strip().splitlines()
    return "\n".join(map(lambda s : s.rstrip(), lines))


def _test(parser, filename: str) -> bool:
    print(filename)
    test_case = _slurp(filename)
    # print(test_case)
    (uml, expected_result) = test_case.split("////////////////////////////")
    uml = uml.strip()
    expected_result = _cleanup(expected_result)

    try:
        tree = parser.parse(uml)
    except lark.UnexpectedCharacters as e:
        sys.stderr.write(str(e))
        return False
    except lark.UnexpectedEOF as e:
        sys.stderr.write(str(e))
        return False

    pretty = _cleanup(tree.pretty().expandtabs())
    passed = pretty == expected_result
    if not passed:
        print("FROM:")
        print(input)
        print("EXPECTED:")
        print(expected_result)
        print("GOT:")
        print(pretty)
        differ = difflib.Differ()
        diff = differ.compare(expected_result.splitlines(), pretty.splitlines())
        for line in diff:
            print(line)

    return passed


def _main(_) -> int:
    grammar = _slurp(_GRAMMAR)
    parser = lark.Lark(grammar)

    for root, _, files in os.walk('.'):
        files.sort()
        for file in files:
            if file[-9:] == ".plantuml":
                filename = os.path.join(root, file)
                passed = _test(parser, filename)
                if not passed:
                    return 1
    return 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv))
