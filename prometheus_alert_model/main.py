# Copyright © 2020 Tim Schwenke <tim.and.trallnag+code@gmail.com>
# Licensed under Apache License 2.0 <http://www.apache.org/licenses/LICENSE-2.0>

from datetime import datetime
from re import Pattern, compile
from typing import Dict, List, Optional, Sequence, Union

from pydantic import BaseModel, Field, validator
from typing_extensions import Literal

from .utils import intersect


class Alert(BaseModel):
    fingerprint: str
    status: str
    starts_at: datetime = Field(alias="startsAt")
    ends_at: datetime = Field(alias="endsAt")
    generator_url: str = Field(alias="generatorURL")
    annotations: Dict[str, str]
    labels: Dict[str, str]

    specific_annotations: Dict[str, str] = Field(
        default={},
        description=(
            "Annotations that are specific to this alert in the context of the "
            "whole alert group. Does not have to be provided in the payload "
            "and is automatically calculated."
        ),
    )
    specific_labels: Dict[str, str] = Field(
        default={},
        description=(
            "Labels that are specific to this alert in the context of the "
            "whole alert group. Does not have to be provided in the payload "
            "and is automatically calculated."
        ),
    )

    class Config:
        extra = "allow"
        allow_population_by_field_name = True


class AlertGroup(BaseModel):
    receiver: str
    status: str
    external_url: str = Field(alias="externalURL")
    version: str
    group_key: str = Field(alias="groupKey")
    truncated_alerts: int = Field(alias="truncatedAlerts", default=0)
    group_labels: Dict[str, str] = Field(alias="groupLabels")
    common_annotations: Dict[str, str] = Field(alias="commonAnnotations")
    common_labels: Dict[str, str] = Field(alias="commonLabels")
    alerts: List[Alert]

    @validator("alerts")
    def check_specific(cls, v, values):
        """Updates specific labels and annotations."""

        for alert in v:
            alert.specific_annotations = {
                name: alert.annotations[name]
                for name in set(alert.annotations) - set(values.get("common_annotations"))
            }

            alert.specific_labels = {
                name: alert.labels[name]
                for name in set(alert.labels) - set(values.get("common_labels"))
            }

        return v

    class Config:
        extra = "allow"
        allow_population_by_field_name = True

    # --------------------------------------------------------------------------

    def update_specific_elements(
        self,
        targets: Union[
            Sequence[Literal["annotations", "labels"]], Literal["annotations", "labels"]
        ] = ["annotations", "labels"],
    ) -> None:
        """Updates specific labels and annotations."""

        targets = (targets,) if isinstance(targets, str) else targets

        for target in targets:
            for alert in self.alerts:
                alert.__dict__[f"specific_{target}"] = {
                    name: alert.__dict__[target][name]
                    for name in set(alert.__dict__[target])
                    - set(self.__dict__[f"common_{target}"])
                }

    def update_specific_annotations(self) -> None:
        """Updates specific annotations."""

        for alert in self.alerts:
            alert.specific_annotations = {
                name: alert.annotations[name]
                for name in set(alert.annotations) - set(self.common_annotations)
            }

    def update_specific_labels(self) -> None:
        """Updates specific labels."""

        for alert in self.alerts:
            alert.specific_labels = {
                name: alert.labels[name]
                for name in set(alert.labels) - set(self.common_labels)
            }

    # --------------------------------------------------------------------------

    def update_common_elements(
        self,
        targets: Union[
            Sequence[Literal["annotations", "labels"]], Literal["annotations", "labels"]
        ] = ["annotations", "labels"],
    ) -> None:
        """Updates common annotations and labels.

        Args:
            targets (Union[Sequence[Literal["annotations", "labels"]], Literal["annotations", "labels"], optional):
                Targets that should be updated. Defaults to ["annotations", "labels"].
        """

        for target in targets:
            self.__dict__[f"common_{target}"] = intersect(
                [alert.__dict__[target] for alert in self.alerts]
            )

    def update_common_annotations(self) -> None:
        """Updates common annotations."""

        self.common_annotations = intersect([alert.annotations for alert in self.alerts])

    def update_common_labels(self) -> None:
        """Updates common labels."""

        self.common_labels = intersect([alert.labels for alert in self.alerts])

    # --------------------------------------------------------------------------

    def remove(
        self,
        annotations: Optional[Union[List[str], str]] = None,
        labels: Optional[Union[List[str], str]] = None,
    ) -> None:
        """Removes annotations and labels by name.

        Args:
            annotations (Union[List[str], str], optional): Names of
                annotations to remove. Defaults to `None`.
            labels (Union[List[str], str], optional): Names of labels to
                remove. Defaults to `None`.
        """

        targets: Dict[str, Union[List[str], str]] = {}

        if annotations:
            targets["annotations"] = annotations

        if labels:
            targets["labels"] = labels

        for target, values in targets.items():
            names_to_pop: List[str] = [values] if isinstance(values, str) else values

            for name_to_pop in names_to_pop:
                self.__dict__[f"common_{target}"].pop(name_to_pop, None)
                for alert in self.alerts:
                    alert.__dict__[target].pop(name_to_pop, None)
                    alert.__dict__[f"specific_{target}"].pop(name_to_pop, None)

    # --------------------------------------------------------------------------

    def remove_re(
        self,
        annotations: Optional[Union[List[Union[Pattern, str]], Pattern, str]] = None,
        labels: Optional[Union[List[Union[Pattern, str]], Pattern, str]] = None,
    ) -> None:
        """Removes annotations and labels by matching names with regex.

        Args:
            annotations (Union[List[Union[Pattern, str]], Pattern, str], optional):
                Patterns that should be matched unanchored against annotations.
                If a `str` is given instead of a `Pattern`, the `str` will be
                compiled to `Pattern`. Defaults to `None`.
            labels (Union[List[Union[Pattern, str]], Pattern, str], optional):
                Patterns that should be matched unanchored against labels.
                If a `str` is given instead of a `Pattern`, the `str` will be
                compiled to `Pattern`. Defaults to `None`.
        """

        targets: Dict[
            Literal["annotations", "labels"],
            Union[List[Union[Pattern, str]], Pattern, str],
        ] = {}

        if annotations:
            targets["annotations"] = annotations

        if labels:
            targets["labels"] = labels

        if targets:
            for target, target_value in targets.items():

                patterns: List[Pattern]
                if isinstance(target_value, str):
                    patterns = [compile(target_value)]
                elif isinstance(target_value, Pattern):
                    patterns = [target_value]
                else:
                    patterns = [
                        compile(pattern) if isinstance(pattern, str) else pattern
                        for pattern in target_value
                    ]

                for pattern in patterns:
                    elements = self.__dict__[f"common_{target}"]

                    for name_to_pop in {e for e in elements if pattern.search(e)}:
                        elements.pop(name_to_pop, None)

                    for alert in self.alerts:
                        elements = alert.__dict__[target]
                        for name_to_pop in {e for e in elements if pattern.search(e)}:
                            elements.pop(name_to_pop, None)

            self.update_specific_elements(list(targets.keys()))

    # --------------------------------------------------------------------------

    def add(
        self,
        annotations: Optional[Dict[str, str]] = None,
        labels: Optional[Dict[str, str]] = None,
    ) -> None:
        """Adds annotations and labels but skips existing elements.

        Args:
            annotations (Optional[Dict[str, str]], optional): `Dict` of
                annotations to add. Defaults to `None`.
            labels (Optional[Dict[str, str]], optional): `Dict` of labels to add.
                Defaults to `None`.
        """

        targets: Dict[Literal["annotations", "labels"], Dict[str, str]] = {}

        if annotations:
            targets["annotations"] = annotations

        if labels:
            targets["labels"] = labels

        if targets:
            for target, items_to_add in targets.items():
                for name, value in items_to_add.items():
                    unique_values = set()

                    for alert in self.alerts:
                        elements = alert.__dict__[target]

                        if name not in elements:
                            elements[name] = value
                            unique_values.add(value)
                        else:
                            unique_values.add(elements[name])

                    if len(unique_values) == 1 and value in unique_values:
                        self.__dict__[f"common_{target}"][name] = value

            self.update_specific_elements(list(targets.keys()))

    # --------------------------------------------------------------------------

    def override(
        self,
        annotations: Optional[Dict[str, str]] = None,
        labels: Optional[Dict[str, str]] = None,
    ) -> None:
        """Adds annotations and labels and overrides existing elements.

        Args:
            annotations (Optional[Dict[str, str]], optional): `Dict` of
                annotations to override with. Defaults to `None`.
            labels (Optional[Dict[str, str]], optional): `Dict` of labels to
                override with. Defaults to `None`.
        """

        targets: Dict[Literal["annotations", "labels"], Dict[str, str]] = {}

        if annotations:
            targets["annotations"] = annotations

        if labels:
            targets["labels"] = labels

        if targets:
            for target, items_to_override in targets.items():
                for name, value in items_to_override.items():
                    self.__dict__[f"common_{target}"][name] = value
                    for alert in self.alerts:
                        alert.__dict__[target][name] = value

            self.update_specific_elements(list(targets.keys()))

    # --------------------------------------------------------------------------

    def add_prefix(
        self,
        annotations: Optional[Dict[str, str]] = None,
        labels: Optional[Dict[str, str]] = None,
    ) -> None:
        """Adds prefix to annotations and labels.

        Args:
            annotations (Optional[Dict[str, str]], optional): Dictionary with
                annotation names that should be updated and values representing
                the to be added prefix. Defaults to `None`.
            labels (Optional[Dict[str, str]], optional): Dictionary with
                labels names that should be updated and values representing
                the to be added prefix. Defaults to `None`.
        """

        targets: Dict[Literal["annotations", "labels"], Dict[str, str]] = {}

        if annotations:
            targets["annotations"] = annotations

        if labels:
            targets["labels"] = labels

        if targets:
            for target, prefixes_to_add in targets.items():
                for name, prefix in prefixes_to_add.items():
                    self.__dict__[f"common_{target}"][name] = (
                        prefix + self.__dict__[f"common_{target}"][name]
                    )
                    for alert in self.alerts:
                        alert.__dict__[target][name] = (
                            prefix + alert.__dict__[target][name]
                        )

            self.update_specific_elements(list(targets.keys()))

    # --------------------------------------------------------------------------

    
class Matcher(BaseModel):
    name: str
    value: str
    isRegex: bool
    isEqual: bool = True


class AlertManagerSilence(BaseModel):
    # https://github.com/prometheus/alertmanager/blob/f958b8be84b870e363f7dafcbeb807b463269a75/api/v2/openapi.yaml#L327-L347
    matchers: List[Matcher]
    startsAt: datetime
    endsAt: datetime
    createdBy: str
    comment: str
