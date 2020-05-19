{ config, lib, uuid, name, ... }:

with lib;
with import <nixops/lib.nix> lib;

{

  imports = [ ./common-grafana-options.nix ];

  options = {

    dashboardId = mkOption {
      example = "9619";
      default = "";
      type = types.nullOr types.str;
      description = ''
        The identifier of a dashboard. Only unique per Grafana install.
        It is a numeric value generated in an auto-incrementing fashion.
        Should be left empty to create a new dashboard
      '';
    };

    uid = mkOption {
      example = "cIBgcSjkk";
      default = "";
      type = types.nullOr types.str;
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

    folder = mkOption {
      example = "faefae";
      type = types.nullOr (types.either types.str (resource "grafana-folder"));
      description = ''
        Parent folder containing the dashboard.
        May be a folder ID or a resource created by nixops
        Can be omitted to have the dashboard at the general level
      '';
    };

#   configJson = mkOption {
#      example = { };
#      type = types.nullOr types.attrs;
#      description = ''
#        JSON template describing the dashboard
#      '';
#    };


  };

  config._type = "grafana-dashboard";

}
