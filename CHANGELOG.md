# Change Log
All notable changes to this project will be documented in this file.

## 1.4.0 - 2023-05-31
### Added
- Added new dereferencing function to current openapi-spec 0.12 library.

### Changed
- Instead of running create_spec at runtime, a spec is created and spec download time, made into a dict, and we use that at runtime.
- Updates to accommodate these changes.

### Removed
- Spec are no longer created at initialization, only need to be loaded. 7 seconds -> .04 seconds.


## 1.3.4 - 2023-05-16
### Added
- No change.

### Changed
- Update spec for app and authenticator.
- Nathan added json serializer for tapis result object serialization to dictionary.

### Removed
- No change.


## 1.3.3 - 2023-04-18
### Added
- No change.

### Changed
- Update spec for files.

### Removed
- No change.


## 1.3.2 - 2023-04-14
### Added
- No change.

### Changed
- Added support for requests with multipart/form-data headers. File uploading/etc now working natively.
- t.files.insert is now usable.
- Updating specs for systems, apps, workflows, notifications.

### Removed
- No change.


## 1.3.1 - 2023-03-23
### Added
- No change.

### Changed
- Updating spec for files.

### Removed
- No change.


## 1.3.0 - 2023-03-22
### Added
- No change.

### Changed
- Updating specs for streams, pgrest, jobs, apps, notifications.

### Removed
- No change.


## 1.2.20 - 2023-01-26
### Added
- Updated __version__ and will keep it up to date with true version.

### Changed
- No change.

### Removed
- No change.


## 1.2.19 - 2023-01-09
### Added
- No change.

### Changed
- Updating specs for workflows.

### Removed
- No change.


## 1.2.18 - 2022-12-13
### Added
- No change.

### Changed
- Updating specs for files, systems, pods, jobs, apps, workflows.

### Removed
- No change.


## 1.2.17 - 2022-10-28
### Added
- Added test to test running resource_set='local'.

### Changed
- Fixed bug when running resource_set='local'.

### Removed
- No change.


## 1.2.16 - 2022-10-27
### Added
- No change.

### Changed
- Updating spec for jobs.

### Removed
- No change.


## 1.2.15 - 2022-10-26
### Added
- Adding notifications spec.

### Changed
- Changing files url. Updating workflows and files spec.

### Removed
- No change.


## 1.2.14 - 2022-10-25
### Added
- No change.

### Changed
- Updating specs for sk, systems, jobs, apps, workflows.

### Removed
- No change.


## 1.2.13 - 2022-10-18
### Added
- No change.

### Changed
- Updating specs for pods, workflows.

### Removed
- No change.


## 1.2.12 - 2022-10-13
### Added
- Nathan - Added new error message response code/statuses to Tapipy __call__ and upload.

### Changed
- Updated the specs for authenticator, workflows, systems, tokens, app.

### Removed
- No change.


## 1.2.11 - 2022-09-27
### Added
- Add support for specifying arbitrary query parameters via the `_tapis_query_parameters` argument and headers
  va the `_tapis_headers` argument (see issue #30).

### Changed
- The use of the `headers` argument for passing arbitrary headers has been deprecated in favor of `_tapis_headers`.

### Removed
- No change.


## 1.2.10 - 2022-09-07
### Added
- No change.

### Changed
- Requirement for openapi-spec-validator added to toml.

### Removed
- No change.


## 1.2.9 - 2022-09-07
### Added
- Added new specs for systems and apps.

### Changed
- Fixed lacking requirement in test docker-compose.

### Removed
- No change.


## 1.2.8 - 2022-08-24
### Added
- Added new specs for authenticator, workflows, and one other one.
- Added workflows to code.

### Changed
- Fixed spec creation script.

### Removed
- No change.


## 1.2.7 - 2022-07-25
### Added
- No change.

### Changed
- Updated systems and jobs specs.

### Removed
- No change.


## 1.2.6 - 2022-06-22
### Added
- No change.

### Changed
- Nathan Freeman added claims to jwt and proper initializing jwt when jwt received from str and not TapisResult.

### Removed
- No change.


## 1.2.5 - 2022-06-16
### Added
- No change.
- Added test to ensure you can create a Tapis client with solely client_id, client_key, and refresh_token.

### Changed
- Fix, access_token was always being set to jwt (usually None) on instantiation. 

### Removed
- No change.


## 1.2.4 - 2022-06-16
### Added
- Added test for refresh_tokens.

### Changed
- Added back in set_refresh_tokens(). Got deleted when switching to plugins architecture.
- Updated spec for Pods.

### Removed
- No change.


## 1.2.3 - 2022-06-15
### Added
- Added Pods spec.

### Changed
- Updated specs for Systems.

### Removed
- No change.


## 1.2.2 - 2022-06-07
### Added
- Updating specs for authenticator, sk, streams, systems, tokens, jobs.

### Changed
- No change.

### Removed
- No change.


## 1.2.1 - 2022-05-20
### Added
- No change

### Changed
- Broadened dependencies allowed. Tapipy compatible with Python 3.10 now.
- Tests now only cover tapipy. Not tapisservice. Tapisservice tests done by tapipy-tapisservice repo.
- Tests now use user account.
- Test user and password configured in Makefile now.

### Removed
- No change.


## 1.2.0 - 2022-05-19
### Added
- No change

### Changed
- Added compatibility for PyJWT > 2.0.0. Still only requiring > 1.7.1.
- Fixed tests for Tapipy to include plugins rework.
- Tests now using pip install of tapisservice plugin.

### Removed
- No change.


## 1.1.1 - 2022-04-16
### Added
- No change

### Changed
- This update converts tapipy to using a plugins architecture. In particular, functionality related to tapis services
has been moved to the tapipy-tapisservice repository, in the form of a plugin.

### Removed
- No change.


## 1.1.0 - 2022-04-04 (target)
### Added
- No change.

### Changed
- Bug fix. tapipy.actors.get_client() wrongly instantiated with jwt rather than access_token.
- Setting jwt in Tapis object now also sets access_token (jwt is an alias for access_token).
- Fix for create_token test - basic_auth should be false to create tokens on other tenants.

### Removed
- No change.


## 1.0.7 - 2022-02-08 (target)
### Added
- No change.

### Changed
- Updating spec for actors.

### Removed
- No change.


## 1.0.6 - 2022-02-02 (target)
### Added
- No change.

### Changed
- Updating spec for actors, streams, app, systems.

### Removed
- No change.


## 1.0.5 - 2021-12-20 (target)
### Added
- No change.

### Changed
- Updating spec for PgREST and meta.
- Fixed bug in receiving int or float types as parameter values in '__call__'

### Removed
- No change.


## 1.0.4 - 2021-12-20 (target)
### Added
- No change.

### Changed
- Updating spec for PgREST.

### Removed
- No change.


## 1.0.3 - 2021-12-01 (target)
### Added
- No change.

### Changed
- Updating specs for authenticator, files, sk, systems, jobs, apps.

### Removed
- No change.


## 1.0.2 - 2021-10-20 (target)
### Added
- No change.

### Changed
- Downgraded jsonschema version due to slowdown caused by 4.0+ releases in spec parsing.

### Removed
- No change.


## 1.0.1 - 2021-09-29 (target)
### Added
- No change.

### Changed
- Rebuild to ensure new specs working (PgREST was using previous spec still).

### Removed
- No change.


## 1.0.0 - 2021-09-28 (target)
### Added
- No change.

### Changed
- Updating specs for pgrest, apps, jobs, tokens.

### Removed
- No change.


## Tapis V3 in Production, moving from 0.3.34 -> 1.0.0


## 0.3.34 - 2021-09-20 (target)
### Added
- No change.

### Changed
- Bugfix for debug prints.

### Removed
- No change.


## 0.3.33 - 2021-09-20 (target)
### Added
- Added "debug_prints" flag to Tapipy object to get rid of some annoying print statements. Purely QOL.

### Changed
- No change.

### Removed
- No change.


## 0.3.32 - 2021-08-06 (target)
### Added
- No change.

### Changed
- Syntax fix.

### Removed
- No change.


## 0.3.31 - 2021-08-06 (target)
### Added
- No change.

### Changed
- No change.

### Removed
- Remove test exception.


## 0.3.30 - 2021-08-06 (target)
### Added
- No change.

### Changed
- Updating specs for systems, apps.

### Removed
- No change.


## 0.3.29 - 2021-07-22 (target)
### Added
- No change.

### Changed
- Updating specs for streams.

### Removed
- No change.


## 0.3.28 - 2021-07-22 (target)
### Added
- No change.

### Changed
- Updating specs for sk, streams, systems, tenants, jobs, apps.

### Removed
- No change.


## 0.3.27 - 2021-06-29 (target)
### Added
- Added `resource_dicts` to Tapis object. This allows you to view the specs in dictionary form that Tapipy is using.

### Changed
- No change.

### Removed
- No change.


## 0.3.26 - 2021-06-23 (target)
### Added
- No change.

### Changed
- Changed multiprocessing to threads library.

### Removed
- No change.


## 0.3.25 - 2021-06-23 (target)
### Added
- No change.

### Changed
- Bug fixes in __call__
- Bug fix in `add_claims_to_token` function.

### Removed
- No change.


## 0.3.24 - 2021-06-22 (target)
### Added
- No change.

### Changed
- Updating apps, authenticator, and systems specs.

### Removed
- No change.


## 0.3.23 - 2021-06-22 (target)
### Added
- No change.

### Changed
- Utilizing threads library rather than multiprocessing for spec downloading.

### Removed
- No change.


## 0.3.22 - 2021-06-03 (target)
### Added
- Adding set of staging specs accessible with 'resource_set' = 'staging'.

### Changed
- No change.

### Removed
- No change.


## 0.3.21 - 2021-05-28 (target)
### Added
- No change.

### Changed
- Updating systems and apps specs.

### Removed
- No change.


## 0.3.20 - 2021-05-20 (target)
### Added
- Adding back support for inputted access/refresh tokens at Tapis() initialization.

### Changed
- No change.

### Removed
- No change.


## 0.3.19 - 2021-05-17 (target)
### Added
- No change.

### Changed
- Updating streams spec.

### Removed
- No change.


## 0.3.18 - 2021-04-22 (target)
### Added
- No change.

### Changed
- Updating apps pickled spec.

### Removed
- No change.


## 0.3.17 - 2021-04-22 (target)
### Added
- Added apps service.

### Changed
- Updating files to account for apps service spec.

### Removed
- No change.


## 0.3.16 - 2021-04-20 (target)
### Added
- No change.

### Changed
- Updated specs for files, systems, sk, and jobs.

### Removed
- No change.


## 0.3.15 - 2021-04-08 (target)
### Added
- Jobs spec added.
- Added a Makefile for building, pulling specs, and testing. (Note: Should add way to update version number and add Changelog)

### Changed
- Changed some scripts for ease of use.

### Removed
- No change.


## 0.3.14 - 2021-03-26 (target)
### Added
- No change.

### Changed
- Bug fix.

### Removed
- No change.


## 0.3.13 - 2021-03-26 (target)
### Added
- Adding pgrest spec files

### Changed
- No change.

### Removed
- No change.

## 0.3.12 - 2021-03-16 (target)
### Added
- No change.

### Changed
- Updating files pickled spec.

### Removed
- No change.


## 0.3.11 - 2021-03-16 (target)
### Added
- No change.

### Changed
- Bumping cryptography.

### Removed
- No change.


## 0.3.10 - 2021-03-16 (target)
### Added
- No change.

### Changed
- Updating systems resource urls and resource/spec.

### Removed
- Removing cyptography package as it was had security flaws and was not used.


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
