from nixops.resources import ResourceOptions
from typing import Optional


class GrafanaFolderOptions(ResourceOptions):
    apiToken: str
    host: str
    title: str
    folderId: Optional[int]
    uid: Optional[str]
