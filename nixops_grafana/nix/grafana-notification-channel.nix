{ config, lib, uuid, name, ... }:

with lib;

{

  imports = [ ./common-grafana-options.nix ];

  options = {

    name = mkOption {
      default = "";
      example = "nixos-organization";
      type = types.str;
      description = ''
        The name of the organization in Grafana
      '';
    };

    type = mkOption {
      default = "";
      example = "nixos-organization";
      type = types.str;
      description = ''
        The name of the organization in Grafana
      '';
    };

    id = mkOption {
      default = "";
      example = "nixos-organization";
      type = types.str;
      description = ''
        The name of the organization in Grafana
      '';
    };

  };

  config._type = "grafana-notification-channel";

}