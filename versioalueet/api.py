"""Provide the class VersionRanges for operations on version ranges

Use case example:

TBD
"""

import argparse
from typing import Union

from versioalueet import DEBUG, ENCODING, ENCODING_ERRORS_POLICY, log

ASTERISK = '*'
COLON = ':'
PIPE = '|'
SLASH = '/'


class VersionRanges:
    """Provide operations on version ranges.

    TBD

    """

    def __init__(self, version_range: str) -> None:
        """Later alligator."""
        self.version_range = version_range
        self.normalize()
        self.tempo = self.parse(self.version_range)

    def normalize(self, version_range: str = '') -> str:
        """Normalize version range."""
        if not version_range:
            version_range = self.version_range
        self.version_range = version_range.replace(' ', '')
        return self.version_range

    def parse(self, version_range: str) -> dict[str, Union[str, list[str]]]:
        """Poor person parser for bootstrap."""
        tempo: dict[str, Union[str, list[str]]] = {}

        if not version_range.startswith(f'vers{COLON}'):
            raise ValueError('version range must start with the URI scheme vers')

        tempo['uri-scheme'] = 'vers'
        rest = version_range[5:]

        if SLASH not in rest:
            raise ValueError('version range must provide <versioning-scheme> followed by a slash (/)')

        self.versioning_scheme, rest = rest.split(SLASH, 1)
        tempo['versioning-scheme'] = self.versioning_scheme

        if not self.versioning_scheme.strip():
            raise ValueError('version system must be non empty')

        self.versioning_scheme = self.versioning_scheme.strip()
        if not self.versioning_scheme.lower() == self.versioning_scheme:
            raise ValueError('version system must be lower case')

        if not rest.strip():
            raise ValueError('version constraints must be non empty')

        if rest.strip(PIPE).startswith(ASTERISK):
            self.version_constraints = [ASTERISK]
            if rest.strip(PIPE) != ASTERISK:
                raise ValueError(f'if present, asterisk ({ASTERISK}) must be the only version constraint')
        elif PIPE not in rest:
            self.version_constraints = [rest.replace(' ', '')]
        else:
            self.version_constraints = [vc for vc in rest.replace(' ', '').split(PIPE) if vc]

        tempo['version-constraints'] = self.version_constraints

        self.version_range = 'vers' + COLON + self.versioning_scheme + SLASH
        self.version_range += PIPE.join(self.version_constraints)

        return tempo


def main(options: argparse.Namespace) -> int:
    log.info(f'{DEBUG=}, {ENCODING=}, {ENCODING_ERRORS_POLICY=}')
    return 0


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)
