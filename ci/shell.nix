{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {

  buildInputs = [
    (pkgs.poetry2nix.mkPoetryEnv {
      projectDir = ../.;
      python = pkgs.python38;
      overrides = pkgs.poetry2nix.overrides.withDefaults(self: super: {
        # TODO: Add build input poetry to _all_ git deps in poetry2nix
        nixops = super.nixops.overridePythonAttrs(old: {
          buildInputs = old.buildInputs ++ [
            self.poetry
          ];
        });
        grafana-api = super.grafana-api.overridePythonAttrs (old: {
          postPatch = ''
            substituteInPlace setup.py --replace 'version=get_version()' 'version="${old.version}"'
          '';
        });
      });
    })
  ];

}
