import os.path
import nixops.plugins
from nixops.plugins import Plugin


class NixopsGrafanaPlugin(Plugin):
    @staticmethod
    def nixexprs():
        return [os.path.dirname(os.path.abspath(__file__)) + "/nix"]

    @staticmethod
    def load():
        return [
            "nixops_grafana.resources",
        ]


@nixops.plugins.hookimpl
def plugin():
    return NixopsGrafanaPlugin()
