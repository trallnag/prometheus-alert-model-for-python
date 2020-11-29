# Copyright © 2020 Tim Schwenke <tim.and.trallnag+code@gmail.com>
# Licensed under Apache License 2.0 <http://www.apache.org/licenses/LICENSE-2.0>

import json

from prometheus_alert_model.main import AlertGroup


def test_create_alert_group(helpers, data_path):
    with data_path.joinpath("payload-simple-01.json").open() as file:
        payload = json.load(file)

    alert_group = AlertGroup(**payload)
    helpers.wrapped_debug(alert_group)

    assert alert_group.receiver == "generic"
    assert alert_group.status == "firing"
    assert alert_group.group_labels == {"alertname": "WhatEver"}
    assert len(alert_group.common_labels) == 3
    assert len(alert_group.common_annotations) == 2
    assert alert_group.external_url == "http://1217896f2a1d:9093"
    assert alert_group.version == "4"
    assert alert_group.group_key == '{}:{alertname="WhatEver"}'
    assert alert_group.truncated_alerts == 0


def test_create_alert_group_alerts(helpers, data_path):
    with data_path.joinpath("payload-simple-01.json").open() as file:
        payload = json.load(file)

    alert_group = AlertGroup(**payload)
    helpers.wrapped_debug(alert_group)

    assert len(alert_group.alerts[0].labels) == 4
    assert len(alert_group.alerts[0].annotations) == 2
    assert len(alert_group.alerts[1].labels) == 3
    assert len(alert_group.alerts[1].annotations) == 3

    assert len(alert_group.alerts[0].specific_labels) == 1
    assert len(alert_group.alerts[0].specific_annotations) == 0
    assert len(alert_group.alerts[1].specific_labels) == 0
    assert len(alert_group.alerts[1].specific_annotations) == 1
