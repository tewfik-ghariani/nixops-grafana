# -*- coding: utf-8 -*-

from typing import (
    Optional,
    Literal,
    Union,
    Tuple,
)
from grafana_client import GrafanaApi


def connect(
    auth: str,
    host: str,
    protocol: Literal["http", "https"] = "https",
):
    token: Union[Tuple, str]
    if ":" in auth:
        # username:password
        token = tuple(auth.split(":"))
    else:
        # API token
        token = auth

    grafana_api = GrafanaApi(auth=token, host=host, protocol=protocol)
    return grafana_api
