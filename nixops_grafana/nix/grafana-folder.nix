{ config, lib, uuid, name, ... }:

with lib;

{

  imports = [ ./common-grafana-options.nix ];

  options = {

    title = mkOption {
      example = "Folder Title";
      type = types.str;
      description = ''
        The name of the folder
      '';
    };

    folderId = mkOption {
      example = "9619";
      default = "";
      type = types.str;
      description = ''
        The identifier of a folder. Only unique per Grafana install.
        It is a numeric value generated in an auto-incrementing fashion.
        Should be left empty to create a new folder
      '';
    };

    uid = mkOption {
      example = "cIBgcSjkk";
      default = "";
      type = types.str;
      description = ''
        A unique identifier of a folder across all Grafana organizations.
        Automatically generated if not provided when creating a folder.
        Should be left empty to create a new folder
      '';
    };


  };

  config._type = "grafana-folder";

}
