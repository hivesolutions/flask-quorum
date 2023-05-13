# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

*

### Changed

*

### Fixed

* Incompatibilities with Flask 2.3+ - [#1](https://github.com/hivesolutions/flask-quorum/issues/1)

## [0.8.0] - 2023-01-06

### Added

* Support for the `basic_auth()` method
* Support for the `date.py` module and the `format_delta` function

### Changed

* Renamed repository to `flask-quorum`

## [0.7.0] - 2022-02-04

### Fixed

* Safer check for integer value in Excel

## [0.6.4] - 2021-12-18

### Fixed

* Support for `count_documents` in `PyMongo>=4`

## [0.6.3] - 2021-12-01

### Fixed

* PyMongo version number split operation

## [0.6.2] - 2021-07-31

### Fixed

* Made client side sessions more stable, by patching some global session related configurations

## [0.6.1] - 2021-07-31

### Added

* Support for version printing at startup
