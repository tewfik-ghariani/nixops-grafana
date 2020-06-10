# -*- coding: utf-8 -*-

from typing import (
    Optional,
    Literal,
)

from grafana_api.grafana_face import GrafanaFace


def connect(
    api_token: str, host: str, protocol: Literal["http", "https"] = "https",
):
    grafana_api = GrafanaFace(auth=api_token, host=host, protocol=protocol)
    return grafana_api
