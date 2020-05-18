# -*- coding: utf-8 -*-

import nixops.util
import nixops.resources

from typing import Optional, Dict, List, Generator, Callable

from grafana_api.grafana_face import GrafanaFace
from grafanalib.core import (
    Alert,
    AlertCondition,
    Dashboard,
    Graph,
    GreaterThan,
    OP_AND,
    OPS_FORMAT,
    Row,
    RTYPE_SUM,
    SECONDS_FORMAT,
    SHORT_FORMAT,
    single_y_axis,
    Target,
    TimeRange,
    YAxes,
    YAxis,
)

class GrafanaDashboardOptions(nixops.resources.ResourceOptions):
    apiToken: str
    host: str


class GrafanaDashboardDefinition(nixops.resources.ResourceDefinition):
    """Definition of a Grafana Dashboard"""

    config: GrafanaDashboardOptions

    api_token : str
    host : str

    @classmethod
    def get_type(cls):
        return "grafana-dashboard"

    @classmethod
    def get_resource_type(cls):
        return "grafanaDashboards"

    def show_type(self):
        return "{0}".format(self.get_type())

    def __init__(self, name: str, config:nixops.resources.ResourceEval):
        super().__init__(name, config)
        self.api_token = config.apiToken
        self.host = config.host


class GrafanaDashboardState(nixops.resources.ResourceState):
    """State of a Grafana Dashboard"""

    #api_token = nixops.util.attr_property("apiToken", None)
    #grafana_host = nixops.util.attr_property("grafanaHost", None)
    #dashboard_id = nixops.util.attr_property("dashboardId", None)
    #dashboard_uid = nixops.util.attr_property("dashboardUid", None)
    #title = nixops.util.attr_property("title", None)

    @classmethod
    def get_type(cls):
        return "grafana-dashboard"

    def __init__(self, depl, name, id):
        nixops.resources.ResourceState.__init__(self, depl, name, id)

    def _exists(self):
        return self.state != self.MISSING

    def show_type(self):
        s = super(GrafanaDashboardState, self).show_type()
        # Add more details maybe
        return s

    @property
    def resource_id(self):
        return self.dashboard_uid

    def create(self, defn, check, allow_reboot, allow_recreate):
        self.log("Create dashboard")

    def check(self):
        self.log("Get Dashboard")
        return

    
    def _destroy(self):
        self.log("Delete request")

    def destroy(self, wipe=False):
        self.check()
        if not self._exists(): return True

        print("Destroying")
        self._destroy()
        return True
