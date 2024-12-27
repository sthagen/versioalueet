"""Provide the class VersionRanges for operations on version ranges

Use case example:

>>> version_ranges = VersionRanges('vers:pypi/|1.2.3|||||')
>>> assert version_ranges.normalize() == 'vers:pypi/1.2.3'
"""

import argparse
from typing import Union
from urllib.parse import unquote

import versioalueet.env as env
from versioalueet import DEBUG, log

ASTERISK = '*'
COLON = ':'
PIPE = '|'
SLASH = '/'

VCPairsType = list[tuple[str, str]]
ModelType = dict[str, Union[str, list[str], VCPairsType]]


def fail(message: str, model: Union[ModelType, None] = None) -> bool:
    """DRY.

    Usage examples:

    >>> DEBUG = True
    >>> model = {'received': 'no:thing'}
    >>> fail('some problem', model=model)
    True
    """
    if DEBUG and model:
        log.debug('Model = %s' % (model,))
    log.error(message)
    return True


def _parse_uri_scheme(version_range: str, model: ModelType) -> tuple[bool, str]:
    """The URI-scheme must be vers.

    Usage examples:

    >>> _parse_uri_scheme('VERS:WRONG/YES', model={'received': 'VERS:WRONG/YES', 'uri-scheme': 'vers'})
    (True, '')
    """
    if not version_range.startswith(f'vers{COLON}'):
        model['error'] = 'version range must start with the URI scheme vers'
        return fail(message=model['error'], model=model), ''  # type: ignore

    model['uri-scheme'] = 'vers'
    return False, version_range[5:]


def _parse_version_scheme(scheme_and_vcs: str, model: ModelType) -> tuple[bool, str]:
    """The <versioning-scheme> must be lowercase and a slash must separate from version constraints.

    Usage examples:

    >>> model = {'received': 'vers:pypi/*', 'uri-scheme': 'vers', 'versioning-scheme': 'pypi'}
    >>> _parse_version_scheme('pypi/*', model=model)
    (False, '*')

    >>> model = {'received': 'vers:pypi/', 'uri-scheme': 'vers', 'versioning-scheme': 'pypi'}
    >>> _parse_version_scheme('pypi/', model=model)
    (True, '')
    """
    if SLASH not in scheme_and_vcs:
        model['error'] = 'version range must provide <versioning-scheme> followed by a slash (/)'
        return fail(message=model['error'], model=model), ''  # type: ignore

    versioning_scheme, vc_string = scheme_and_vcs.split(SLASH, 1)
    model['versioning-scheme'] = versioning_scheme

    if not versioning_scheme:
        model['error'] = 'version system must be non empty'
        return fail(message=model['error'], model=model), ''  # type: ignore

    if not versioning_scheme.lower() == versioning_scheme:
        model['error'] = 'version system must be lower case'
        return fail(message=model['error'], model=model), ''  # type: ignore

    if not vc_string:
        model['error'] = 'version constraints must be non empty'
        return fail(message=model['error'], model=model), ''  # type: ignore

    return False, vc_string


def _split_version_constraints(vc_string: str, model: ModelType) -> tuple[bool, list[str]]:
    """Split real version constraints.

    Usage examples:

    >>> _split_version_constraints('13', {})
    (False, ['13'])

    >>> _split_version_constraints('|||||42||', {})
    (False, ['42'])

    >>> _split_version_constraints('|1|2|3|=4||>=6', {})
    (False, ['1', '2', '3', '=4', '>=6'])
    """
    if PIPE in vc_string:
        vc_unframed = vc_string.strip(PIPE)
        if vc_unframed.startswith(ASTERISK):
            version_constraints = [ASTERISK]
            if vc_unframed != ASTERISK:
                model['error'] = 'if present, asterisk (%s) must be the only version constraint' % (ASTERISK,)
                return fail(message=model['error'], model=model), []  # type: ignore

    version_constraints = [vc for vc in vc_string.split(PIPE) if vc]
    return False, version_constraints


def _parse_version_constraint_pairs(version_constraints: list[str], model: ModelType) -> tuple[bool, VCPairsType]:
    """Parse the constraints into pairs of versions and comparators.

    Implementer notes:

    - the version constraints items contain no spaces and no pipes

    Usage examples:

    >>> _parse_version_constraint_pairs(['1', '3', '=4', '2', '>=6'], model={})
    (False, [('1', ''), ('2', ''), ('3', ''), ('4', '='), ('6', '>=')])

    >>> model = {}
    >>> _parse_version_constraint_pairs(['1', '', '2'], model=model)
    (True, [])
    >>> assert 'empty' in model.get('error', '')
    """
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

    versions = [version for version, _ in vc_pairs]

    if sorted(list(set(versions))) != versions:
        model['error'] = 'versions must be unique across all version constraints'
        return fail(message=model['error'], model=model), []  # type: ignore

    return False, vc_pairs


def _validate_version_constraints(vc_pairs: VCPairsType, model: ModelType) -> bool:
    """Validate and optimize the version constraints parsed from string.

    Examples:

    >>> True
    True
    """
    vc_unequal_pairs = [(v, c) for v, c in vc_pairs if c == '!=']
    vc_other_pairs = [(v, c) for v, c in vc_pairs if c != '!=']
    model['vc-unequal-pairs'] = vc_unequal_pairs
    model['vc-other-pairs'] = vc_other_pairs
    model['version-constraint-pairs'] = vc_pairs
    return False


class VersionRanges:
    """Provide operations on version ranges.

    Usage examples:

        >>> lc_url_encoded = '1%3e2%3c3%3d4%215%2a6%7c7'
        >>> uc_url_encoded = '1%3E2%3C3%3D4%215%2A6%7C7'
        >>> version_decoded = '1>2<3=4!5*6|7'
        >>> triplicated = '|'.join((lc_url_encoded, uc_url_encoded, version_decoded))
        >>> version_ranges = VersionRanges(f'vers:pypi/{triplicated}')
        >>> assert 'unique' in version_ranges.model.get('error', '')

    """

    def __init__(self, version_range: str) -> None:
        """Later alligator.

        Usage examples:

        >>> hidden_emopty_version = 'vers:pypi/|1.2.3|>||||'
        >>> version_ranges = VersionRanges(hidden_emopty_version)
        >>> assert 'empty version detected' in version_ranges.model.get('error', '')
        """
        self.failed, self.model = self.parse(''.join(version_range.split()))

    def normalize(self, version_range: Union[str, None] = None) -> str:
        """Normalize version range.

        Usage examples:

        >>> a_version = 'vers:pypi/|1.2.3||||'
        >>> version_ranges = VersionRanges(a_version)
        >>> assert not version_ranges.model.get('error', '')
        >>> version_ranges.normalize()
        'vers:pypi/1.2.3'

        >>> hidden_emopty_version = 'vers:pypi/|1.2.3|>||||'
        >>> vr = VersionRanges('vers:abc/42')
        >>> vr.normalize(hidden_emopty_version)
        'ERROR:<empty version detected>'
        """
        if version_range is not None:
            self.failed, self.model = self.parse(''.join(version_range.split()))
        if error := self.model.get('error', ''):
            return 'ERROR:<' + error + '>'  # type: ignore
        return self.version_range  # type:ignore

    def __repr__(self) -> str:
        """The version ranges string is what we are.

        Usage examples:

        >>> maybe_43 = 'vers:pypi/<44|>42'
        >>> version_ranges = VersionRanges(maybe_43)
        >>> assert 'vers:pypi/>42|<44' == str(version_ranges)
        """
        return self.version_range  # type: ignore

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

        failed = _validate_version_constraints(vc_pairs, model)
        if failed:
            return failed, model

        model['version-constraints'] = [f'{c}{v}' for v, c in vc_pairs]
        model['version-range'] = (
            'vers' + COLON + model['versioning-scheme'] + SLASH + PIPE.join(model['version-constraints'])  # type: ignore
        )

        self.versioning_scheme = model['versioning-scheme']
        self.version_constraints = model['version-constraints']
        self.version_range = model['version-range']

        return failed, model


def main(options: argparse.Namespace) -> int:
    if DEBUG:
        for line in env.report(format='text').split('\n'):  # type: ignore
            log.debug(line)
    if options.versions:
        log.warning('version inclusion assessment requested, but not implemented yet')
        log.warning("details: requested versions were ('%s')" % ("', '".join(options.versions),))
        non_space_versions = [v.strip() for v in options.versions]
        non_empty_versions = [v for v in non_space_versions if v]
        if non_space_versions != non_empty_versions:
            log.error('received empty or space only version identifiers for inclusion test')
            return 2
    version_ranges = VersionRanges(options.version_ranges)
    if not version_ranges.failed:
        if DEBUG:
            log.debug('model: [')
            for k, v in version_ranges.model.items():
                if isinstance(v, str):
                    log.debug("- %s: '%s'" % (k, str(v)))
                else:
                    log.debug('- %s: %s' % (k, str(v)))
            log.debug(']')
        print(version_ranges)
        return 0

    return 1


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)
