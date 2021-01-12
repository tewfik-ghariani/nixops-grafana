{ 
  organization ? ""
, auth ? ""
, grafanaHost ? "grafana.monocle.com"
, ...
}:
{
  network.description = "Grafana Dashboard Example";

  resources.grafanaFolders.parent-folder =
    {
      inherit auth grafanaHost;
      title = "Nixops Folder";
    };
  resources.grafanaDashboards.first-grafana-dashboard =
    { resources, ... }:
    {
      inherit auth grafanaHost;
      folder = resources.grafanaFolders.parent-folder;
      #folder = 9900;
      #template = "/home/tewfikghariani/repositories/nix-community/nixops-grafana/examples/empty_dashboard.json";
      template = "/data/grafana_templates/operations_dashboard.json";
    };
}
