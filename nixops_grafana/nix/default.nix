{
  config_exporters = { ... }: [];
  options = [];
  resources =
    { evalResources, zipAttrs, resourcesByType, ...}:
    {
      grafanaDashboards = evalResources ./grafana-dashboard.nix (zipAttrs resourcesByType.grafanaDashboards or []);
      grafanaDataSources = evalResources ./grafana-data-source.nix (zipAttrs resourcesByType.grafanaDataSources or []);
      grafanaFolders = evalResources ./grafana-folder.nix (zipAttrs resourcesByType.grafanaFolders or []);
      grafanaNotificationChannels = evalResources ./grafana-notification-channel.nix (zipAttrs resourcesByType.grafanaNotificationChannels or []);
      grafanaOrganizations = evalResources ./grafana-organization.nix (zipAttrs resourcesByType.grafanaOrganizations or []);
    };
}
