{
  description = "TapisUI DevEnv";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        python = pkgs.python312;
        tapipyPython = python.withPackages (ps: [
          ps.requests
          ps.pip
          ps.pyaml
          ps.openapi-core
          ps.atomicwrites
        ]);
        commonPackages = [
          tapipyPython
          pkgs.docker
          pkgs.poetry
          pkgs.gnugrep
          pkgs.xdg-utils
          pkgs.which
          pkgs.ripgrep
          pkgs.fd
          pkgs.libffi # needed for cffi package which is a dependency of something
        ];
      in {
        devShells = {
          default = pkgs.mkShell {
            packages = commonPackages;
            shellHook = ''
              echo ""
              echo "Entering tapipy nix shell..."
              echo "Python:  $(python --version)"
              echo "Poetry:  $(poetry --version)"
              echo "Nix:     $(nix --version)"
              ## check docker is running
              if ! docker info > /dev/null 2>&1; then
                echo "Docker:  Not running. Please start Docker on host. Some commands may not work."
              else
                echo "Docker:  $(docker -v)"
              fi
              poetry env use $(which python)

              echo ""
              echo "Available Makefile commands:"
              echo "=============================="
              echo "  - make build        # Build the Python package"
              echo "  - make install      # Install the Python package"
              echo "  - make test         # Run tests (in Docker) (must place password in Makefile)"
              echo "  - make pull_specs   # Update OpenAPI specs"
              echo ""
              echo "You can run these make commands directly inside this shell."
              echo ""
              echo "Available Python poetry commands:" 
              echo "==================================="
              echo "  - poetry install       # Install dependencies"
              echo "  - poetry update        # Update dependencies"
              echo "  - poetry env activate  # Enter a poetry shell"
              echo "  - poetry env list      # List poetry environments"
              echo "  - poetry env info      # Show poetry environment info"
              echo "  - poetry run <sh>      # Run command in poetry environment"
              echo "  - poetry build         # Build the package"
              echo "  - poetry publish --username=__token__ --password=pypi-TOKEN  # Publish the package"
              echo ""
            '';
          help = pkgs.mkShell {
            packages = commonPackages;
            shellHook = ''
              echo "Entering TapisUI nix shell..."
              echo "Available make commands:"
              echo "========================="
              make help
            '';
            };
          };
        };
      }
    );
}

