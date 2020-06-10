# -*- coding: utf-8 -*-

import json

from grafana_api.grafana_api import (
    GrafanaBadInputError,
    GrafanaClientError,
    GrafanaServerError,
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

import nixops.util
import nixops.resources
from nixops.state import RecordId

from nixops_grafana import grafana_utils
from .types.grafana_dashboard import GrafanaDashboardOptions


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

    def __init__(self, name: str, config: nixops.resources.ResourceEval):
        super().__init__(name, config)


class GrafanaDashboardState(nixops.resources.ResourceState[GrafanaDashboardDefinition]):
    """State of a Grafana Dashboard"""

    api_token = nixops.util.attr_property("apiToken", None)
    host = nixops.util.attr_property("host", None)
    dashboard_id = nixops.util.attr_property("dashboardId", None, int)
    uid = nixops.util.attr_property("uid", None)
    title = nixops.util.attr_property("title", None)
    tags = nixops.util.attr_property("tags", [], "json")
    folder = nixops.util.attr_property("folder", None, int)
    template = nixops.util.attr_property("template", None)

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

    def create(self, defn, check, allow_reboot, allow_recreate):
        if self._exists():
            if defn.config.uid and self.uid != defn.config.uid:
                raise Exception("Cannot update the uid of a dashboard.")

        grafana_api = grafana_utils.connect(
            api_token=defn.config.apiToken, host=defn.config.host
        )
        # Update using the json template regardless?
        self.log("Creating/Updating grafana dashboard..")

        if self.folder and self.folder != defn.config.folder:
            self.log(
                "Noticed that the folder has been changed from '{0}' to '{1}'...".format(
                    str(self.folder), str(defn.config.folder)
                )
            )
            raise Exception(
                "Destroy the dashboard then re-deploy to create it under a different folder."
            )

        # ToDo This is still not working when folder is another resource.
        if isinstance(defn.config.folder, int):
            folder = defn.config.folder
        elif defn.config.folder:
            folder = defn.config.folder.folderId
        else:
            folder = 0

        try:
            template = json.loads(open(defn.config.template, "r").read())
        except Exception:
            self.log("Could not parse the template JSON file")
            raise

        try:
            # Create or update a dashboard
            dashboard_info = grafana_api.dashboard.update_dashboard(
                dashboard={
                    "dashboard": template,
                    "folderId": folder,
                    "overwrite": True,
                }
            )
        except GrafanaBadInputError:
            self.log("Creation failed for dashboard ‘{0}’...".format(defn.name))
            raise
        except GrafanaClientError:
            self.log("A dashboard with the specified ID or UID does not exist.")
            raise
        except GrafanaServerError:
            raise Exception(
                "Probably the parent folder of the dashboard with ID '{0}' does not exist".format(
                    str(folder)
                )
            )

        self.log("Dashboard created/updated..")
        with self.depl._db:
            self.state = self.UP
            self.api_token = defn.config.apiToken
            self.host = defn.config.host
            self.dashboard_id = dashboard_info["id"]
            self.uid = dashboard_info["uid"]
            self.url = self.host + dashboard_info["url"]
            self.folder = folder
            self._check()

        self.log("Dashboard URL is '{0}'.".format(self.url))

    def _check(self):
        if not self.uid:
            self.state = self.MISSING
            return
        grafana_api = grafana_utils.connect(api_token=self.api_token, host=self.host)
        try:
            dashboard_info = grafana_api.dashboard.get_dashboard(dashboard_uid=self.uid)
            if dashboard_info["dashboard"]["uid"] == self.uid:
                self.state = self.UP
                self.title = dashboard_info["dashboard"]["title"]
        except Exception:
            self.state = self.MISSING
        return

    def _destroy(self):
        grafana_api = grafana_utils.connect(api_token=self.api_token, host=self.host)
        try:
            grafana_api.dashboard.delete_dashboard(dashboard_uid=self.uid)
        except GrafanaClientError:
            self.log("The dashboard seems to have already been deleted..")
        except Exception:
            self.log("Deletion failed for dashboard ‘{0}’...".format(self.title))
            raise

        self.log(
            "Dashboard '{0}' with uid '{1}' has been deleted.".format(
                self.title, self.uid
            )
        )
        return

    def destroy(self, wipe=False):
        if not self._exists():
            return True

        if not self.depl.logger.confirm(
            "are you sure you want to destroy Grafana Dashboard '{0}'?".format(
                self.title
            )
        ):
            return False

        self.log("Destroying Grafana Dashboard '{0}'...".format(self.uid))
        self._destroy()
        return True
