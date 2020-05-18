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

    host = mkOption {
      example = "grafana.nixos.com";
      type = types.str;
      description = ''
        The URL of the Grafana installation
        This is required to contact your corresponding API
      '';
    };

  };
}
