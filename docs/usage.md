# Usage

## Help

```console
❯ versioalueet
usage: versioalueet [-h] [-q] [-v] [-d] [-R] [-V] [-r VERSION_RANGES] [versions ...]

Version ranges (Finnish: versioalueet).

positional arguments:
  versions              version(s) to test against version ranges for inclusion (default: '')

options:
  -h, --help            show this help message and exit
  -q, --quiet           work as quiet as possible (default: False)
  -v, --verbose         work logging more information along the way (default: False)
  -d, --debug           provide debug level information (default: False)
  -R, --report-environment
                        report the runtime environment in JSON format (default: False)
  -V, --version-of-lib  show the library / package version and exit (default: False)
  -r VERSION_RANGES, --version-ranges VERSION_RANGES
                        version ranges as valid vers string (default: '')
```

## Interactive Examples

A failing version ranges string validation (a version constraint with a comparator but no version):

```bash
❯ VERSIOALUEET_DEBUG= versioalueet -vr 'vers:pypi/<'
2025-01-08T05:59:44.688727+00:00 ERROR [VERSIOALUEET]: empty version detected
```

Same with debug-mode activated (merging both output streams and cutting off the timestamp prefixes of the output lines):

```console
❯ VERSIOALUEET_DEBUG=Y versioalueet -vr 'vers:pypi/<' 2>&1 | cut -c34-
DEBUG [VERSIOALUEET]: library-env: debug-mode=True, quiet-mode=False, verbose-mode=True, version=2025.1.8+parent.g03f55e57, encoding=utf-8, encoding-errors-policy=ignore
DEBUG [VERSIOALUEET]: interpreter-env: exec-prefix=/some/python/install-or-virtualenv, exec-path=/some/python/install-or-virtualenv/bin/python3.12
DEBUG [VERSIOALUEET]: interpreter-impl: impl-name=cpython, version(major=3, minor=12, micro=4, releaselevel=final, serial=0)
DEBUG [VERSIOALUEET]: interpreter-flags: hash_randomization=1, int_max_str_digits=4300
DEBUG [VERSIOALUEET]: os-env: node-id=c79891e5-aabf-3a83-95b9-588edcd8327f, machine-type=arm64, platform-code=macOS-14.7.2, platform_release=23.6.0
DEBUG [VERSIOALUEET]: os-uname: os-sysname=Darwin, os-nodename=helsinki.home, os-version=Darwin Kernel Version 23.6.0: Fri Nov 15 15:13:56 PST 2024; root:xnu-10063.141.1.702.7~1/RELEASE_ARM64_T8103
DEBUG [VERSIOALUEET]: os-resource-usage: ru-maxrss-mbytes-kbytes-precision=16.297, ru-utime-msec-usec-precision=38.371, ru-stime-msec-usec-precision=32.527, ru-minflt=3127, ru-majflt=341, ru-inblock=0, ru-outblock=0, ru_nvcsw=325, ru_nivcsw=540
DEBUG [VERSIOALUEET]: os-cpu-resources: os-cpu-present=8, os-cpu-available=-1
ERROR [VERSIOALUEET]: empty version detected
```

Quiet (or silent) mode only provides the validation result in the exit code from the process (using another invalid version range as example):

```bash
❯ versioalueet -qr 'vers:pypi/<' || echo $?
1
```

Or, a valid example (yields the normalized verion ranges on standard out and a successful exit code i.e. zero):

```bash
❯ versioalueet -qr 'vers:pypi/*'
vers:pypi/*
❯ echo $?
0
```

Reporting only the process environment (including python and library information):

```bash
❯ versioalueet -R
```

The above yields the following valid JSON (on some randomly selected machine):

```json
{
  "library-env": {
    "debug-mode": false,
    "quiet-mode": false,
    "verbose-mode": false,
    "version": "2025.1.8+parent.g03f55e57",
    "encoding": "utf-8",
    "encoding-errors-policy": "ignore"
  },
  "interpreter-env": {
    "exec-prefix": "/some/python/install-or-virtualenv",
    "exec-path": "/some/python/install-or-virtualenv/bin/python3.12"
  },
  "interpreter-impl": {
    "impl-name": "cpython",
    "version": {
      "major": 3,
      "minor": 12,
      "micro": 4,
      "releaselevel": "final",
      "serial": 0
    }
  },
  "interpreter-flags": {
    "hash_randomization": 1,
    "int_max_str_digits": 4300
  },
  "os-env": {
    "node-id": "807d4647-bb4f-3886-b29b-67cbc762ab28",
    "machine-type": "arm64",
    "platform-code": "macOS-14.7.2",
    "platform_release": "23.6.0"
  },
  "os-uname": {
    "os-sysname": "Darwin",
    "os-nodename": "helsinki.local",
    "os-version": "Darwin Kernel Version 23.6.0: Fri Nov 15 15:13:56 PST 2024; root:xnu-10063.141.1.702.7~1/RELEASE_ARM64_T8103"
  },
  "os-resource-usage": {
    "ru-maxrss-mbytes-kbytes-precision": 14.469,
    "ru-utime-msec-usec-precision": 35.519,
    "ru-stime-msec-usec-precision": 21.395,
    "ru-minflt": 2762,
    "ru-majflt": 13,
    "ru-inblock": 0,
    "ru-outblock": 0,
    "ru_nvcsw": 0,
    "ru_nivcsw": 39
  },
  "os-cpu-resources": {
    "os-cpu-present": 8,
    "os-cpu-available": -1
  }
}
```

Some benchmarking of success versus failure validation cases on process level (randomly distracted Mac mini with Apple M1 CPU and macOS Sonoma 14.7.2 (23H311)):

| Command                                                                  |   Mean [ms] | Min [ms] | Max [ms] |    Relative |
|:-------------------------------------------------------------------------|------------:|---------:|---------:|:------------|
| `versioalueet -qr 'vers:pypi/42'`                                        | 119.0 ± 1.8 |    117.0 |    126.1 | 1.00 ± 0.02 |
| `versioalueet -qr ''`                                                    | 118.5 ± 0.9 |    116.6 |    120.3 | 1.00        |
| `versioalueet -qr 'vers:golang/>v0\|>=v1\|v2\|&lt;v3\|v4\|&lt;v5\|>=v6'` | 118.9 ± 1.0 |    117.1 |    121.3 | 1.00 ± 0.01 |

Table: Benchmark of success and failure paths.


| `versioalueet -qr 'vers:pypi/42'` | 119.0 ± 1.8 | 117.0 | 126.1 | 1.00 ± 0.02 |
| `versioalueet -qr ''` | 118.5 ± 0.9 | 116.6 | 120.3 | 1.00 |
| `versioalueet -qr 'vers:golang/>v0\|>=v1\|v2\|<v3\|v4\|<v5\|>=v6'` | 118.9 ± 1.0 | 117.1 | 121.3 | 1.00 ± 0.01 |

```bash
❯ hyperfine "versioalueet -qr 'vers:pypi/42'" "versioalueet -qr ''" "versioalueet -qr 'vers:golang/>v0|>=v1|v2|<v3|v4|<v5|>=v6'"\
  --warmup 13 --ignore-failure --export-markdown foo.md
  Benchmark 1: versioalueet -qr 'vers:pypi/42'
    Time (mean ± σ):     119.0 ms ±   1.8 ms    [User: 30.6 ms, System: 10.8 ms]
    Range (min … max):   117.0 ms … 126.1 ms    24 runs
  
  Benchmark 2: versioalueet -qr ''
    Time (mean ± σ):     118.5 ms ±   0.9 ms    [User: 30.5 ms, System: 10.7 ms]
    Range (min … max):   116.6 ms … 120.3 ms    24 runs
  
    Warning: Ignoring non-zero exit code.
  
  Benchmark 3: versioalueet -qr 'vers:golang/>v0|>=v1|v2|<v3|v4|<v5|>=v6'
    Time (mean ± σ):     118.9 ms ±   1.0 ms    [User: 30.5 ms, System: 10.7 ms]
    Range (min … max):   117.1 ms … 121.3 ms    24 runs
  
  Summary
    versioalueet -qr '' ran
      1.00 ± 0.01 times faster than versioalueet -qr 'vers:golang/>v0|>=v1|v2|<v3|v4|<v5|>=v6'
      1.00 ± 0.02 times faster than versioalueet -qr 'vers:pypi/42'
```

Above run was using [hyperfine](https://crates.io/crates/hyperfine) version 1.19.0 and tested:

```bash
❯ versioalueet --version-of-lib
2025.1.8+parent.g03f55e57
```

### Doctest from Implementation

Assuming the `site-packages` folder is below `/some/install/` (and removing some noise):

```bash
❯ python -m doctest /some/install/site-packages/versioalueet/api.py --fail-fast 2>&1 | cut -c34- && echo "OK"
ERROR [VERSIOALUEET]: versions must be unique across all version constraints
ERROR [VERSIOALUEET]: empty version detected
ERROR [VERSIOALUEET]: empty version detected
ERROR [VERSIOALUEET]: version range must start with the URI scheme vers
ERROR [VERSIOALUEET]: empty version detected
ERROR [VERSIOALUEET]: version constraints must be non empty
ERROR [VERSIOALUEET]: some problem
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
2025-01-08T06:04:34.002849+00:00 ERROR [VERSIOALUEET]: versions must be unique across all version constraints
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
2025-01-08T06:04:34.003441+00:00 ERROR [VERSIOALUEET]: empty version detected
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
    assert "VersionRanges('vers:pypi/>42|<44')" == repr(version_ranges)
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
2025-01-08T06:04:34.003837+00:00 ERROR [VERSIOALUEET]: empty version detected
ok
Trying:
    received = 'vers:golang/>v0|>=v1|v2|<v3|v4|<v5|>=v6'
Expecting nothing
ok
Trying:
    split_up = [('v0', GT), ('v1', GE), ('v2', EQ), ('v3', LT), ('v4', EQ), ('v5', LT), ('v6', GT)]
Expecting nothing
ok
Trying:
    pairs = _optimize_version_constraints(vc_pairs=split_up, model={})
Expecting nothing
ok
Trying:
    pairs
Expecting:
    [('v0', '>'), ('v5', '<'), ('v6', '>')]
ok
Trying:
    _parse_uri_scheme('VERS:WRONG/YES', model={'received': 'VERS:WRONG/YES', 'uri-scheme': 'vers'})
Expecting:
    (True, '')
2025-01-08T06:04:34.004155+00:00 ERROR [VERSIOALUEET]: version range must start with the URI scheme vers
ok
Trying:
    _parse_version_constraint_pairs(['1', '3', '=4', '2', '>=6'], model={})
Expecting:
    (False, [('1', '='), ('2', '='), ('3', '='), ('4', '='), ('6', '>=')])
ok
Trying:
    model = {}
Expecting nothing
ok
Trying:
    _parse_version_constraint_pairs(['1', '', '2'], model=model)
Expecting:
    (True, [])
2025-01-08T06:04:34.004326+00:00 ERROR [VERSIOALUEET]: empty version detected
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
2025-01-08T06:04:34.004490+00:00 ERROR [VERSIOALUEET]: version constraints must be non empty
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
    to_squeeze = [('v0', GT), ('v1', GE), ('v2', EQ), ('v3', LT), ('v4', EQ), ('v5', LT), ('v6', GT)]
Expecting nothing
ok
Trying:
    collected = _squeeze_ranges(to_squeeze)
Expecting nothing
ok
Trying:
    collected
Expecting:
    [('v0', '>'), ('v5', '<'), ('v6', '>')]
ok
Trying:
    model = {'received': 'no:thing'}
Expecting nothing
ok
Trying:
    fail('some problem', model=model)
Expecting:
    True
2025-01-08T06:04:34.004779+00:00 ERROR [VERSIOALUEET]: some problem
ok
Trying:
    model = {'received': 'no:thing'}
Expecting nothing
ok
Trying:
    fail('some problem', model=model, debug=True)
Expecting:
    True
2025-01-08T06:04:34.004847+00:00 ERROR [VERSIOALUEET]: some problem
ok
4 items had no tests:
    api.VersionRanges.__eq__
    api.VersionRanges.__hash__
    api.VersionRanges.parse
    api.main
13 items passed all tests:
   2 tests in api
   6 tests in api.VersionRanges
   3 tests in api.VersionRanges.__init__
   3 tests in api.VersionRanges.__repr__
   3 tests in api.VersionRanges.__str__
   7 tests in api.VersionRanges.normalize
   4 tests in api._optimize_version_constraints
   1 tests in api._parse_uri_scheme
   4 tests in api._parse_version_constraint_pairs
   4 tests in api._parse_version_scheme
   3 tests in api._split_version_constraints
   3 tests in api._squeeze_ranges
   4 tests in api.fail
47 tests in 17 items.
47 passed and 0 failed.
Test passed.
OK
```
