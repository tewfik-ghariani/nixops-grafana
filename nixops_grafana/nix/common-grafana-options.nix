{ config, lib, ...}:
with lib;
{

  options = {
    apiToken = mkOption {
      default = "";
      example = "eyJrIjoiT0tTcG1pUlY2RnVKZTFVaDFsNFZXdE9ZWmNrMkZYbk";
      type = types.str;
      description = ''
        Grafana API Token generated in the 'API Keys' section
      '';
    };

    grafanaHost = mkOption {
      default = "grafana.com";
      example = "grafana.prod.nixos.come";
      type = types.str;
      description = ''
        The URL of the Grafana installation
        This is required to contact your corresponding API
      ''
    };

    organization = mkOption {
      default = "";
      example = "nixos-organization";
      type = types.str;
      description = ''
        The name of the organization in Grafana
      '';
    };

  };
}
