# -*- coding: utf-8 -*-

from grafana_api.grafana_api import (
    GrafanaBadInputError,
    GrafanaClientError,
)

import nixops.util
import nixops.resources
from nixops.state import RecordId

from nixops_grafana import grafana_utils
from .types.grafana_folder import GrafanaFolderOptions


class GrafanaFolderDefinition(nixops.resources.ResourceDefinition):
    """Definition of a Grafana Folder"""

    config: GrafanaFolderOptions

    @classmethod
    def get_type(cls):
        return "grafana-folder"

    @classmethod
    def get_resource_type(cls):
        return "grafanaFolders"

    def show_type(self):
        return "{0}".format(self.get_type())

    def __init__(self, name: str, config: nixops.resources.ResourceEval):
        super().__init__(name, config)


class GrafanaFolderState(nixops.resources.ResourceState[GrafanaFolderDefinition]):
    """State of a Grafana Folder"""

    auth = nixops.util.attr_property("auth", None)
    grafana_host = nixops.util.attr_property("grafanaHost", None)
    title = nixops.util.attr_property("title", None)
    folder_id = nixops.util.attr_property("folderId", None, int)
    uid = nixops.util.attr_property("uid", None)

    @classmethod
    def get_type(cls):
        return "grafana-folder"

    def __init__(self, depl: nixops.deployment.Deployment, name: str, id: RecordId):
        super().__init__(depl, name, id)

    def _exists(self):
        return self.state == self.UP

    def show_type(self):
        s = super(GrafanaFolderState, self).show_type()
        # Add more details maybe
        return s

    @property
    def resource_id(self):
        # grafana_host + uid
        return self.uid

    def create(self, defn, check, allow_reboot, allow_recreate):
        if self._exists():
            if defn.config.uid and self.uid != defn.config.uid:
                raise Exception("Cannot update the uid of a folder.")

            if not defn.config.title:
                raise Exception(
                    "The folder 'title' of '{0}' cannot be empty.".format(defn.name)
                )

            if self.title != defn.config.title:
                self.log(
                    "Noticed that the title has been changed from '{0}' to '{1}'...".format(
                        self.title, defn.config.title
                    )
                )
                if self.depl.logger.confirm(
                    "are you sure you want to update the Folder title ?"
                ):
                    grafana_api = grafana_utils.connect(
                        auth=self.auth, host=self.grafana_host
                    )
                    try:
                        grafana_api.folder.update_folder(
                            uid=self.uid, title=defn.config.title, overwrite=True
                        )
                    except GrafanaClientError:
                        self.log(
                            "The folder seems to have been destroyed outside of nixops.."
                        )
                        self.state = self.MISSING
                    except Exception:
                        self.log(
                            "Failed updating the title of the folder with uid '{0}'..".format(
                                self.uid
                            )
                        )
                        raise
                    self.title = defn.config.title
                    self.log(
                        "Updated the folder title successfully : '{0}'".format(
                            self.title
                        )
                    )

        if not self._exists():
            if not defn.config.title:
                raise Exception(
                    "You must specify the folder 'title' of '{0}'..".format(defn.name)
                )

            self.log("Creating folder : '{0}'..".format(defn.config.title))

            grafana_api = grafana_utils.connect(
                auth=defn.config.auth, host=defn.config.grafanaHost
            )
            try:
                new_folder = grafana_api.folder.create_folder(
                    title=defn.config.title,
                    uid=defn.config.uid,
                )
            except GrafanaBadInputError:
                self.log("Creation failed for folder ‘{0}’...".format(defn.name))
                raise

            self.log("Folder created..")
            with self.depl._db:
                self.state = self.UP
                self.auth = defn.config.auth
                self.grafana_host = defn.config.grafanaHost
                self.folder_id = new_folder["id"]
                self.uid = new_folder["uid"]
                self.title = new_folder["title"]
                self.url = self.grafana_host + new_folder["url"]

            self.log("Folder URL is '{0}'.".format(self.url))

    def _check(self):
        if not self.uid:
            self.state = self.MISSING
            return
        grafana_api = grafana_utils.connect(auth=self.auth, host=self.grafana_host)
        try:
            folder_info = grafana_api.folder.get_folder(uid=self.uid)
            if folder_info["uid"] == self.uid:
                self.state = self.UP
            if folder_info["title"] != self.title:
                self.log(
                    "The title has been changed outside of nixops to '{0}'".format(
                        folder_info["title"]
                    )
                )
                self.log("Run deploy to correct the title of this folder")
                self.title = folder_info["title"]
        except GrafanaClientError:
            self.state = self.MISSING
        except Exception:
            self.state = self.MISSING
        return

    def _destroy(self):
        grafana_api = grafana_utils.connect(auth=self.auth, host=self.grafana_host)
        try:
            grafana_api.folder.delete_folder(uid=self.uid)
        except GrafanaClientError:
            self.log("The folder seems to have already been deleted..")
        except Exception:
            self.log("Deletion failed for folder ‘{0}’...".format(self.title))
            raise

        self.log(
            "Folder '{0}' with uid '{1}' has been deleted.".format(self.title, self.uid)
        )
        return

    def destroy(self, wipe=False):
        if not self._exists():
            return True

        if not self.depl.logger.confirm(
            "are you sure you want to destroy Grafana Folder '{0}'?".format(self.title)
        ):
            return False

        self.log("Destroying Grafana Folder '{0}'...".format(self.uid))
        self._destroy()
        return True
