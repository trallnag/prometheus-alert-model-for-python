<!-- omit in toc -->
# Prometheus Alert Model *for Python*

[![PyPI](https://img.shields.io/pypi/pyversions/prometheus-alert-model.svg)](https://pypi.python.org/pypi/prometheus-alert-model-for-python)

This project provides the Pydantic models `AlertGroup` and `Alert` in addition
to a number of useful utility methods that perform actions on alert data. It can
be used as a drop-in wherever you want to work with Prometheus Alertmanager
alert payload data.

A prominent example for using it is a FastAPI route that receives alert payloads.
Simple add `AlertGroup` as a parameter to the handler. Utilities include
actions like adding and removing labels and annotations or updating them by
adding prefixes and suffixes. 

<!-- omit in toc -->
## Table of Contents

- [Motivation](#motivation)
- [Development](#development)

## Motivation

I have a bunch of Python scripts that work in some shape or form with Prometheus
Alertmanager data. Instead of duplicating the model across all of them I prefer
to have a single small package and reuse it again and again.

## Development

Please refer to ["DEVELOPMENT.md"](DEVELOPMENT.md).
