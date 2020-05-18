{ 
  organization ? ""
, apiToken ? ""
, ...
}:
{
  resources.grafanaDashboards.firstGrafanaDashboard =
    {
      inherit apiToken;
      dashboardId = "";
      grafanaHost = "grafana.monocle.infor.com";
      title = "First Testing Dashboard";
    };
    resources.commandOutput.test =  
    {
      script = ''
        #!/bin/sh
        echo -n '"12345"'
      '';
    };
}
