# Application Programming Interface (API)

Please see below examples and use the python help command to learn about the API.

## Example

```python
❯ python
Python 3.12.4 (main, Jun 23 2024, 15:04:49) [Clang 18.1.7 ] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import json, logging
>>> import versioalueet.api as vers
>>> version_ranges = vers.VersionRanges('vers:pypi/42')
>>> version_ranges
VersionRanges('vers:pypi/42')
>>> str(version_ranges)
'vers:pypi/42'
>>> print(json.dumps(version_ranges.model, indent=2))
{
  "received": "vers:pypi/42",
  "uri-scheme": "vers",
  "versioning-scheme": "pypi",
  "version-constraint-pairs": [
    [
      "42",
      "="
    ]
  ],
  "vc-unequal-pairs": [],
  "vc-other-pairs": [
    [
      "42",
      "="
    ]
  ],
  "version-constraints": [
    "=42"
  ],
  "version-constraints-string-compressed": "42",
  "version-range": "vers:pypi/42"
}
>>> version_ranges.normalize('wrong')
2025-01-08T05:56:23.309204+00:00 ERROR [VERSIOALUEET]: version range must start with the URI scheme vers
'ERROR:<version range must start with the URI scheme vers>'
>>> vers.log.setLevel(logging.CRITICAL)
>>> version_ranges.normalize('wrong')
'ERROR:<version range must start with the URI scheme vers>'
>>> print(json.dumps(version_ranges.model, indent=2))
{
  "received": "wrong",
  "error": "version range must start with the URI scheme vers"
}
>>> version_ranges.normalize('vers:golang/>v0|>=v1|v2|<v3|v4|<v5|>=v6')
'vers:golang/>v0|<v5|>=v6'
>>> print(json.dumps(version_ranges.model, indent=2))
{
  "received": "vers:golang/>v0|>=v1|v2|<v3|v4|<v5|>=v6",
  "uri-scheme": "vers",
  "versioning-scheme": "golang",
  "version-constraint-pairs": [
    [
      "v0",
      ">"
    ],
    [
      "v5",
      "<"
    ],
    [
      "v6",
      ">="
    ]
  ],
  "vc-unequal-pairs": [],
  "vc-other-pairs": [
    [
      "v0",
      ">"
    ],
    [
      "v1",
      ">="
    ],
    [
      "v2",
      "="
    ],
    [
      "v3",
      "<"
    ],
    [
      "v4",
      "="
    ],
    [
      "v5",
      "<"
    ],
    [
      "v6",
      ">="
    ],
    [
      "v6",
      ">="
    ]
  ],
  "version-constraints": [
    ">v0",
    "<v5",
    ">=v6"
  ],
  "version-constraints-string-compressed": ">v0|<v5|>=v6",
  "version-range": "vers:golang/>v0|<v5|>=v6"
}
```

Another example using the help function on the above imported name `vers` in that session:

```python
>>> help(vers)
Help on module versioalueet.api in versioalueet:

NAME
    versioalueet.api - Provide the class VersionRanges for operations on version ranges

DESCRIPTION
    Use case example:

    >>> version_ranges = VersionRanges('vers:pypi/|1.2.3|||||')
    >>> assert version_ranges.normalize() == 'vers:pypi/1.2.3'

CLASSES
    builtins.object
        VersionRanges

    class VersionRanges(builtins.object)
     |  VersionRanges(version_range: str) -> None
     |
     |  Provide operations on version ranges.
     |
     |  Usage examples:
     |
     |      >>> lc_url_encoded = '1%3e2%3c3%3d4%215%2a6%7c7'
     |      >>> uc_url_encoded = '1%3E2%3C3%3D4%215%2A6%7C7'
     |      >>> version_decoded = '1>2<3=4!5*6|7'
     |      >>> triplicated = '|'.join((lc_url_encoded, uc_url_encoded, version_decoded))
     |      >>> version_ranges = VersionRanges(f'vers:pypi/{triplicated}')
     |      >>> assert 'unique' in version_ranges.model.get('error', '')
     |
     |  Methods defined here:
     |
     |  __eq__(self, other: object) -> bool
     |      We define equality per the version ranges.
     |
     |  __hash__(self) -> int
     |      We define our identity per the version range.
     |
     |  __init__(self, version_range: str) -> None
     |      Later alligator.
     |
     |      Usage examples:
     |
     |      >>> hidden_emopty_version = 'vers:pypi/|1.2.3|>||||'
     |      >>> version_ranges = VersionRanges(hidden_emopty_version)
     |      >>> assert 'empty version detected' in version_ranges.model.get('error', '')
     |
     |  __repr__(self) -> str
     |      The version ranges string wrapped in constructor.
     |
     |      Usage examples:
     |
     |      >>> maybe_43 = 'vers:pypi/<44|>42'
     |      >>> version_ranges = VersionRanges(maybe_43)
     |      >>> assert "VersionRanges('vers:pypi/>42|<44')" == repr(version_ranges)
     |
     |  __str__(self) -> str
     |      The version ranges string is what we are.
     |
     |      Usage examples:
     |
     |      >>> maybe_43 = 'vers:pypi/<44|>42'
     |      >>> version_ranges = VersionRanges(maybe_43)
     |      >>> assert 'vers:pypi/>42|<44' == str(version_ranges)
     |
     |  normalize(self, version_range: Optional[str] = None) -> str
     |      Normalize version range.
     |
     |      Usage examples:
     |
     |      >>> a_version = 'vers:pypi/|1.2.3||||'
     |      >>> version_ranges = VersionRanges(a_version)
     |      >>> assert not version_ranges.model.get('error', '')
     |      >>> version_ranges.normalize()
     |      'vers:pypi/1.2.3'
     |
     |      >>> hidden_emopty_version = 'vers:pypi/|1.2.3|>||||'
     |      >>> vr = VersionRanges('vers:abc/42')
     |      >>> vr.normalize(hidden_emopty_version)
     |      'ERROR:<empty version detected>'
     |
     |  parse(self, version_range: str) -> tuple[bool, dict[str, typing.Union[str, list[str], list[tuple[str, str]]]]]
     |      Poor person parser for bootstrap.
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |
     |  __dict__
     |      dictionary for instance variables
     |
     |  __weakref__
     |      list of weak references to the object

FUNCTIONS
    fail(message: str, model: Optional[dict[str, Union[str, list[str], list[tuple[str, str]]]]] = None, debug: bool = False) -> bool
        DRY.

        Usage examples:

        >>> model = {'received': 'no:thing'}
        >>> fail('some problem', model=model)
        True

        >>> model = {'received': 'no:thing'}
        >>> fail('some problem', model=model, debug=True)
        True

    main(options: argparse.Namespace) -> int

DATA
    ASTERISK = '*'
    COLON = ':'
    EQ = '='
    GE = '>='
    GT = '>'
    LE = '<='
    LT = '<'
    ModelType = dict[str, typing.Union[str, list[str], list[tuple[str, str...
    NE = '!='
    NOT = '!'
    PERCENT = '%'
    PIPE = '|'
    SLASH = '/'
    Union = typing.Union
        Union type; Union[X, Y] means either X or Y.

        On Python 3.10 and higher, the | operator
        can also be used to denote unions;
        X | Y means the same thing to the type checker as Union[X, Y].

        To define a union, use e.g. Union[int, str]. Details:
        - The arguments must be types and there must be at least one.
        - None as an argument is a special case and is replaced by
          type(None).
        - Unions of unions are flattened, e.g.::

            assert Union[Union[int, str], float] == Union[int, str, float]

        - Unions of a single argument vanish, e.g.::

            assert Union[int] == int  # The constructor actually returns int

        - Redundant arguments are skipped, e.g.::

            assert Union[int, str, int] == Union[int, str]

        - When comparing unions, the argument order is ignored, e.g.::

            assert Union[int, str] == Union[str, int]

        - You cannot subclass or instantiate a union.
        - You can use Optional[X] as a shorthand for Union[X, None].

    VCPairsType = list[tuple[str, str]]
    log = <Logger VERSIOALUEET (CRITICAL)>

FILE
    /some/install/site-packages/versioalueet/api.py
```
