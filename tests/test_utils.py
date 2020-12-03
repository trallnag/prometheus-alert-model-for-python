# Copyright © 2020 Tim Schwenke <tim.and.trallnag+code@gmail.com>
# Licensed under Apache License 2.0 <http://www.apache.org/licenses/LICENSE-2.0>

from prometheus_alert_model.utils import intersect


def test_intersect_none():
    assert intersect([]) == {}


def test_intersect_single():
    assert intersect([{1: 2}]) == {1: 2}


def test_intersect_multiple_v1():
    assert intersect(
        [
            {"a": "bbbbbbbbb", "b": "b", "c": "c"},
            {
                "a": "aaaaaaaaaa",
                "b": "b",
            },
        ]
    ) == {
        "b": "b",
    }


def test_intersect_multiple_v2():
    assert intersect(
        [
            {
                "a": "a",
                "b": "b",
                "c": "fefe",
                "dddddddddd": "ddwdwdwd dwdwdwdwd dwdwdw",
                1: 1,
            },
            {
                "a": "a",
                "b": "b",
                "c": 32,
                "dddddddddd": "ddwdwdwd dwdwdwdwd dwdwdw",
            },
        ]
    ) == {
        "a": "a",
        "b": "b",
        "dddddddddd": "ddwdwdwd dwdwdwdwd dwdwdw",
    }


def test_intersect_multiple_v3():
    assert (
        intersect(
            [
                {
                    "a": "a",
                    "b": "b",
                },
                {
                    "a": "a",
                    "b": "b",
                },
                {},
            ]
        )
        == {}
    )


def test_intersect_multiple_v4():
    assert (
        intersect(
            [
                {
                    "a": "a",
                    "b": "b",
                },
                {
                    "a": "a",
                    "b": "b",
                },
                {
                    "a": "a",
                },
                {
                    "a": "a",
                    "b": "c",
                },
            ]
        )
        == {"a": "a"}
    )
