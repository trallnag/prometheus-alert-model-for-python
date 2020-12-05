# Copyright © 2020 Tim Schwenke <tim.and.trallnag+code@gmail.com>
# Licensed under Apache License 2.0 <http://www.apache.org/licenses/LICENSE-2.0>

import json

from prometheus_alert_model.main import AlertGroup

# ==============================================================================


def test_update_common_annotations_v1(helpers, data_path):
    with data_path.joinpath("payload-simple-01.json").open() as file:
        payload = json.load(file)

    alert_group = AlertGroup(**payload)
    helpers.wrapped_debug(alert_group)

    assert alert_group.common_annotations == {
        "description": "A Prometheus job has disappe",
        "summary": "Prometheus job missing (instance )",
    }

    for alert in alert_group.alerts:
        alert.annotations["a"] = "a"

    alert_group.update_common_annotations()
    helpers.wrapped_debug(alert_group)

    assert alert_group.common_annotations == {
        "description": "A Prometheus job has disappe",
        "summary": "Prometheus job missing (instance )",
        "a": "a",
    }


def test_update_common_annotations_v2(helpers, data_path):
    with data_path.joinpath("payload-simple-01.json").open() as file:
        payload = json.load(file)

    alert_group = AlertGroup(**payload)
    helpers.wrapped_debug(alert_group)

    assert alert_group.common_annotations == {
        "description": "A Prometheus job has disappe",
        "summary": "Prometheus job missing (instance )",
    }

    alert_group.alerts[0].annotations["a"] = "a"
    alert_group.alerts[1].annotations["a"] = "aa"

    alert_group.update_common_annotations()
    helpers.wrapped_debug(alert_group)

    assert alert_group.common_annotations == {
        "description": "A Prometheus job has disappe",
        "summary": "Prometheus job missing (instance )",
    }


# ==============================================================================


def test_update_common_labels_v1(helpers, data_path):
    with data_path.joinpath("payload-simple-01.json").open() as file:
        payload = json.load(file)

    alert_group = AlertGroup(**payload)
    helpers.wrapped_debug(alert_group)

    assert alert_group.common_labels == {
        "alertname": "WhatEver",
        "foo_bar_qux": "foo_moo_zoom",
        "severity": "warning",
    }

    for alert in alert_group.alerts:
        alert.labels["a"] = "a"

    alert_group.update_common_labels()
    helpers.wrapped_debug(alert_group)

    assert alert_group.common_labels == {
        "alertname": "WhatEver",
        "foo_bar_qux": "foo_moo_zoom",
        "severity": "warning",
        "a": "a",
    }


def test_update_common_labels_v2(helpers, data_path):
    with data_path.joinpath("payload-simple-01.json").open() as file:
        payload = json.load(file)

    alert_group = AlertGroup(**payload)
    helpers.wrapped_debug(alert_group)

    assert alert_group.common_labels == {
        "alertname": "WhatEver",
        "foo_bar_qux": "foo_moo_zoom",
        "severity": "warning",
    }

    alert_group.alerts[0].labels["a"] = "a"
    alert_group.alerts[1].labels["a"] = "aa"

    alert_group.update_common_labels()
    helpers.wrapped_debug(alert_group)

    assert alert_group.common_labels == {
        "alertname": "WhatEver",
        "foo_bar_qux": "foo_moo_zoom",
        "severity": "warning",
    }
