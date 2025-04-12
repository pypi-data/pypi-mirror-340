<div align="center">
    <h1>pyro_dash_py</h1>
    <p style="font-size: 18px;">A pretty light-weight and somewhat bearable python-sdk for the pyro-dashboard-api</p>
</div>

[![Deploy Docs](https://github.com/pyrologix/pyro_dash_py/actions/workflows/deploy-docs.yml/badge.svg)](https://github.com/pyrologix/pyro_dash_py/actions/workflows/deploy-docs.yml)
[![Build and Release](https://github.com/pyrologix/pyro_dash_py/actions/workflows/build.yml/badge.svg)](https://github.com/pyrologix/pyro_dash_py/actions/workflows/build.yml)
[![Tests](https://github.com/pyrologix/pyro_dash_py/actions/workflows/run_tests.yml/badge.svg)](https://github.com/pyrologix/pyro_dash_py/actions/workflows/run_tests.yml)

Visit `pyro_dash_py`'s full documentation here: https://pyrologix.github.io/pyro_dash_py/

## Installation

`pyro_dash_py` has a public [pypi package](https://pypi.org/project/pyro-dash-py/) that you can install.

```bash
pip install pyro_dash_py
```

## Speed Run Usage

First, initialize the `PyroDash` client, make sure you are specifying your own api key.

```python
pyro = PyroDash(
    host="https://api.dashboard.pyrologix.com",
    email="dev@pyrologix.com",
    apikey="my-super-secret-key",
)
```

Now you can create some projects and jobs:

```python
my_project = pyro.projects.create(name="Hello from pyro_dash_py")
my_job = pyro.jobs.create("wildest")

my_project.add_job(my_job.id)
```

## For Contributors

This project uses poetry to manage dependencies and virtual environments. You're gonna need that.

You can follow the installation instructions [here](https://python-poetry.org/docs/#installing-with-the-official-installer) or you can just run the command below:

```bash
curl -sSL https://install.python-poetry.org | python3 -
source ~/.zshrc # or whatever shell you're using
```

Then you can clone this repo and install dependencies:

```bash
git clone https://github.com/pyrologix/pyro_dash_py.git
poetry install --with dev

# and you should be able to run the test suite
poetry run pytest
```

You are encouraged to check out the `examples/` in order to get a feel for usage.

## Releases

Once a code change has been made in this repository in `main`, it does not automatically become available in pip as a new version.
In order to create a new release and have it available through pip, do the following:

```bash
git checkout main
git pull # make sure you're up-to-date with current main
git checkout <my release branch>

poetry version patch # can also be minor/major version bump- default to just patch
>>> Bumping version from 0.1.0 to 0.1.1

git add pyproject.toml
git commit -m "Bump version to 0.1.1"

git tag v0.1.1 # vN.N.N pattern required for CI/CD hooks

git push origin <my release branch>
git push origin v0.1.1

```

A pull request will then be required to get these changes into `main`.

On merge of the release branch to `main`, Github actions will manage the necessary steps to make a new version of the package
available. Pip may not immediately update with the new package version, but within a few hours it should show up on the [web page](https://pypi.org/project/pyro-dash-py/) and will then be available to download via pip.

## Docs

- `poetry run mkdocs serve` - Start the live-reloading docs server.
- `poetry run mkdocs build` - Build the documentation site.
