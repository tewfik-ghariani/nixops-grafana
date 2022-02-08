{ pkgs ? import <nixpkgs> {} }:
let
  overrides = import ./overrides.nix { inherit pkgs; };
in pkgs.poetry2nix.mkPoetryApplication {
  projectDir = ./.;
  python = pkgs.python39;
  overrides = pkgs.poetry2nix.overrides.withDefaults overrides;
  meta.description = "Nix package for ${pkgs.stdenv.system}";
}
