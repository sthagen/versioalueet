from versioalueet.api import VersionRanges


def test_versioalueet():
    incoming = 'vers:npm/1.2.3 | < 5.0.0| >= 2.0.0 '
    expected = 'vers:npm/1.2.3|>=2.0.0|<5.0.0'
    normalized = VersionRanges(incoming).normalize()
    assert normalized == expected


def test_parse_empty():
    version_ranges = VersionRanges('')
    assert 'scheme vers' in version_ranges.model.get('error', '')


def test_parse_no_uri_scheme():
    version_ranges = VersionRanges('asd')
    assert 'scheme vers' in version_ranges.model.get('error', '')


def test_parse_uri_scheme_not_lowercase():
    version_ranges = VersionRanges('Vers:')
    assert 'scheme vers' in version_ranges.model.get('error', '')


def test_parse_no_versioning_system():
    version_ranges = VersionRanges('vers:/')
    assert 'empty' in version_ranges.model.get('error', '')


def test_parse_versioning_system_not_lower_case():
    version_ranges = VersionRanges('vers:Npm/')
    assert 'lower case' in version_ranges.model.get('error', '')


def test_parse_no_version_constraints():
    version_ranges = VersionRanges('vers:pypi/       ')
    assert 'empty' in version_ranges.model.get('error', '')


def test_parse_no_slash():
    version_ranges = VersionRanges('vers:pypi>42')
    assert 'slash' in version_ranges.model.get('error', '')


def test_parse_comparator_but_no_version():
    version_ranges = VersionRanges('vers:pypi/>    ')
    assert 'empty' in version_ranges.model.get('error', '')


def test_parse_asterisk_and_other_version_constraints():
    version_ranges = VersionRanges('vers:pypi/*|<=42')
    assert 'present' in version_ranges.model.get('error', '')


def test_parse_single_version():
    version_ranges = VersionRanges('vers:pypi/1.2.3')
    assert version_ranges.normalize() == 'vers:pypi/1.2.3'


def test_parse_all_versions_asterisk():
    version_ranges = VersionRanges('vers:pypi/|*|||')
    assert version_ranges.normalize() == 'vers:pypi/*'


def test_parse_superfluos_pipes():
    version_ranges = VersionRanges('vers:pypi/|1.2.3|||||')
    assert version_ranges.normalize() == 'vers:pypi/1.2.3'


def test_parse_superfluos_pipes_explicitly():
    version_ranges = VersionRanges('vers:pypi/|1.2.3|||||')
    assert version_ranges.normalize('vers:pypi/|1.2.3|||||') == 'vers:pypi/1.2.3'


def test_parse_comparators():
    pairs = (
        ('vers:pypi/<=42', 'vers:pypi/<=42'),
        ('vers:pypi/>=42', 'vers:pypi/>=42'),
        ('vers:pypi/!=42', 'vers:pypi/!=42'),
        ('vers:pypi/=42', 'vers:pypi/42'),
        ('vers:pypi/42', 'vers:pypi/42'),
        ('vers:pypi/<42', 'vers:pypi/<42'),
        ('vers:pypi/>42', 'vers:pypi/>42'),
    )
    for incoming, expected in pairs:
        version_ranges = VersionRanges(incoming)
        assert version_ranges.normalize() == expected


def test_parse_optimizer():
    pairs = (
        ('vers:golang/>v0.0.0|!=v42', 'vers:golang/>v0.0.0|!=v42'),
        ('vers:golang/>v0.0.0|>=v0.0.1', 'vers:golang/>v0.0.0'),
        ('vers:golang/>v0.0.0|>=v0.0.1|>=v0.0.2', 'vers:golang/>v0.0.0'),
        ('vers:golang/>v0.0.0|>=v0.0.1|v0.0.2|<v0.0.3|v0.0.4|<v0.0.5|>=v0.0.6', 'vers:golang/>v0.0.0|<v0.0.5|>=v0.0.6'),
    )
    for incoming, expected in pairs:
        version_ranges = VersionRanges(incoming)
        assert version_ranges.normalize() == expected


def test_parse_some_empty_version():
    hidden_emopty_version = 'vers:pypi/|1.2.3|>||||'
    version_ranges = VersionRanges(hidden_emopty_version)
    assert 'empty version detected' in version_ranges.model.get('error', '')


def test_parse_hidden_duplicate_versions():
    lc_url_encoded = '1%3e2%3c3%3d4%215%2a6%7c7'
    uc_url_encoded = '1%3E2%3C3%3D4%215%2A6%7C7'
    version_decoded = '1>2<3=4!5*6|7'
    triplicated = '|'.join((lc_url_encoded, uc_url_encoded, version_decoded))
    version_ranges = VersionRanges(f'vers:pypi/{triplicated}')
    assert 'unique' in version_ranges.model.get('error', '')


def test_normalize_versioning_system_not_lower_case():
    versioning_system_not_lower_case = 'vers:Npm/'
    version_ranges = VersionRanges(versioning_system_not_lower_case)
    response = version_ranges.normalize(versioning_system_not_lower_case)
    assert 'lower case' in response
