{ config, lib, ...}:
with lib;
{

  options = {
    auth = mkOption {
      default = "";
      example = "eyJrIjoiT0tTcG1pUlY2RnVKZTFVaDFsNFZXdE9ZWmNrMkZYbk";
      type = types.str;
      description = ''
        Authentication code to access Grafana API, can be one of the following :
          - API Token generated in the 'API Keys' section
          - username:password basic authentication ( single string separated by a colon )
      '';
    };

    grafanaHost = mkOption {
      example = "grafana.nixos.com";
      type = types.str;
      description = ''
        The URL of the Grafana installation
        This is required to contact your corresponding API
      '';
    };

    protocol = mkOption {
      example = "https";
      default = "https";
      type = types.str;
      description = ''
        The HTTP protocol to be using while submitting requests to the Grafana Host
        Either "http" or "https"
      '';
    };
  };

}
