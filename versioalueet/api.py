"""Provide the class VersionRanges for operations on version ranges

Use case example:

TBD
"""

import argparse
import traceback
from typing import Union
from urllib.parse import unquote

from versioalueet import DEBUG, ENCODING, ENCODING_ERRORS_POLICY, log

ASTERISK = '*'
COLON = ':'
PIPE = '|'
SLASH = '/'

VCPairsType = list[tuple[str, str]]
ModelType = dict[str, Union[str, list[str], VCPairsType]]


def fail(message: str, model: Union[ModelType, None] = None) -> bool:
    """DRY."""
    try:
        raise ValueError(message)
    except ValueError:
        if DEBUG and model:
            log.debug('Model = %s' % (model,))
        for line in traceback.format_exc().splitlines():
            log.error(line)
    return True


class VersionRanges:
    """Provide operations on version ranges.

    TBD

    """

    def __init__(self, version_range: str) -> None:
        """Later alligator."""
        self.version_range = version_range
        self.normalize()
        self.failed, self.model = self.parse(self.version_range)

    def normalize(self, version_range: str = '') -> str:
        """Normalize version range."""
        if not version_range:
            version_range = self.version_range
        else:
            self.parse(version_range)
        return self.version_range

    def __repr__(self) -> str:
        """The version ranges string is what we are."""
        return self.version_range

    def parse(self, version_range: str) -> tuple[bool, ModelType]:
        """Poor person parser for bootstrap."""
        failed = False
        tempo: ModelType = {
            'received': version_range,
        }

        if not version_range.startswith(f'vers{COLON}'):
            tempo['error'] = 'version range must start with the URI scheme vers'
            return fail(message=tempo['error'], model=tempo), tempo  # type: ignore

        tempo['uri-scheme'] = 'vers'
        rest = version_range[5:]

        if SLASH not in rest:
            tempo['error'] = 'version range must provide <versioning-scheme> followed by a slash (/)'
            return fail(message=tempo['error'], model=tempo), tempo  # type: ignore

        self.versioning_scheme, rest = rest.split(SLASH, 1)
        tempo['versioning-scheme'] = self.versioning_scheme

        if not self.versioning_scheme.strip():
            tempo['error'] = 'version system must be non empty'
            failed = fail(message=tempo['error'], model=tempo)  # type: ignore

        self.versioning_scheme = self.versioning_scheme.strip()
        if not self.versioning_scheme.lower() == self.versioning_scheme:
            tempo['error'] = 'version system must be lower case'
            return fail(message=tempo['error'], model=tempo), tempo  # type: ignore

        if not rest.strip():
            tempo['error'] = 'version constraints must be non empty'
            return fail(message=tempo['error'], model=tempo), tempo  # type: ignore

        if PIPE in rest:
            if rest.strip(PIPE).startswith(ASTERISK):
                self.version_constraints = [ASTERISK]
                if rest.strip(PIPE) != ASTERISK:
                    tempo['error'] = 'if present, asterisk (%s) must be the only version constraint' % (ASTERISK,)
                    return fail(message=tempo['error'], model=tempo), tempo  # type: ignore

        self.version_constraints = [vc for vc in rest.replace(' ', '').split(PIPE) if vc]

        vc_pairs: VCPairsType = []
        for cv in self.version_constraints:
            comparator, version = '', ''
            if cv.startswith('>='):
                comparator, version = '>=', cv[2:]
            elif cv.startswith('<='):
                comparator, version = '<=', cv[2:]
            elif cv.startswith('!='):
                comparator, version = '!=', cv[2:]
            elif cv.startswith('<'):
                comparator, version = '<', cv[1:]
            elif cv.startswith('>'):
                comparator, version = '>', cv[1:]
            elif cv.startswith('='):
                comparator, version = '=', cv[1:]
            else:
                comparator, version = '', cv

            if not version:
                tempo['error'] = 'empty version detected'
                return fail(message=tempo['error'], model=tempo), tempo  # type: ignore

            if '%' in version:
                version = unquote(version)

            vc_pairs.append((version, comparator))

        vc_pairs_sorted = sorted(vc_pairs)
        tempo['version-constraint-pairs'] = vc_pairs_sorted

        versions = [version for version, _ in vc_pairs_sorted]

        if sorted(list(set(versions))) != versions:
            tempo['error'] = 'versions must be unique across all version constraints'
            return fail(message=tempo['error'], model=tempo), tempo  # type: ignore

        self.version_constraints = [f'{c}{v}' for v, c in vc_pairs_sorted]
        tempo['version-constraints'] = self.version_constraints
        self.version_range = 'vers' + COLON + self.versioning_scheme + SLASH
        self.version_range += PIPE.join(self.version_constraints)

        return failed, tempo


def main(options: argparse.Namespace) -> int:
    if not options.quiet:
        log.info(f'{DEBUG=}, {ENCODING=}, {ENCODING_ERRORS_POLICY=}')
    version_ranges = VersionRanges(options.version_ranges)
    if not version_ranges.failed:
        print(version_ranges)
        return 0

    return 1


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)
