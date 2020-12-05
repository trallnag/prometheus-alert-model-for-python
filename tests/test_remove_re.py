# Copyright © 2020 Tim Schwenke <tim.and.trallnag+code@gmail.com>
# Licensed under Apache License 2.0 <http://www.apache.org/licenses/LICENSE-2.0>

import json
import re

from prometheus_alert_model.main import AlertGroup


def test_remove_re_single_label_as_str(helpers, data_path):
    with data_path.joinpath("payload-simple-01.json").open() as file:
        payload = json.load(file)

    alert_group = AlertGroup(**payload)
    helpers.wrapped_debug(alert_group, description="Alert group BEFORE remove_re")

    assert "mu" in alert_group.alerts[0].labels
    assert "mu" in alert_group.alerts[0].specific_labels
    assert "foo_bar_qux" in alert_group.alerts[0].labels
    assert "foo_bar_qux" in alert_group.alerts[1].labels

    alert_group.remove_re(labels=r"^(foo|mu).*$")
    helpers.wrapped_debug(alert_group, description="Alert group AFTER remove_re")

    assert "mu" not in alert_group.alerts[0].labels
    assert "mu" not in alert_group.alerts[0].specific_labels
    assert "foo_bar_qux" not in alert_group.alerts[0].labels
    assert "foo_bar_qux" not in alert_group.alerts[1].labels


def test_remove_re_single_label_as_pattern(helpers, data_path):
    with data_path.joinpath("payload-simple-01.json").open() as file:
        payload = json.load(file)

    alert_group = AlertGroup(**payload)
    helpers.wrapped_debug(alert_group, description="Alert group BEFORE remove_re")

    assert "mu" in alert_group.alerts[0].labels
    assert "mu" in alert_group.alerts[0].specific_labels
    assert "foo_bar_qux" in alert_group.alerts[0].labels
    assert "foo_bar_qux" in alert_group.alerts[1].labels

    alert_group.remove_re(labels=re.compile(r"^(foo|mu).*$"))
    helpers.wrapped_debug(alert_group, description="Alert group AFTER remove_re")

    assert "mu" not in alert_group.alerts[0].labels
    assert "mu" not in alert_group.alerts[0].specific_labels
    assert "foo_bar_qux" not in alert_group.alerts[0].labels
    assert "foo_bar_qux" not in alert_group.alerts[1].labels


def test_remove_re_multiple_annotations(helpers, data_path):
    with data_path.joinpath("payload-simple-01.json").open() as file:
        payload = json.load(file)

    alert_group = AlertGroup(**payload)

    alert_group.remove_re(annotations=[r"^(description|summary)$", r"^(this|that)$"])

    assert alert_group.common_annotations == {}

    for alert in alert_group.alerts:
        assert alert.annotations == {}
        assert alert.specific_annotations == {}
