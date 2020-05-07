lib: name:
with lib;
{

  apiToken = mkOption {
    default = "";
    example = "eyJrIjoiT0tTcG1pUlY2RnVKZTFVaDFsNFZXdE9ZWmNrMkZYbk";
    type = types.str;
    description = ''
      Grafana API Token generated in the 'API Keys' section
    '';
  };

}
