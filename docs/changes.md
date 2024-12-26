# Changelog

2024.12.26
:    Fixed meta data, amended capabilities, and optimized version ranges parser
- added a version option for the library / package
- added conditional validation of aby version arguments given
- added positional version argument(s) to complete command line interface for version inclusion
- added the python 3.13 interoperability claim (untested)
- amended documentation on usage and API
- ensured the normalize method works as intended (still maybe add a free function)
- fixed meta data that caused an implementation less package publication
- harmonized the order of short and long options for the help page
- moved from replace to classic python split-join idiom for un-spacing
- updated test (for now with many copies of the changed brittle usage tagline)


2024.12.25
:    Initial release on PyPI allowing some version ranges validation already
- warning: this release was broken as no implementation was included (cf. 2024.12.26 for the fix)
