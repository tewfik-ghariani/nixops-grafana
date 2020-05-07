{ config, lib, uuid, name, ...}:

with lib

{
  options = (import ./common-grafana-options.nix ) // {

    title = mkOption {
      example = "Operations Super Dashboard";
      type = types.str;
      description = ''
        The title of the dashboard
      '';
    };


  };

  config._type = "grafana-dashboard";

}
