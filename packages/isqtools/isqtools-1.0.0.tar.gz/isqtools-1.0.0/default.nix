{ lib
, buildPythonPackage

  # build-system
, hatchling

  # dependencies
, numpy
, requests
, autograd
, # tests
  pytestCheckHook
, ...
}:
buildPythonPackage rec {
  pname = "isqtools";
  version = "1.0.0";
  src = ./.;

  pyproject = true;

  build-system = [ hatchling ];
  dependencies = [ numpy autograd requests ];
  nativeBuildInputs = [ ];
  buildInputs = [ ];
  propagatedBuildInputs = [ ];

  doCheck = false;
  # nativeCheckInputs = [
  #   pytestCheckHook
  # ];

  pythonImportsCheck = [ ];

  meta = { };
}
