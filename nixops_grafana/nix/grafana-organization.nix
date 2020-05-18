{ config, lib, uuid, name, ... }:

with lib;

{

  imports = [ ./common-grafana-options.nix ];

  options = {

    organization = mkOption {
      default = "";
      example = "nixos-organization";
      type = types.str;
      description = ''
        The name of the organization in Grafana
      '';
    };


  };

  config._type = "grafana-organization";

}