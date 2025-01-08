# Changelog

2025.1.8
:    Fixed the union type annotation ( <https://todo.sr.ht/~sthagen/versioalueet/2> ) and enhanced debug handling
- adapted report to new debug mode management
- added new debug option including tests
- fixed the union type annotation to restore python 3.9 compatibility
- increased test coverage
- VERSIOALUEET_DEBUG environment variable now only used to overwrite the new debug option (which it should not, ahem) to simplify the state machine

2025.1.6
:    Fixed the env report and refactored fail function
- changed fail function signature for testability
- fixed the failing uname report on windows ( <https://todo.sr.ht/~sthagen/versioalueet/1> )

2024.12.30
:    Simplified optimization code, added tests, inceased consistency
- added (real) repr and str methods
- added doctest execution via pytest
- added hash and eq methods to only consider the version range string
- added test for round trip dump to and load from string
- added tests for identity and comparisons
- better names for optimizing and squeezing
- better names for the stencil variables
- extracted function for the squeeze
- guaranteed consistent comparator typed pair containers in model
- removal of unused variables
- removed YAGNI doctest stub
- replaced use of pkg_resources - untested
- simplified function return types
- simplified squeezing algorithm
- updated and amended API and CLI docs
- updated the doctests

2024.12.29
:    Added constraints optimization, unified EQ handling, optimized resource import, and refactored literals of relevance
- added compressed version constraints string to model
- added test cases for version constraints optimization
- added test for normalize with explicit argument
- added tests for version and report capabilities
- aligned an EQ test case to the new unified handling
- cosmetics for help example in API doc
- empty and EQ comparator now are both mapped to EQ in the model
- fixed failed CPSR-coding for README and documentation index
- implemented the specified example algorithm from spec to validate and optimize the contingent version constraints
- map classical two letter abbreviations for comparators to literals to ease maintenance
- name a special indicator for URL encoded version strings
- on output the optimized version constraints string is stripped of all EQ comparators
- replaced the clumsy try-except around resource import with the more natural use of importlib.util.find_spec
- updated version call example

2024.12.27
:    Added environment reporting and updated documentation
- added clarification to example in usage doc
- added custom stylesheet to enlarge content width
- added env module to provide process level environment reports
- added JSON and dict format to report function
- added report capability to CLI
- added some 'pragma: no cover' exemptions
- added tests for the new reporting module (env)
- added validator and optimizer for version constraint pair sets (no implementation yet)
- changed report command to prduce JSON
- fixed failed CPSR-coding of pyproject.toml and requirements.txt
- fixed heading and amended intro of API document
- had to ignore a lot of type errors
- included some import juggling to test dummy values in case the resource module is not available
- no third-party dependencies besides python standard library
- refactored CLI test to enhance maintenance with changing capabilities and changing terminal widths (in the test runs)
- refactored env report into separate module
- refactored unique version validation to be inside version constraint pair parsing
- replaced debug version of an example
- replaced help screen info
- simplified flattening for log format reports (verbose or debug mode)
- split assessment from report
- updated API and CLI usage docs
- updated benchmark to cover latest published version
- updated third-party documentation
- widened the content area in documentation

2024.12.26
:    Fixed meta data, amended capabilities, and optimized version ranges parser
- added a version option for the library / package
- added conditional validation of aby version arguments given
- added positional version argument(s) to complete command line interface for version inclusion
- added the python 3.13 interoperability claim (untested)
- amended documentation on usage and API
- ensured the normalize method works as intended (still maybe add a free function)
- fixed corner case in normalize when receiving explicit empty string
- fixed meta data that caused an implementation less package publication
- harmonized the order of short and long options for the help page
- moved from replace to classic python split-join idiom for un-spacing
- updated test (for now with many copies of the changed brittle usage tagline)


2024.12.25
:    Initial release on PyPI allowing some version ranges validation already
- warning: this release was broken as no implementation was included (cf. 2024.12.26 for the fix)
