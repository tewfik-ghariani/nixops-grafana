# -*- coding: utf-8 -*-

import nixops.util
import nixops.resources
from nixops.state import RecordId

from typing import (
    Optional,
    Dict,
    List,
    Generator,
    Union,
    Callable,
)

from grafana_api.grafana_face import GrafanaFace
from grafana_api.grafana_api import (
    GrafanaBadInputError,
    GrafanaClientError,
)
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

#from nixops_grafana.resources.grafana_folder import GrafanaFolderDefinition


class GrafanaDashboardOptions(nixops.resources.ResourceOptions):
    apiToken: str
    host: str
    dashboardId: Optional[str]
    uid: Optional[str]
    title: Optional[str]
    folder: Optional[Union[str, nixops.resources.ResourceEval]]
    configJson: Optional[Dict]
    tags: Optional[tuple]


class GrafanaDashboardDefinition(nixops.resources.ResourceDefinition):
    """Definition of a Grafana Dashboard"""

    config: GrafanaDashboardOptions

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


class GrafanaDashboardState(nixops.resources.ResourceState[GrafanaDashboardDefinition]):
    """State of a Grafana Dashboard"""

    api_token = nixops.util.attr_property("apiToken", None)
    host = nixops.util.attr_property("host", None)
    dashboard_id = nixops.util.attr_property("dashboardId", None)
    uid = nixops.util.attr_property("uid", None)
    title = nixops.util.attr_property("title", None)
    folder = nixops.util.attr_property("folder", None)
    tags = nixops.util.attr_property("tags", {}, "json")
    config_json = nixops.util.attr_property("configJson", {}, "json")

    @classmethod
    def get_type(cls):
        return "grafana-dashboard"

    def __init__(self, depl: nixops.deployment.Deployment, name: str, id: RecordId):
        super().__init__(depl, name, id)

    def _exists(self):
        return self.state == self.UP

    def show_type(self):
        s = super(GrafanaDashboardState, self).show_type()
        # Add more details maybe
        return s

    @property
    def resource_id(self):
        # host + uid
        return self.uid

    def connect(self, api_token: str, host: str, protocol: Union['http','https'] = 'https'):
        self.grafana_api = GrafanaFace(auth=api_token, host=host, protocol=protocol)
        return

    def create(self, defn, check, allow_reboot, allow_recreate):
        if self._exists(): return

        self.connect(api_token=defn.config.apiToken,
                     host=defn.config.host)
        try:
            new_dashboard = self.grafana_api.dashboard.update_dashboard(
               title=defn.config.title,
               uid=defn.config.uid,
              )
        except GrafanaBadInputError:
            self.log("Creation failed for dashboard ‘{0}’...".format(defn.name))
            self.state = self.MISSING
            raise

        with self.depl._db:
            self.state = self.UP
            self.api_token = defn.config.apiToken
            self.host = defn.config.host
            self.folder_id = new_dashboard['id']
            self.uid = new_dashboard['uid']
            self.title = new_dashboard['title']
            self.url = self.host + new_dashboard['url']

        self.log("Dashboard URL is '{0}'.".format(self.url))


    def _check(self):
        self.log("Get Dashboard : Silent")
        # update state
        return

    def _destroy(self):
        self.connect(api_token=self.api_token,
                     host=self.host)
        self.grafana_api.dashboard.delete_dashboard(dashboard_uid=self.uid)
        return

    def destroy(self, wipe=False):
        if not self._exists(): return True

        if not self.depl.logger.confirm(
            "are you sure you want to destroy Grafana Dashboard '{0}'?".format(self.title)
        ):
            return False

        self.log("Destroying Grafana Dashboard '{0}'...".format(self.uid))
        self._destroy()
        return True
