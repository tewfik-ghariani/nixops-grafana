{ 
  organization ? ""
, apiToken ? ""
, ...
}:
{
  resources.grafanaDashboards.firstGrafanaDashboard =
    {
      inherit apiToken;
      host = "grafana.monocle.infor.com";
      title = "First nixops Dashboard";
      config_json = "dashboard.json";
    };
    resources.commandOutput.test =  
    {
      script = ''
        #!/bin/sh
        echo -n '"12345"'
      '';
    };
}
