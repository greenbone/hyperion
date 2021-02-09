# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

For detailed code changes, please visit
https://github.com/greenbone/hyperion/commits/master
or get the entire source code repository and view log history:

```sh
$ git clone https://github.com/greenbone/hyperion.git
$ cd hyperion && git log
```

## [Unreleased]
### Added
- Implement `average_duration` for tasks and audits fields. [#14](https://github.com/greenbone/hyperion/pull/14)

### Changed
- For all NVT related Entities we use `id` instead of `oid` now, so every Entity uses `id` now. [#15](https://github.com/greenbone/hyperion/pull/15)
- Use `next` instead of `latest` `python-gvm` version for developement. [#15](https://github.com/greenbone/hyperion/pull/15)
- Removed empty `uuid= ` from `filter_string` in `create_export_by_ids_mutation` [#23](https://github.com/greenbone/hyperion/pull/23) 

### Deprecated
### Removed
### Fixed
- Fixed a problem with NVT `oid` in Notes. [#15](https://github.com/greenbone/hyperion/pull/15)
- Fixed a problem with NVT `oid` in Overrides. [#16](https://github.com/greenbone/hyperion/pull/16)
- Now the `name` field in Overrides and Notes can not be queried. It returned the `name` of the `permission`/`owner` because of `.find()`. Notes/Overrides don't have a name field theirself. [#16](https://github.com/greenbone/hyperion/pull/16)
- Added the `asset_hosts_filter` parameter to `createTarget` mutation [#15](https://github.com/greenbone/hyperion/pull/15)
- Added the `allow_simultaneous_ips` parameter to `createTarget`, `modifyTarget` mutation and `getTarget(s)` queries. [#15](https://github.com/greenbone/hyperion/pull/15)