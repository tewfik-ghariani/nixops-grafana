{ config, lib, uuid, name, ... }:

with lib;
with import <nixops/lib.nix> lib;

{

  imports = [ ./common-grafana-options.nix ];

  options = {

    dashboardId = mkOption {
      example = 9619;
      default = null;
      type = types.nullOr types.int;
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
        A unique identifier of a dashboard across all Grafana installations.
        Automatically generated if not provided when creating a dashboard.
        Should be left empty to create a new dashboard
      '';
    };

    title = mkOption {
      example = "Operations Super Dashboard";
      default = "";
      type = types.str;
      description = ''
        The title of the dashboard
      '';
    };

    tags = mkOption {
      example = [ "random" "tags" ];
      default = [ ];
      type = types.listOf types.str;
      description = ''
        Tags associated to the dashboard
      '';
    };

    folder = mkOption {
      example = 4;
      default = 0;
      type = types.nullOr (types.either types.int (resource "grafana-folder"));
      description = ''
        Parent folder containing the dashboard.
        May be a folder ID or a folder resource created by nixops
        Can be omitted to have the dashboard in the General folder (id=0).
      '';
    };

    template = mkOption {
      example = "/data/grafana_templates/operations_dashboard.json";
      default = null;
      type = types.nullOr types.path;
      description = ''
        JSON file containing a description of a Grafana dashboard
        The template is used similarly to the 'Upload Json' feature in Grafana.
      '';
    };

  };

  config._type = "grafana-dashboard";

}
