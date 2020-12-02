# Copyright © 2020 Tim Schwenke <tim.and.trallnag+code@gmail.com>
# Licensed under Apache License 2.0 <http://www.apache.org/licenses/LICENSE-2.0>

import json

from prometheus_alert_model.main import AlertGroup


def test_add_prefix_annotations(helpers, data_path):
    with data_path.joinpath("payload-simple-01.json").open() as file:
        payload = json.load(file)

    alert_group = AlertGroup(**payload)
    helpers.wrapped_debug(alert_group)

    assert alert_group.common_annotations["description"] == "A Prometheus job has disappe"
    assert (
        alert_group.alerts[0].annotations["description"] == "A Prometheus job has disappe"
    )
    assert (
        alert_group.alerts[1].annotations["description"] == "A Prometheus job has disappe"
    )

    alert_group.add_prefix(annotations={"description": "PREFIX: "})
    helpers.wrapped_debug(alert_group)

    assert (
        alert_group.common_annotations["description"]
        == "PREFIX: A Prometheus job has disappe"
    )
    assert (
        alert_group.alerts[0].annotations["description"]
        == "PREFIX: A Prometheus job has disappe"
    )
    assert (
        alert_group.alerts[1].annotations["description"]
        == "PREFIX: A Prometheus job has disappe"
    )


def test_add_prefix_labels(helpers, data_path):
    with data_path.joinpath("payload-simple-01.json").open() as file:
        payload = json.load(file)

    alert_group = AlertGroup(**payload)
    helpers.wrapped_debug(alert_group)

    assert alert_group.common_labels["alertname"] == "WhatEver"
    assert alert_group.alerts[0].labels["alertname"] == "WhatEver"
    assert alert_group.alerts[1].labels["alertname"] == "WhatEver"

    alert_group.add_prefix(labels={"alertname": "PREFIX: "})
    helpers.wrapped_debug(alert_group)

    assert alert_group.common_labels["alertname"] == "PREFIX: WhatEver"
    assert alert_group.alerts[0].labels["alertname"] == "PREFIX: WhatEver"
    assert alert_group.alerts[1].labels["alertname"] == "PREFIX: WhatEver"
