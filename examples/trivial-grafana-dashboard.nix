{ 
  organization ? ""
, apiToken ? ""
, host ? "grafana.monocle.com"
, ...
}:
{
  resources.grafanaFolders.parent-folder =
    {
      inherit apiToken host;
      title = "Nixops Folder";
    };
  resources.grafanaDashboards.first-grafana-dashboard =
    { resources, ... }:
    {
      inherit apiToken host;
      title = "First nixops Dashboard";
      folder = resources.grafanaFolders.parent-folder;
      #configJson = dashboard.json;
    };
}
