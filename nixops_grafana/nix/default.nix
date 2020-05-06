{
  config_exporters = { ... }: [];
  options = [];
  resources =
    { evalResources, zipAttrs, resourcesByType, ...}:
    {
      grafanaAlerts = evalResources ./grafana-alert.nix (zipAttrs resourcesByType.grafanaAlerts or []);
      grafanaDashboards = evalResources ./grafana-dashboard.nix (zipAttrs resourcesByType.grafanaDashboards or []);
    };
}
