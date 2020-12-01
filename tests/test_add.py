# Copyright © 2020 Tim Schwenke <tim.and.trallnag+code@gmail.com>
# Licensed under Apache License 2.0 <http://www.apache.org/licenses/LICENSE-2.0>

import json

from prometheus_alert_model.main import AlertGroup


def test_add_single_annotation_non_specific(helpers, data_path):
    with data_path.joinpath("payload-simple-01.json").open() as file:
        payload = json.load(file)

    alert_group = AlertGroup(**payload)
    helpers.wrapped_debug(alert_group)

    assert alert_group.alerts[0].annotations == {
        "description": "A Prometheus job has disappe",
        "summary": "Prometheus job missing (instance )",
    }
    assert alert_group.alerts[0].specific_annotations == {}

    alert_group.add(annotations={"hello": "world"})

    assert alert_group.alerts[0].annotations == {
        "description": "A Prometheus job has disappe",
        "summary": "Prometheus job missing (instance )",
        "hello": "world",
    }
    assert alert_group.alerts[0].specific_annotations == {}

    assert alert_group.alerts[1].annotations == {
        "description": "A Prometheus job has disappe",
        "summary": "Prometheus job missing (instance )",
        "this": "isspecific",
        "hello": "world",
    }


def test_add_single_annotation_specific(helpers, data_path):
    with data_path.joinpath("payload-simple-01.json").open() as file:
        payload = json.load(file)

    alert_group = AlertGroup(**payload)
    helpers.wrapped_debug(alert_group, "original")

    alert_group.alerts[1].annotations["hallo"] = "bump"
    alert_group.update_specific(targets="annotations")
    helpers.wrapped_debug(alert_group, "after adding hallo bump to alert1")

    assert alert_group.alerts[0].annotations == {
        "description": "A Prometheus job has disappe",
        "summary": "Prometheus job missing (instance )",
    }
    assert alert_group.alerts[0].specific_annotations == {}

    assert alert_group.alerts[1].annotations == {
        "description": "A Prometheus job has disappe",
        "summary": "Prometheus job missing (instance )",
        "this": "isspecific",
        "hallo": "bump",
    }
    assert alert_group.alerts[1].specific_annotations == {
        "hallo": "bump",
        "this": "isspecific",
    }

    alert_group.add(annotations={"hallo": "world"})
    helpers.wrapped_debug(alert_group, "after using add method")

    assert alert_group.alerts[0].annotations == {
        "description": "A Prometheus job has disappe",
        "summary": "Prometheus job missing (instance )",
        "hallo": "world",
    }
    assert alert_group.alerts[0].specific_annotations == {"hallo": "world"}

    assert alert_group.alerts[1].annotations == {
        "description": "A Prometheus job has disappe",
        "summary": "Prometheus job missing (instance )",
        "this": "isspecific",
        "hallo": "bump",
    }
    assert alert_group.alerts[1].specific_annotations == {
        "hallo": "bump",
        "this": "isspecific",
    }


def test_add_single_label(helpers, data_path):
    with data_path.joinpath("payload-simple-01.json").open() as file:
        payload = json.load(file)

    alert_group = AlertGroup(**payload)
    helpers.wrapped_debug(alert_group)

    assert alert_group.alerts[0].labels == {
        "alertname": "WhatEver",
        "foo_bar_qux": "foo_moo_zoom",
        "mu": "sik",
        "severity": "warning",
    }
    assert alert_group.alerts[0].specific_labels == {"mu": "sik"}

    alert_group.add(labels={"hello": "world"})

    assert alert_group.alerts[0].labels == {
        "alertname": "WhatEver",
        "foo_bar_qux": "foo_moo_zoom",
        "mu": "sik",
        "severity": "warning",
        "hello": "world",
    }
    assert alert_group.alerts[0].specific_labels == {"mu": "sik"}

    assert alert_group.alerts[1].labels == {
        "alertname": "WhatEver",
        "foo_bar_qux": "foo_moo_zoom",
        "severity": "warning",
        "hello": "world",
    }


def test_add_multiple_anotations_and_labels(helpers, data_path):
    with data_path.joinpath("payload-simple-01.json").open() as file:
        payload = json.load(file)

    alert_group = AlertGroup(**payload)
    helpers.wrapped_debug(alert_group)

    alert_group.add(labels={"hello": "world"}, annotations={"hello": "world"})

    assert alert_group.common_annotations["hello"] == "world"
    assert alert_group.common_labels["hello"] == "world"

    assert alert_group.alerts[0].annotations["hello"] == "world"
    assert alert_group.alerts[1].annotations["hello"] == "world"
    assert alert_group.alerts[0].labels["hello"] == "world"
    assert alert_group.alerts[1].labels["hello"] == "world"

    assert not alert_group.alerts[0].specific_annotations.get("hello", None)
    assert not alert_group.alerts[1].specific_labels.get("hello", None)
    assert not alert_group.alerts[0].specific_annotations.get("hello", None)
    assert not alert_group.alerts[1].specific_labels.get("hello", None)


def test_add_none_none(helpers, data_path):
    with data_path.joinpath("payload-simple-01.json").open() as file:
        payload = json.load(file)

    alert_group = AlertGroup(**payload)

    alert_group.add()

    assert alert_group.dict() == AlertGroup(**payload)
