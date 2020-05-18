{ config, lib, uuid, name, ... }:

with lib;

{

  imports = [ ./common-grafana-options.nix ];

  options = {

    title = mkOption {
      example = "Folder Title;
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

    uid = mkOption {
      example = "cIBgcSjkk";
      default = "";
      type = types.str;
      description = ''
        ....
      '';
    };



  };

  config._type = "grafana-folder";

}