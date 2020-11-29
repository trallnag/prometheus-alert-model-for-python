# Copyright © 2020 Tim Schwenke <tim.and.trallnag+code@gmail.com>
# Licensed under Apache License 2.0 <http://www.apache.org/licenses/LICENSE-2.0>

from datetime import datetime
from re import Pattern, compile
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field, validator


class Alert(BaseModel):
    fingerprint: str
    status: str
    starts_at: datetime = Field(alias="startsAt")
    ends_at: datetime = Field(alias="endsAt")
    generator_url: str = Field(alias="generatorURL")
    annotations: Dict[str, str]
    labels: Dict[str, str]

    specific_annotations: Dict[str, str] = {}
    specific_labels: Dict[str, str] = {}

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

    def update_specific(self) -> None:
        """Updates specific labels and annotations."""

        for alert in self.alerts:
            alert.specific_annotations = {
                name: alert.annotations[name]
                for name in set(alert.annotations) - set(self.common_annotations)
            }

            alert.specific_labels = {
                name: alert.labels[name]
                for name in set(alert.labels) - set(self.common_labels)
            }

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

        target = {}
        
        if annotations:
            target["annotations"] = annotations

        if labels:
            target["labels"] = labels

        for target, names_to_pop in target.items():

            if isinstance(names_to_pop, str):
                names_to_pop = [names_to_pop]

            for name_to_pop in names_to_pop:
                self.__dict__[f"common_{target}"].pop(name_to_pop, None)

                for alert in self.alerts:
                    alert.__dict__[target].pop(name_to_pop, None)
                    alert.__dict__[f"specific_{target}"].pop(name_to_pop, None)

    # --------------------------------------------------------------------------

        if labels:
            if isinstance(labels, str):
                labels = (labels,)
            for label in labels:
                self.common_labels.pop(label, None)
                for alert in self.alerts:
                    alert.labels.pop(label, None)
                    alert.specific_labels.pop(label, None)


# ==============================================================================
