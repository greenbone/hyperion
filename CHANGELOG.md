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
- Add `compliance_count` to AuditLastReport [#26](https://github.com/greenbone/hyperion/pull/26)
- Implement `average_duration` for tasks and audits fields. [#14](https://github.com/greenbone/hyperion/pull/14)
- Implement new abstract Class for SecInfo BulkExport by IDs. [#24](https://github.com/greenbone/hyperion/pull/24)
- Add Bulk Export for NVTs. [#25](https://github.com/greenbone/hyperion/pull/25)

### Changed
- Explicitly implement audit subobjects [#26](https://github.com/greenbone/hyperion/pull/26)
- For all NVT related Entities we use `id` instead of `oid` now, so every Entity uses `id` now. [#15](https://github.com/greenbone/hyperion/pull/15)
- Use `next` instead of `latest` `python-gvm` version for developement. [#15](https://github.com/greenbone/hyperion/pull/15)
- Removed empty `uuid= ` from `filter_string` in `create_export_by_ids_mutation` [#23](https://github.com/greenbone/hyperion/pull/23) 
- Changed dependency of `xml` to `lxml` [#27](https://github.com/greenbone/hyperion/pull/27)
- Changed `CVE`s entity so it can parse new-format xml correctly [#29](https://github.com/greenbone/hyperion/pull/29) [#38](https://github.com/greenbone/hyperion/pull/38)
- Refactored `OvalDefinitions` entity [#30](https://github.com/greenbone/hyperion/pull/30)
- Increased coverage for `OvalDefinitions`, `CertBundAdvisories` and `DFNCertAdvisories` entity [#30](https://github.com/greenbone/hyperion/pull/30)
- Added the `deprecatedBy` field to `CPEs` [#51](https://github.com/greenbone/hyperion/pull/51)
- Refactored `NVT` entity, removed complexity and redundant fields [#58](https://github.com/greenbone/hyperion/pull/58)[#60](https://github.com/greenbone/hyperion/pull/60)[#64](https://github.com/greenbone/hyperion/pull/64)

### Deprecated
### Removed
### Fixed
- Fixed a problem with NVT `oid` in Notes. [#15](https://github.com/greenbone/hyperion/pull/15)
- Fixed a problem with NVT `oid` in Overrides. [#16](https://github.com/greenbone/hyperion/pull/16)
- Now the `name` field in Overrides and Notes can not be queried. It returned the `name` of the `permission`/`owner` because of `.find()`. Notes/Overrides don't have a name field theirself. [#16](https://github.com/greenbone/hyperion/pull/16)
- Added the `asset_hosts_filter` parameter to `createTarget` mutation [#15](https://github.com/greenbone/hyperion/pull/15)
- Added the `allow_simultaneous_ips` parameter to `createTarget`, `modifyTarget` mutation and `getTarget(s)` queries. [#15](https://github.com/greenbone/hyperion/pull/15)
- Fixed `FutureWarnings` due to `if x:` -> `if x is not None:` [#27](https://github.com/greenbone/hyperion/pull/27)
- Added missing fields to `CPE` entity [#39](https://github.com/greenbone/hyperion/pull/39)
- Fix product rstrip() from NoneType error. [#41](https://github.com/greenbone/hyperion/pull/41)
- Adding missing field `port` to `override` entity. [#57](https://github.com/greenbone/hyperion/pull/57)