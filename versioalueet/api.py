"""Provide the class VersionRanges for operations on version ranges

Use case example:

TBD
"""

import argparse
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
    if DEBUG and model:
        log.debug('Model = %s' % (model,))
    log.error(message)
    return True


def _parse_uri_scheme(version_range: str, model: ModelType) -> tuple[bool, str]:
    """The URI-scheme must be vers."""
    if not version_range.startswith(f'vers{COLON}'):
        model['error'] = 'version range must start with the URI scheme vers'
        return fail(message=model['error'], model=model), ''  # type: ignore

    model['uri-scheme'] = 'vers'
    return False, version_range[5:]


def _parse_version_scheme(scheme_and_vcs: str, model: ModelType) -> tuple[bool, str]:
    """The <versioning-scheme> must be lowercase and a slash must separate from version constraints."""
    if SLASH not in scheme_and_vcs:
        model['error'] = 'version range must provide <versioning-scheme> followed by a slash (/)'
        return fail(message=model['error'], model=model), ''  # type: ignore

    versioning_scheme, vc_string = scheme_and_vcs.split(SLASH, 1)
    versioning_scheme = versioning_scheme.strip()
    model['versioning-scheme'] = versioning_scheme

    if not versioning_scheme:
        model['error'] = 'version system must be non empty'
        return fail(message=model['error'], model=model), ''  # type: ignore

    if not versioning_scheme.lower() == versioning_scheme:
        model['error'] = 'version system must be lower case'
        return fail(message=model['error'], model=model), ''  # type: ignore

    vc_string = vc_string.strip()
    if not vc_string:
        model['error'] = 'version constraints must be non empty'
        return fail(message=model['error'], model=model), ''  # type: ignore

    return False, vc_string


def _split_version_constraints(vc_string: str, model: ModelType) -> tuple[bool, list[str]]:
    """Split real version constraints."""
    if PIPE in vc_string:
        if vc_string.strip(PIPE).startswith(ASTERISK):
            version_constraints = [ASTERISK]
            if vc_string.strip(PIPE) != ASTERISK:
                model['error'] = 'if present, asterisk (%s) must be the only version constraint' % (ASTERISK,)
                return fail(message=model['error'], model=model), []  # type: ignore

    version_constraints = [vc for vc in vc_string.replace(' ', '').split(PIPE) if vc]
    return False, version_constraints


def _parse_version_constraint_pairs(version_constraints: list[str], model: ModelType) -> tuple[bool, VCPairsType]:
    """Separation of concerns."""
    vc_pairs: VCPairsType = []
    for cv in version_constraints:
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
            model['error'] = 'empty version detected'
            return fail(message=model['error'], model=model), []  # type: ignore

        if '%' in version:
            version = unquote(version)

        vc_pairs.append((version, comparator))

    vc_pairs.sort()
    model['version-constraint-pairs'] = vc_pairs

    return False, vc_pairs


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
        model: ModelType = {
            'received': version_range,
        }

        failed, scheme_and_vcs = _parse_uri_scheme(version_range, model)
        if failed:
            return failed, model

        failed, vc_string = _parse_version_scheme(scheme_and_vcs, model)
        if failed:
            return failed, model

        failed, version_constraints = _split_version_constraints(vc_string, model)
        if failed:
            return failed, model

        failed, vc_pairs = _parse_version_constraint_pairs(version_constraints, model)
        if failed:
            return failed, model

        versions = [version for version, _ in vc_pairs]

        if sorted(list(set(versions))) != versions:
            model['error'] = 'versions must be unique across all version constraints'
            return fail(message=model['error'], model=model), model  # type: ignore

        self.versioning_scheme = model['versioning-scheme']
        self.version_constraints = [f'{c}{v}' for v, c in vc_pairs]
        model['version-constraints'] = self.version_constraints
        self.version_range = 'vers' + COLON + self.versioning_scheme + SLASH  # type: ignore
        self.version_range += PIPE.join(self.version_constraints)

        return failed, model


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
