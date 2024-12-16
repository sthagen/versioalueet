import pytest

from versioalueet.api import VersionRanges


def test_versioalueet():
    incoming = 'vers:npm/1.2.3 | < 5.0.0| >= 2.0.0 '
    expected = 'vers:npm/1.2.3|>=2.0.0|<5.0.0'
    normalized = VersionRanges(incoming).normalize()
    assert normalized == expected


def test_parse_empty():
    with pytest.raises(ValueError) as err:
        VersionRanges('')
        assert 'empty' in str(err)


def test_parse_no_uri_scheme():
    with pytest.raises(ValueError) as err:
        VersionRanges('asd')
        assert 'scheme' in str(err)


def test_parse_uri_scheme_not_lowercase():
    with pytest.raises(ValueError) as err:
        VersionRanges('Vers:')
        assert 'lower case' in str(err)


def test_parse_no_versioning_system():
    with pytest.raises(ValueError) as err:
        VersionRanges('vers:/')
        assert 'empty' in str(err)


def test_parse_versioning_system_not_lower_case():
    with pytest.raises(ValueError) as err:
        VersionRanges('vers:Npm/')
        assert 'lower case' in str(err)


def test_parse_no_version_constraints():
    with pytest.raises(ValueError) as err:
        VersionRanges('vers:pypi/       ')
        assert 'empty' in str(err)


def test_parse_asterisk_and_other_version_constraints():
    with pytest.raises(ValueError) as err:
        VersionRanges('vers:pypi/*|<=42')
        assert 'present' in str(err)


def test_parse_single_version():
    version_ranges = VersionRanges('vers:pypi/1.2.3')
    assert version_ranges.normalize() == 'vers:pypi/1.2.3'


def test_parse_all_versions_asterisk():
    version_ranges = VersionRanges('vers:pypi/|*|||')
    assert version_ranges.normalize() == 'vers:pypi/*'


def test_parse_superfluos_pipes():
    version_ranges = VersionRanges('vers:pypi/|1.2.3|||||')
    assert version_ranges.normalize() == 'vers:pypi/1.2.3'
