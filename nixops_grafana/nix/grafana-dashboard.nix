{ config, lib, uuid, name, ... }:

with lib;

{

  imports = [ ./common-grafana-options.nix ];

  options = {

    id = mkOption {
      example = "9619";
      default = "";
      type = types.str;
      description = ''
        The identifier of a dashboard. Only unique per Grafana install.
        It is a numeric value generated in an auto-incrementing fashion.
        Should be left empty to create a new dashboard
      '';
    };

    uid = mkOption {
      example = "cIBgcSjkk";
      default = "";
      type = types.str;
      description = ''
        A unique identifier of a dashboard across all Grafana organizations.
        Automatically generated if not provided when creating a dashboard.
        Should be left empty to create a new dashboard
      '';
    };

    title = mkOption {
      example = "Operations Super Dashboard";
      type = types.str;
      description = ''
        The title of the dashboard
      '';
    };

    tags = mkOption {
      default = [ ];
      example = [ "random" "tags" ];
      type = types.listOf types.str;
      description = ''
        Tags associated to the dashboard
      '';
    };

    config_json = mkOption {
      example = "dashboard.json";
      type = types.str;
      description = ''
        Tags associated to the dashboard
      '';
    };


  };

  config._type = "grafana-dashboard";

}