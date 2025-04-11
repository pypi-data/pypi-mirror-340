{ lib
, buildPythonPackage
, fetchPypi

, # build-system
  setuptools

  #dep
, cirq-core
, deprecation
, h5py
, networkx
, numpy
, requests
, scipy
, sympy

, # tests
  pytestCheckHook
, ...
}:
buildPythonPackage rec {
  pname = "openfermion";
  version = "1.6.1";
  format = "setuptools";
  # pyproject = false;

  src = fetchPypi {
    inherit pname version;
    hash = "sha256-1/HfTPmP6qV3oHDLQy49BYY8c6TzvB99ESkUzyo8m8s=";
  };

  build-system = [ setuptools ];

  dependencies = [
    cirq-core
    deprecation
    h5py
    networkx
    numpy
    requests
    scipy
    sympy
  ];

  nativeBuildInputs = [ ];
  propagatedBuildInputs = [ ];
  buildInputs = [ ];

  doCheck = false;
  # nativeCheckInputs = [
  #   pytestCheckHook
  # ];

  pythonImportsCheck = [ ];

  meta = { };
}
