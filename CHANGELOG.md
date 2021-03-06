# Change Log
All notable changes to this project will be documented in this file.

## 0.3.9 - 2021-03-12 (target)
### Added
- No change.

### Changed
- Lowering openapi-core version requirement. 0.13.0 slightly hurts some services.

### Removed
- No change.


## 0.3.8 - 2021-03-12 (target)
### Added
- No change.

### Changed
- Properly added actors pickled file

### Removed
- No change.


## 0.3.7 - 2021-03-12 (target)
### Added
- No change.

### Changed
- Changed actors spec and pickled files

### Removed
- No change.

## 0.3.6 - 2021-03-12 (target)
### Added
- No change.

### Changed
- Bug fix

### Removed
- No change.

## 0.3.5 - 2021-03-11 (target)
### Added
- No change.

### Changed
- Support for x-www-form-urlencoded

### Removed
- No change.

## 0.3.4 - 2021-XX-XX (target)
### Added
- No change.

### Changed
- Updated files spec yaml and pickled files.

### Removed
- No change.

## 0.3.3 - 2021-01-28 (target)
### Added
- No change.

### Changed
- Updated files spec yaml and pickled files.

### Removed
- No change.

## 0.3.2 - 2021-01-12 (target)
### Added
- No change.

### Changed
- Up'ed compatibility with older version of openapi_core.

### Removed
- No change.


## 0.3.1 - 2020-12-11 (target)
### Added
- No change.

### Changed
- Updated tapipy to work with 'admin' tenant at primary site rather than 'master'.
- Also updated tests.

### Removed
- No change.

## 0.3.0 - 2020-12-1 (target)
### Added
- Added sites integration for Tapis v3.
- Added tests for sites integreation.
- Added a set of local specs under 'local'
- Many helper functions added for sites ease-of-use.

### Changed
- Update to certifi version to alleviate ssl issues.
- Updatetd some resources in the resources folder.
- Updated pickled specs to the most up to date prod specs.

### Removed
- No change.

## 0.2.11 - 2020-10-13 (target)
### Added
- Adding the ability to load local spec files.

### Changed
- No change.

### Removed
- No change.

## 0.2.10 - 2020-10-13 (target)
### Added
- Adding default falling back to prod spec if there was an error reading in other spec.

### Changed
- Bug fixes.
- Changed logs to be much more readable.

### Removed
- No change.

## 0.2.9 - 2020-10-13 (target)
### Added
- No change.

### Changed
- Bug fixes.

### Removed
- No change.

## 0.2.8 - 2020-10-13 (target)
### Added
- No change.

### Changed
- Bug fix, making custom pickled files use protocol 4 as well.

### Removed
- No change.

## 0.2.8 - 2020-10-13 (target)
### Added
- No change.

### Changed
- All pickled files will now use pickle.protocol 4.

### Removed
- No change.

## 0.2.7 - 2020-10-13 (target)
### Added
- No change.

### Changed
- Updated SK spec pickled file (again).
- Modified script to create pickled files.

### Removed
- No change.

## 0.2.6 - 2020-10-9 (target)
### Added
- No change.

### Changed
- Updated SK spec pickled file.

### Removed
- No change.

## 0.2.5 - 2020-9-14 (target)
### Added
- No change.

### Changed
- Bug fix to solve tenant cache not being filled initially issue.

### Removed
- No change.

## 0.2.4 - 2020-9-4 (target)
### Added
- Added pickling, multithreading, additional options to download files, and speed improvements.
- Added back module level initialization.

### Changed
- Changed the way specs are loaded. Now using pickled files and unpickling those files to load in specs for speed.

### Removed
- No change.

## 0.2.3 - 2020-11-20 (target)
### Added
- Configurable specs. There is now the option of a dev or master set of specs along with an option to specify custom specs when creating a Tapis object.

### Changed
- No change.

### Removed
- No change.

## 0.2.0 - 2019-11-20 (target)
### Added
- Continuing in Alpha. Added PyPi package for ease of use.

### Changed
- Bug fixes.

### Removed
- No change.


## 0.1.0 - 2019-11-20 (target)
### Added
- Initial alpha release.

### Changed
- No change.

### Removed
- No change.
