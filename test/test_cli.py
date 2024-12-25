import pathlib

import pytest

import versioalueet.cli as cli
from versioalueet.api import VersionRanges

TEST_PREFIX = pathlib.Path('test', 'fixtures')
DEFAULT_DOCUMENTS_PATH = TEST_PREFIX
TEST_MAKE_MISSING = 'missing-this-file-for-'


def test_main_empty_request(capsys):
    options = cli.main([])
    assert options == 0  # type: ignore
    out, err = capsys.readouterr()
    assert 'usage: versioalueet [-h] [--quiet] [--verbose]' in out
    assert not err


def test_main_help_request(capsys):
    with pytest.raises(SystemExit) as err:
        options = cli.main(['-h'])
        assert options == 0  # type: ignore
    out, err = capsys.readouterr()
    assert 'usage: versioalueet [-h] [--quiet] [--verbose]' in out
    assert 'Version ranges (Finnish: versioalueet)' in out
    assert 'show this help message and exit' in out
    assert not err


def test_main_quiet_and_verbose_request(capsys):
    with pytest.raises(SystemExit) as err:
        options = cli.main(['-q', '-v'])
        assert options == 2  # type: ignore
    out, err = capsys.readouterr()
    assert 'usage: versioalueet [-h] [--quiet] [--verbose]' in err
    assert 'error' in err.lower()
    assert 'cannot be quiet and verbose' in err
    assert not out


def test_main_valid_version_ranges_request(capsys):
    in_vrs = 'vers:pypi/*'
    options = cli.main(['-r', in_vrs])
    assert options == 0  # type: ignore
    out, err = capsys.readouterr()
    version_ranges = VersionRanges(in_vrs)
    assert version_ranges.normalize() == in_vrs
    assert in_vrs in out
    assert not err


def test_parse_empty_request(capsys):
    options = cli.parse_request([])
    assert options == 0  # type: ignore
    out, err = capsys.readouterr()
    assert 'usage: versioalueet [-h] [--quiet] [--verbose]' in out
    assert not err


def test_parse_help_request(capsys):
    with pytest.raises(SystemExit) as err:
        options = cli.parse_request(['-h'])
        assert options == 0  # type: ignore
    out, err = capsys.readouterr()
    assert 'usage: versioalueet [-h] [--quiet] [--verbose]' in out
    assert 'Version ranges (Finnish: versioalueet)' in out
    assert 'show this help message and exit' in out
    assert not err


def test_parse_request_pos_doc_root_not_present(capsys):
    with pytest.raises(SystemExit) as err:
        cli.parse_request([f'{TEST_MAKE_MISSING}{DEFAULT_DOCUMENTS_PATH}', '-q', '-v'])
    assert err.value.code == 2
    out, err = capsys.readouterr()
    assert not out
    message_part = f'versioalueet: error: unrecognized arguments: {TEST_MAKE_MISSING}{DEFAULT_DOCUMENTS_PATH}'
    assert message_part in err
