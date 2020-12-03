# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
as well as the [Conventional Commits](https://www.conventionalcommits.org) 
specification.

## [Unreleased]

### Added

- Automatic creation of specific labels and annotations by using Pydantic
    validator during creation of `AlertGroup`.
- Method `update_specific` that updates specific labels and annotations in case
    something is changed in the alert.
- Action `remve` allows you to remove labels and annotations by name.
- Action `remove_re` allows you to remove labels and annotations that match
    regex expressions. Different types of parameters are supported.
- Action `add` allows you to add missing labels and annoations. If a label or
    annotation already exists it will not be overriden.
- Action `override` allows you to add and override labels and annotations.
    This makes it different from `add`.
- Action `add_prefix` allows to add prefixes to annotations and labels.
- Util that intersects list of dicts by key value.
- Methods `update_common` that update common annotations and common labels.
