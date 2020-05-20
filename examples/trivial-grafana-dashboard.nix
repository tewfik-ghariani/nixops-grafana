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
      #folder = resources.grafanaFolders.parent-folder;
      #folder = 9900;
      #template = "/home/tewfikghariani/repositories/nix-community/nixops-grafana/examples/empty_dashboard.json";
      template = "/data/grafana_templates/operations_dashboard.json";
    };
}
