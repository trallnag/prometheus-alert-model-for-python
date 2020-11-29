# Copyright © 2020 Tim Schwenke <tim.and.trallnag+code@gmail.com>
# Licensed under Apache License 2.0 <http://www.apache.org/licenses/LICENSE-2.0>

import json

from prometheus_alert_model.main import AlertGroup


def test_remove_nothing(helpers, data_path):
    with data_path.joinpath("payload-simple-01.json").open() as file:
        payload = json.load(file)

    alert_group = AlertGroup(**payload)
    helpers.wrapped_debug(alert_group)

    alert_group.remove()

    assert alert_group.dict() == AlertGroup(**payload)


def test_remove_labels(helpers, data_path):
    with data_path.joinpath("payload-simple-01.json").open() as file:
        payload = json.load(file)

    alert_group = AlertGroup(**payload)
    helpers.wrapped_debug(alert_group, description="Alert group before remove")

    # Labels before

    assert alert_group.alerts[0].labels == {
        "alertname": "WhatEver",
        "foo_bar_qux": "foo_moo_zoom",
        "mu": "sik",
        "severity": "warning",
    }
    assert alert_group.alerts[0].specific_labels == {
        "mu": "sik",
    }

    assert alert_group.alerts[1].labels == {
        "alertname": "WhatEver",
        "foo_bar_qux": "foo_moo_zoom",
        "severity": "warning",
    }
    assert alert_group.alerts[1].specific_labels == {}

    alert_group.remove(labels=["mu", "foo_bar_qux", "alertname"])
    helpers.wrapped_debug(alert_group, description="Alert group after remove")

    # Labels after

    assert alert_group.alerts[0].labels == {"severity": "warning"}
    assert alert_group.alerts[0].specific_labels == {}

    assert alert_group.alerts[1].labels == {
        "severity": "warning",
    }
    assert alert_group.alerts[1].specific_labels == {}

    # Annotations stayed the same

    assert alert_group.alerts[0].annotations == {
        "description": "A Prometheus job has disappe",
        "summary": "Prometheus job missing (instance )",
    }
    assert alert_group.alerts[0].specific_annotations == {}

    assert alert_group.alerts[1].annotations == {
        "description": "A Prometheus job has disappe",
        "summary": "Prometheus job missing (instance )",
        "this": "isspecific",
    }
    assert alert_group.alerts[1].specific_annotations == {
        "this": "isspecific",
    }


def test_remove_annotations(helpers, data_path):
    with data_path.joinpath("payload-simple-01.json").open() as file:
        payload = json.load(file)

    alert_group = AlertGroup(**payload)
    helpers.wrapped_debug(alert_group, description="Alert group before remove")

    # Annotations before

    assert alert_group.alerts[0].annotations == {
        "description": "A Prometheus job has disappe",
        "summary": "Prometheus job missing (instance )",
    }
    assert alert_group.alerts[0].specific_annotations == {}

    assert alert_group.alerts[1].annotations == {
        "description": "A Prometheus job has disappe",
        "summary": "Prometheus job missing (instance )",
        "this": "isspecific",
    }
    assert alert_group.alerts[1].specific_annotations == {
        "this": "isspecific",
    }

    alert_group.remove(annotations=["this", "whatever"])
    helpers.wrapped_debug(alert_group, description="Alert group after remove")

    # Annotations after

    assert alert_group.alerts[0].annotations == {
        "description": "A Prometheus job has disappe",
        "summary": "Prometheus job missing (instance )",
    }
    assert alert_group.alerts[0].specific_annotations == {}

    assert alert_group.alerts[1].annotations == {
        "description": "A Prometheus job has disappe",
        "summary": "Prometheus job missing (instance )",
    }
    assert alert_group.alerts[1].specific_annotations == {}

    # Labels stayed the same

    assert alert_group.alerts[0].labels == {
        "alertname": "WhatEver",
        "foo_bar_qux": "foo_moo_zoom",
        "mu": "sik",
        "severity": "warning",
    }
    assert alert_group.alerts[0].specific_labels == {
        "mu": "sik",
    }

    assert alert_group.alerts[1].labels == {
        "alertname": "WhatEver",
        "foo_bar_qux": "foo_moo_zoom",
        "severity": "warning",
    }
    assert alert_group.alerts[1].specific_labels == {}


def test_remove_annotation(helpers, data_path):
    with data_path.joinpath("payload-simple-01.json").open() as file:
        payload = json.load(file)

    alert_group = AlertGroup(**payload)
    helpers.wrapped_debug(alert_group, description="Alert group before remove")

    assert "this" in alert_group.alerts[1].annotations

    alert_group.remove(annotations="this")

    assert "this" not in alert_group.alerts[1].annotations


def test_remove_label(helpers, data_path):
    with data_path.joinpath("payload-simple-01.json").open() as file:
        payload = json.load(file)

    alert_group = AlertGroup(**payload)
    helpers.wrapped_debug(alert_group, description="Alert group before remove")

    assert "mu" in alert_group.alerts[0].labels

    alert_group.remove(labels="this")

    assert "this" not in alert_group.alerts[0].labels
