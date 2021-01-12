from nixops.resources import (
    ResourceOptions,
    ResourceEval,
)
from typing import (
    Optional,
    Union,
)


class GrafanaDashboardOptions(ResourceOptions):
    auth: str
    grafanaHost: str
    dashboardId: Optional[int]
    uid: Optional[str]
    title: Optional[str]
    tags: Optional[tuple]
    folder: Optional[Union[int, ResourceEval]]
    template: Optional[str]
