# Copyright © 2020 Tim Schwenke <tim.and.trallnag+code@gmail.com>
# Licensed under Apache License 2.0 <http://www.apache.org/licenses/LICENSE-2.0>

from datetime import datetime, timezone

from prometheus_alert_model.main import Alert


def test_create_alert_by_alias(helpers):
    alert = Alert(
        fingerprint="x",
        status="x",
        startsAt="2020-11-03T17:51:36.14925565Z",
        endsAt="2020-11-03T17:51:36.14925565Z",
        generatorURL="https://www.google.com",
        labels={"a": "b"},
        annotations={"a": "b"},
    )
    helpers.wrapped_debug(alert)

    assert alert.fingerprint == "x"
    assert alert.status == "x"
    assert alert.starts_at == datetime(
        2020, 11, 3, 17, 51, 36, 149255, tzinfo=timezone.utc
    )
    assert alert.ends_at == datetime(2020, 11, 3, 17, 51, 36, 149255, tzinfo=timezone.utc)
    assert alert.generator_url == "https://www.google.com"
    assert alert.labels == {"a": "b"}
    assert alert.annotations == {"a": "b"}
    assert alert.specific_annotations == {}
    assert alert.specific_labels == {}


def test_create_alert_by_name(helpers):
    alert = Alert(
        fingerprint="x",
        status="x",
        starts_at="2020-11-03T17:51:36.14925565Z",
        ends_at="2020-11-03T17:51:36.14925565Z",
        generator_url="https://www.google.com",
        labels={"a": "b"},
        annotations={"a": "b"},
    )
    helpers.wrapped_debug(alert)

    assert alert.fingerprint == "x"
    assert alert.status == "x"
    assert alert.starts_at == datetime(
        2020, 11, 3, 17, 51, 36, 149255, tzinfo=timezone.utc
    )
    assert alert.ends_at == datetime(2020, 11, 3, 17, 51, 36, 149255, tzinfo=timezone.utc)
    assert alert.generator_url == "https://www.google.com"
    assert alert.labels == {"a": "b"}
    assert alert.annotations == {"a": "b"}


def test_create_alert_construct(helpers):
    alert = Alert.construct(
        fingerprint="x",
        status="x",
        starts_at=datetime(2020, 11, 3, 17, 51, 36, 149255, tzinfo=timezone.utc),
        ends_at=datetime(2020, 11, 3, 17, 51, 36, 149255, tzinfo=timezone.utc),
        generator_url="https://www.google.com",
        labels={"a": "b"},
        annotations={"a": "b"},
    )
    helpers.wrapped_debug(alert)

    assert alert.fingerprint == "x"
    assert alert.status == "x"
    assert alert.starts_at == datetime(
        2020, 11, 3, 17, 51, 36, 149255, tzinfo=timezone.utc
    )
    assert alert.ends_at == datetime(2020, 11, 3, 17, 51, 36, 149255, tzinfo=timezone.utc)
    assert alert.generator_url == "https://www.google.com"
    assert alert.labels == {"a": "b"}
    assert alert.annotations == {"a": "b"}


def test_create_alert_by_alias_with_additional_attr(helpers):
    alert = Alert(
        fingerprint="x",
        status="x",
        startsAt="2020-11-03T17:51:36.14925565Z",
        endsAt="2020-11-03T17:51:36.14925565Z",
        generatorURL="https://www.google.com",
        labels={"a": "b"},
        annotations={"a": "b"},
        foo="bar",
    )
    helpers.wrapped_debug(alert)

    assert alert.foo == "bar"

    alert.lul = "mump"

    assert alert.lul == "mump"
