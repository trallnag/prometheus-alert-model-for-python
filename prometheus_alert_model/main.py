# Copyright © 2020 Tim Schwenke <tim.and.trallnag+code@gmail.com>
# Licensed under Apache License 2.0 <http://www.apache.org/licenses/LICENSE-2.0>

from datetime import datetime
from typing import Dict, List, Optional, Sequence

from pydantic import BaseModel, Field, validator

# ==============================================================================


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


# ==============================================================================
