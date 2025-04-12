### ansys-api-platform-instancemanagement gRPC Interface Package

![Ansys logo](./doc/source/_static/ansys-logo.png)

This Python package contains the auto-generated gRPC Python interface files for
the Product Instance Management (PIM) API.


#### Installation

Provided that these wheels have been published to public PyPI, they can be
installed with this command:

```
pip install ansys-api-platform-instancemanagement
```

#### Build

To build the gRPC packages, run this command:

```
python -m build
```

The preceding command creates both the source distribution containing only the PROTO files
and the wheel containing the PROTO files and build Python interface files.

Note that the interface files are identical regardless of the version of Python
used to generate them, but the last pre-built wheel for ``grpcio~=1.17`` was
Python 3.7. To improve your build time, use Python 3.7 when building the
wheel.


#### Manual Deployment

After building the packages, manually deploy them with these commands:

```
pip install twine
twine upload dist/*
```

Note that this is automatically done through CI/CD.


#### Automatic Deployment

This repository contains GitHub CI/CD that enables the automatic building of
source and wheel packages for these gRPC Python interface files. By default,
these are built on PRs, the main branch, and on tags when pushing. Artifacts
are uploaded for each PR.

To publicly release wheels to PyPI, ensure your branch is up-to-date and then
push tags. These commands provides an example for the version ``v0.5.0``.

```bash
git tag v0.5.0
git push --tags
```
