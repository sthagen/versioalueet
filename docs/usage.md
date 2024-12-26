# Usage

## Help

```console
❯ versioalueet
usage: versioalueet [-h] [-q] [-v] [-V] [-r VERSION_RANGES] [versions ...]

Version ranges (Finnish: versioalueet).

positional arguments:
  versions              version(s) to test against version ranges for inclusion (default: '')

options:
  -h, --help            show this help message and exit
  -q, --quiet           work as quiet as possible (default: False)
  -v, --verbose         work logging more information along the way (default: False)
  -V, --version-of-lib  show the library / package version and exit (default: False)
  -r VERSION_RANGES, --version-ranges VERSION_RANGES
                        version ranges as valid vers string (default: '')
```

## Interactive Examples

A failing version ranges string validation (a version constraint with a comparator but no version):

```console
❯ VERSIOALUEET_DEBUG= versioalueet -vr 'vers:pypi/<'
2024-12-26T11:48:28.149150+00:00 ERROR [VERSIOALUEET]: empty version detected
```

Same with debug-mode activated:

```console
❯ VERSIOALUEET_DEBUG=Y versioalueet -vr 'vers:pypi/<'
2024-12-26T11:48:17.674762+00:00 DEBUG [VERSIOALUEET]: DEBUG=True, ENCODING='utf-8', ENCODING_ERRORS_POLICY='ignore'
2024-12-26T11:48:17.674998+00:00 DEBUG [VERSIOALUEET]: Model = {\
'received': 'vers:pypi/<', 'uri-scheme': 'vers', 'versioning-scheme': 'pypi', 'error': 'empty version detected'}
2024-12-26T11:48:17.675023+00:00 ERROR [VERSIOALUEET]: empty version detected
```

Quiet or silent mode only providing a non-zero exit code from the process (using another invalid version range as example):

```console
❯ versioalueet -qr 'vers:pypi/<' || echo $?
1
```

Some benchmarking of use versus abuse case on process level (randomly distracted Mac mini with Apple M1 CPU and macOS Sonoma 14.7.2 (23H311)):

```console
❯ hyperfine "versioalueet -qr 'vers:pypi/42'" "versioalueet -qr ''" --warmup 13 --ignore-failure
Benchmark 1: versioalueet -qr 'vers:pypi/42'
  Time (mean ± σ):     108.4 ms ±   5.4 ms    [User: 30.2 ms, System: 11.4 ms]
  Range (min … max):    98.9 ms … 117.0 ms    24 runs

Benchmark 2: versioalueet -qr ''
  Time (mean ± σ):     103.9 ms ±   3.5 ms    [User: 29.5 ms, System: 11.1 ms]
  Range (min … max):   100.3 ms … 116.3 ms    27 runs

  Warning: Ignoring non-zero exit code.

Summary
  versioalueet -qr '' ran
    1.04 ± 0.06 times faster than versioalueet -qr 'vers:pypi/42'
```

Above run was using [hyperfine](https://crates.io/crates/hyperfine) version 1.19.0.

### Doctest from Implementation

Assuming the `site-packages` folder is below `/some/install/` (and removing some noise):

```console
❯ python -m doctest /some/install/site-packages/versioalueet/api.py --fail-fast 2>&1 | cut -c34- && echo "OK"
ERROR [VERSIOALUEET]: versions must be unique across all version constraints
ERROR [VERSIOALUEET]: empty version detected
ERROR [VERSIOALUEET]: empty version detected
ERROR [VERSIOALUEET]: version range must start with the URI scheme vers
ERROR [VERSIOALUEET]: empty version detected
ERROR [VERSIOALUEET]: version constraints must be non empty
ERROR [VERSIOALUEET]: some problem
OK
```

Same tests run but in verbose mode:

```console
❯ python -m doctest /some/install/site-packages/versioalueet/api.py --verbose && echo "OK"
Trying:
    version_ranges = VersionRanges('vers:pypi/|1.2.3|||||')
Expecting nothing
ok
Trying:
    assert version_ranges.normalize() == 'vers:pypi/1.2.3'
Expecting nothing
ok
Trying:
    lc_url_encoded = '1%3e2%3c3%3d4%215%2a6%7c7'
Expecting nothing
ok
Trying:
    uc_url_encoded = '1%3E2%3C3%3D4%215%2A6%7C7'
Expecting nothing
ok
Trying:
    version_decoded = '1>2<3=4!5*6|7'
Expecting nothing
ok
Trying:
    triplicated = '|'.join((lc_url_encoded, uc_url_encoded, version_decoded))
Expecting nothing
ok
Trying:
    version_ranges = VersionRanges(f'vers:pypi/{triplicated}')
Expecting nothing
2024-12-26T11:59:39.869203+00:00 ERROR [VERSIOALUEET]: versions must be unique across all version constraints
ok
Trying:
    assert 'unique' in version_ranges.model.get('error', '')
Expecting nothing
ok
Trying:
    hidden_emopty_version = 'vers:pypi/|1.2.3|>||||'
Expecting nothing
ok
Trying:
    version_ranges = VersionRanges(hidden_emopty_version)
Expecting nothing
2024-12-26T11:59:39.869525+00:00 ERROR [VERSIOALUEET]: empty version detected
ok
Trying:
    assert 'empty version detected' in version_ranges.model.get('error', '')
Expecting nothing
ok
Trying:
    maybe_43 = 'vers:pypi/<44|>42'
Expecting nothing
ok
Trying:
    version_ranges = VersionRanges(maybe_43)
Expecting nothing
ok
Trying:
    assert 'vers:pypi/>42|<44' == str(version_ranges)
Expecting nothing
ok
Trying:
    a_version = 'vers:pypi/|1.2.3||||'
Expecting nothing
ok
Trying:
    version_ranges = VersionRanges(a_version)
Expecting nothing
ok
Trying:
    assert not version_ranges.model.get('error', '')
Expecting nothing
ok
Trying:
    version_ranges.normalize()
Expecting:
    'vers:pypi/1.2.3'
ok
Trying:
    hidden_emopty_version = 'vers:pypi/|1.2.3|>||||'
Expecting nothing
ok
Trying:
    vr = VersionRanges('vers:abc/42')
Expecting nothing
ok
Trying:
    vr.normalize(hidden_emopty_version)
Expecting:
    'ERROR:<empty version detected>'
2024-12-26T11:59:39.869797+00:00 ERROR [VERSIOALUEET]: empty version detected
ok
Trying:
    _parse_uri_scheme('VERS:WRONG/YES', model={'received': 'VERS:WRONG/YES', 'uri-scheme': 'vers'})
Expecting:
    (True, '')
2024-12-26T11:59:39.869898+00:00 ERROR [VERSIOALUEET]: version range must start with the URI scheme vers
ok
Trying:
    _parse_version_constraint_pairs(['1', '3', '=4', '2', '>=6'], model={})
Expecting:
    (False, [('1', ''), ('2', ''), ('3', ''), ('4', '='), ('6', '>=')])
ok
Trying:
    model = {}
Expecting nothing
ok
Trying:
    _parse_version_constraint_pairs(['1', '', '2'], model=model)
Expecting:
    (True, [])
2024-12-26T11:59:39.870010+00:00 ERROR [VERSIOALUEET]: empty version detected
ok
Trying:
    assert 'empty' in model.get('error', '')
Expecting nothing
ok
Trying:
    model = {'received': 'vers:pypi/*', 'uri-scheme': 'vers', 'versioning-scheme': 'pypi'}
Expecting nothing
ok
Trying:
    _parse_version_scheme('pypi/*', model=model)
Expecting:
    (False, '*')
ok
Trying:
    model = {'received': 'vers:pypi/', 'uri-scheme': 'vers', 'versioning-scheme': 'pypi'}
Expecting nothing
ok
Trying:
    _parse_version_scheme('pypi/', model=model)
Expecting:
    (True, '')
2024-12-26T11:59:39.870147+00:00 ERROR [VERSIOALUEET]: version constraints must be non empty
ok
Trying:
    _split_version_constraints('13', {})
Expecting:
    (False, ['13'])
ok
Trying:
    _split_version_constraints('|||||42||', {})
Expecting:
    (False, ['42'])
ok
Trying:
    _split_version_constraints('|1|2|3|=4||>=6', {})
Expecting:
    (False, ['1', '2', '3', '=4', '>=6'])
ok
Trying:
    DEBUG = True
Expecting nothing
ok
Trying:
    model = {'received': 'no:thing'}
Expecting nothing
ok
Trying:
    fail('some problem', model=model)
Expecting:
    True
2024-12-26T11:59:39.870300+00:00 ERROR [VERSIOALUEET]: some problem
ok
2 items had no tests:
    api.VersionRanges.parse
    api.main
10 items passed all tests:
   2 tests in api
   6 tests in api.VersionRanges
   3 tests in api.VersionRanges.__init__
   3 tests in api.VersionRanges.__repr__
   7 tests in api.VersionRanges.normalize
   1 tests in api._parse_uri_scheme
   4 tests in api._parse_version_constraint_pairs
   4 tests in api._parse_version_scheme
   3 tests in api._split_version_constraints
   3 tests in api.fail
36 tests in 12 items.
36 passed and 0 failed.
Test passed.
OK
```
