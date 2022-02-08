{ pkgs }:

self: super: {
  nixops = super.nixops.overridePythonAttrs (
    { nativeBuildInputs ? [], ... }: {
      format = "pyproject";
      nativeBuildInputs = nativeBuildInputs ++ [ self.poetry ];
    }
  );

  grafana-client = super.grafana-client.overridePythonAttrs (old: {
    postPatch = ''
      substituteInPlace setup.py --replace 'version=get_version()' 'version="${old.version}"'
    '';
  });
}
