from nixops.resources import ResourceOptions
from typing import Optional


class GrafanaFolderOptions(ResourceOptions):
    auth: str
    grafanaHost: str
    title: str
    folderId: Optional[int]
    uid: Optional[str]
