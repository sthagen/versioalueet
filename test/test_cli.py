import logging

import pytest

import versioalueet.cli as cli
from versioalueet import VERSION
from versioalueet.api import VersionRanges

SYNOPSIS = 'usage: versioalueet [-h] [-q] [-v] [-R] [-V] [-r VERSION_RANGES]'
POSITIONAL_SYNOPSIS = '[versions ...]'


def test_main_empty_request(capsys):
    options = cli.main([])
    assert options == 0  # type: ignore
    out, err = capsys.readouterr()
    assert SYNOPSIS in out
    assert not err


def test_main_version_request(capsys):
    options = cli.main(['-V'])
    assert options == 0  # type: ignore
    out, err = capsys.readouterr()
    assert VERSION in out
    assert not err


def test_main_process_report_request(capsys):
    options = cli.main(['-R'])
    assert options == 0  # type: ignore
    out, err = capsys.readouterr()
    assert '"library-env":' in out
    assert f'"version": "{VERSION}",' in out
    assert not err


def test_main_help_request(capsys):
    with pytest.raises(SystemExit) as err:
        options = cli.main(['-h'])
        assert options == 0  # type: ignore
    out, err = capsys.readouterr()
    assert SYNOPSIS in out
    assert POSITIONAL_SYNOPSIS in out
    assert 'Version ranges (Finnish: versioalueet)' in out
    assert 'show this help message and exit' in out
    assert not err


def test_main_quiet_and_verbose_request(capsys):
    with pytest.raises(SystemExit) as err:
        options = cli.main(['-q', '-v'])
        assert options == 2  # type: ignore
    out, err = capsys.readouterr()
    assert SYNOPSIS in err
    assert POSITIONAL_SYNOPSIS in err
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
    assert SYNOPSIS in out
    assert POSITIONAL_SYNOPSIS in out
    assert not err


def test_parse_help_request(capsys):
    with pytest.raises(SystemExit) as err:
        options = cli.parse_request(['-h'])
        assert options == 0  # type: ignore
    out, err = capsys.readouterr()
    assert SYNOPSIS in out
    assert POSITIONAL_SYNOPSIS in out
    assert 'Version ranges (Finnish: versioalueet)' in out
    assert 'show this help message and exit' in out
    assert not err


def test_main_version_without_version_ranges(capsys, caplog):
    caplog.set_level(logging.WARNING)
    cli.main(['42'])
    out, err = capsys.readouterr()
    assert not out
    message_part = '42'
    assert message_part in caplog.text
