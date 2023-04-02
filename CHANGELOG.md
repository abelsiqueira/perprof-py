# Changelog

All notable changes to this project will be documented in this file.
Internal changes will frequently not be included here.

The format is based on [Keep a Changelog],
and this project adheres to [Semantic Versioning].

## [Unreleased]

### Added

- Class `solver_data.SolverData`, which stores a single solver information.
- Class `profile_data.ProfileData`, which stores the basic performance profile data.

### Changed

- Allow PyYAML 0.6.0
- Add upper bounds to dependency versions

## [1.1.3] - 2023-03-21

### Added

- Constraints on the versions of packages.
- CITATION.cff
- Docker image

### Changed

- Package name is now perprof-py because of name clashes in PyPI.

### Removed

- Support for Python < 3.7

### Fixed

- Compatible with Matplotlib 3

## [1.1.2] - 2017-06-25

This was too long before we had a CHANGELOG, so the changes were not kept.
Please check the commit list.

## [1.1.1] - 2015-08-31

This was the version used in the [JORS paper].

This was too long before we had a CHANGELOG, so the changes were not kept.
Please check the commit list.

## [1.1.0] - 2015-05-30

This was too long before we had a CHANGELOG, so the changes were not kept.
Please check the commit list.

## [1.0.0] - 2014-08-20

- initial release

<!-- Links -->
[keep a changelog]: https://keepachangelog.com/en/1.0.0/
[semantic versioning]: https://semver.org/spec/v2.0.0.html
[JORS paper]: https://openresearchsoftware.metajnl.com/articles/10.5334/jors.81/

<!-- Versions -->
[unreleased]: https://github.com/abelsiqueira/perprof-py/compare/v1.1.3...HEAD
[1.1.3]: https://github.com/abelsiqueira/perprof-py/compare/v1.1.2...v1.1.3
[1.1.2]: https://github.com/abelsiqueira/perprof-py/compare/v1.1.1...v1.1.2
[1.1.1]: https://github.com/abelsiqueira/perprof-py/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/abelsiqueira/perprof-py/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/abelsiqueira/perprof-py/releases/tag/v1.0.0
