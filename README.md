<!-- omit in toc -->
# Prometheus Alert Model *for Python*

[![Current Package Version](https://badge.fury.io/py/prometheus-alert-model.svg)](https://pypi.python.org/pypi/prometheus-alert-model)
[![Maintenance](https://img.shields.io/badge/maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/prometheus-alert-model.svg)](https://pypi.python.org/pypi/prometheus-alert-model)
[![Downloads](https://pepy.tech/badge/prometheus-alert-model/month)](https://pepy.tech/project/prometheus-alert-model/month)
[![docs](https://img.shields.io/badge/docs-here-blue)](https://trallnag.github.io/prometheus-alert-model-for-python/)

![release](https://github.com/trallnag/prometheus-alert-model-for-python/workflows/release/badge.svg)
![commit](https://github.com/trallnag/prometheus-alert-model-for-python/workflows/commit/badge.svg)
[![codecov](https://codecov.io/gh/trallnag/prometheus-alert-model-for-python/branch/master/graph/badge.svg)](https://codecov.io/gh/trallnag/prometheus-alert-model-for-python)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This project provides the Pydantic models `AlertGroup` and `Alert` that
represent a payload from Prometheus Alertmanager. In addition, it also includes
a number of useful utility methods that perform actions on alert data.  It can
be used as a drop-in wherever you want to work with Prometheus Alertmanager
alert payload data.

A prominent example for using it is a FastAPI route that receives alert payloads.
Simply add `AlertGroup` as a parameter to the handler.

<!-- omit in toc -->
## Features

- Pydantic models that matches the official Alertmanager payload schema.
- Fields `specific_annotations` and `specific_labels` in every alert that
    contain elements that are specific to the respective alert.
- Methods to update common annotations and labels.
- Methods to remove, add, update, override and prefix annotations and labels.
- Every single method is well covered by tests.

<!-- omit in toc -->
## Table of Contents

- [Usage](#usage)
- [Motivation](#motivation)
- [Development](#development)

## Usage

Using the model is pretty straight-forward. Take a look at the automatically
generated docs or the source code itself. 

Here is a very short example how you could use the model. It removes all
annotations and labels starting with two underscores and adds a prefix that
contains namespace info to the summary label. Finally it prints specific
elements for all alerts in the group.

```python

from prometheus_alert_model import AlertGroup
from fastapi import FastAPI
from re import compile

app = FastAPI()

@app.post("/alert")
def post_alert(alert_group: AlertGroup):
    alert_group.remove_re(
        annotations=r"^(__.*)$",
        labels=compile(r"^(__.*)$")
    )

    alert_group.add_prefix(labels={"summary": "Prototyping system: "})
    
    for alert in alert_group.alerts:
        print(alert.specific_annotations
        print(alert.specific_labels)
```

<!-- omit in toc -->
### `Alert` Model

In the following all attributes you can find within a `Alert`. Notice
the custom attributes `specific_annotations` and `specific_labels` that
include elements that are specific to the respective alert in context of the
complete `AlertGroup` / payload.

```python
fingerprint: str
status: str
starts_at: datetime
ends_at: datetime
generator_url: str
annotations: Dict[str, str]
labels: Dict[str, str]
specific_annotations: Dict[str, str]
specific_labels: Dict[str, str]
```

<!-- omit in toc -->
### `AlertGroup` Model

In the following all attributes you can find within a `AlertGroup`. It
represents a single payload from Alertmanager.

```python
receiver: str
status: str
external_url: str
version: str
group_key: str
truncated_alerts: int = =0
group_labels: Dict[str, str]
common_annotations: Dict[str, str]
common_labels: Dict[str, str]
alerts: List[Alert]
```

Here is a short summary over the included utility methods (for full
documentation please refer to type hints or the automatically generated docs):

- `update_specific_elements`: Updates specific labels and annotations.
- `update_specific_annotations`: Updates specific annotations.
- `update_specific_labels`: Updates specific labels.
- `update_common_elements`: Updates common annotations and labels.
- `update_common_annotations`: Updates common annotations.
- `update_common_labels`: Updates common labels.
- `remove`: Removes annotations and labels by name.
- `remove_re`: Removes annotations and labels by matching names with regex.
- `add`: Adds annotations and labels but skips existing elements.
- `override`: Adds annotations and labels and overrides existing elements.
- `add_prefix`: Adds prefix to annotations and labels.

## Motivation

I have a bunch of Python scripts that work in some shape or form with Prometheus
Alertmanager data. Instead of duplicating the model across all of them I prefer
to have a single small package that is well tested and reuse it again and again.
This way I don't have to reimplement utility functions / methods.

## Development

Please refer to ["DEVELOPMENT.md"](DEVELOPMENT.md).
