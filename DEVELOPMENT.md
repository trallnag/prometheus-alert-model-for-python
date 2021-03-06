<!-- omit in toc -->
# Development <!-- omit in toc  -->

This document contains information regarding the development of PromAM.

<!-- omit in toc -->
## Table of Contents

- [CI/CD](#cicd)
  - [Code Coverage](#code-coverage)
  - [Secrets](#secrets)
- [Documentation](#documentation)
  - [Autogenerated Docs](#autogenerated-docs)
  - [Manual Docs](#manual-docs)
- [Questions & Answers](#questions--answers)
  - [How to release a new version?](#how-to-release-a-new-version)
  - [How to change supported Python version(s)?](#how-to-change-supported-python-versions)

## CI/CD

- GitHub Actions is used.
- Workflows are self-documenting.

### Code Coverage

For code coverage, [CodeCov](https://codecov.io/) is used. It is updated
automatically as part of GitHub Actions. Notice that a coverage report must
exist for the update to work.

### Secrets

Secrets are stored as GitHub secrets in repository scope.

- `PYPI_TOKEN`: Access to project PyPI registry.
    Used in [`release.yml`](/.github/workflows/release.yml).
- `TEST_PYPI_TOKEN`: Access to project on PyPI test registry.
    Used in [`test-release.yml`](/.github/workflows/test-release.yml).

## Documentation

Documentation is split into two parts. The autogenerated documentation and
documentation created manually in specific Markdown files.

### Autogenerated Docs

- Pdoc3 is used for automatically generating an API documentation from Docstrings.
- Generated data can be found in `docs`.
- Code to build docs can be found in `run.sh docs`.
- Automatically triggered on every commit to master branch.
- Elements starting with an underscore are excluded.
- GitHub Pages is used to host automatically generated docs.
  - Must be activated manually in GitHub repo settings.
  - `/docs` directory must be used.
  - Only latest commit on `master` branch is respected.

### Manual Docs

Everything contained within `README.md`.

## Questions & Answers

### How to release a new version?

1. Ensure that the `commit` workflow for the latest commit on `master` has
    been successful.
2. Pick a new version number that follows the convention.
3. Ensure that the [changelog](/CHANGELOG.md) is up-to-date and follows the
    convention. The respective section will be extracted automatically.
4. Ensure that the version is up-to-date in [`pyproject.toml`](pyproject.toml).
5. Run `release` workflow manually from GitHub UI.

### How to change supported Python version(s)?

1. Ensure that all tests are running successfully with (new) supported versions
    on your local machine.
2. Update the Python dependency in [`pyproject.toml`](/pyproject.toml).
3. Go through all workflow files and ensure that the correct versions are used.
