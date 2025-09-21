{
  description = "Python environment with matplotlib";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs";

  outputs = { self, nixpkgs }:
    let
      pkgs = import nixpkgs { system = "x86_64-linux"; };
    in
    {
      devShells.default = pkgs.mkShell {
        buildInputs = [
          pkgs.python3
          pkgs.python3Packages.matplotlib
        ];
      };
    };
}

