# Copyright © 2020 Tim Schwenke <tim.and.trallnag+code@gmail.com>
# Licensed under Apache License 2.0 <http://www.apache.org/licenses/LICENSE-2.0>

import json

import pytest

from prometheus_alert_model.main import AlertGroup


def test_update_specific_elements_annotations(helpers, data_path):
    with data_path.joinpath("payload-simple-01.json").open() as file:
        payload = json.load(file)

    alert_group = AlertGroup(**payload)
    helpers.wrapped_debug(alert_group)

    assert alert_group.alerts[0].specific_annotations == {}
    assert alert_group.alerts[1].specific_annotations == {"this": "isspecific"}

    alert_group.alerts[0].annotations["hallo"] = "world"
    alert_group.update_specific_elements("annotations")

    assert alert_group.alerts[0].specific_annotations == {"hallo": "world"}
    assert alert_group.alerts[1].specific_annotations == {"this": "isspecific"}


def test_update_specific_elements_annotations_invalid(helpers, data_path):
    with data_path.joinpath("payload-simple-01.json").open() as file:
        payload = json.load(file)

    alert_group = AlertGroup(**payload)
    helpers.wrapped_debug(alert_group)

    assert alert_group.alerts[0].specific_annotations == {}
    assert alert_group.alerts[1].specific_annotations == {"this": "isspecific"}

    alert_group.alerts[0].annotations["hallo"] = "world"

    with pytest.raises(KeyError):
        alert_group.update_specific_elements("anotations")


def test_update_specific_elements_labels(helpers, data_path):
    with data_path.joinpath("payload-simple-01.json").open() as file:
        payload = json.load(file)

    alert_group = AlertGroup(**payload)
    helpers.wrapped_debug(alert_group)

    assert alert_group.alerts[0].specific_labels == {"mu": "sik"}
    assert alert_group.alerts[1].specific_labels == {}

    alert_group.alerts[1].labels["hallo"] = "world"
    alert_group.update_specific_elements("labels")

    assert alert_group.alerts[0].specific_labels == {"mu": "sik"}
    assert alert_group.alerts[1].specific_labels == {"hallo": "world"}


def test_update_specific_elements_all_defaults(helpers, data_path):
    with data_path.joinpath("payload-simple-01.json").open() as file:
        payload = json.load(file)

    alert_group = AlertGroup(**payload)
    helpers.wrapped_debug(alert_group)

    assert alert_group.alerts[0].specific_annotations == {}
    assert alert_group.alerts[1].specific_annotations == {"this": "isspecific"}

    assert alert_group.alerts[0].specific_labels == {"mu": "sik"}
    assert alert_group.alerts[1].specific_labels == {}

    alert_group.alerts[1].labels["hallo"] = "world"
    alert_group.alerts[0].annotations["hallo"] = "world"
    alert_group.update_specific_elements()

    assert alert_group.alerts[0].specific_annotations == {"hallo": "world"}
    assert alert_group.alerts[1].specific_annotations == {"this": "isspecific"}

    assert alert_group.alerts[0].specific_labels == {"mu": "sik"}
    assert alert_group.alerts[1].specific_labels == {"hallo": "world"}


def test_update_specific_annotations(helpers, data_path):
    with data_path.joinpath("payload-simple-01.json").open() as file:
        payload = json.load(file)

    alert_group = AlertGroup(**payload)
    helpers.wrapped_debug(alert_group)

    alert_group.alerts[0].annotations["hallo"] = "world"

    alert_group.update_specific_annotations()

    assert alert_group.alerts[0].specific_annotations == {"hallo": "world"}


def test_update_specific_labels(helpers, data_path):
    with data_path.joinpath("payload-simple-01.json").open() as file:
        payload = json.load(file)

    alert_group = AlertGroup(**payload)
    helpers.wrapped_debug(alert_group)

    assert alert_group.alerts[0].specific_labels == {"mu": "sik"}

    alert_group.alerts[0].labels["mu"] = "sik"

    alert_group.update_specific_labels()

    assert alert_group.alerts[0].specific_labels == {"mu": "sik"}
