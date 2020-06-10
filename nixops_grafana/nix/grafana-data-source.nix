{ config, lib, uuid, name, ... }:

with lib;

{

  imports = [ ./common-grafana-options.nix ];

  options = {

    name = mkOption {
      example = "Folder Title";
      type = types.str;
      description = ''
        The name of the folder
      '';
    };

    id = mkOption {
      example = "9619";
      default = "";
      type = types.str;
      description = ''
          ...
      '';
    };

    type = mkOption {
      example = "cIBgcSjkk";
      default = "";
      type = types.str;
      description = ''
        ....
      '';
    };

    url = mkOption {
      example = "cIBgcSjkk";
      default = "";
      type = types.str;
      description = ''
        ....
      '';
    };

        database_name = mkOption {
      example = "cIBgcSjkk";
      default = "";
      type = types.str;
      description = ''
        ....
      '';
    };

  };

  config._type = "grafana-data-source";

}
