# Template for running Molecular Studio V Workflows

[![License](https://img.shields.io/github/license/rowansci/rowan-sample-env)](https://github.com/rowansci/rowan-sample-env/blob/master/LICENSE)
[![Powered by: Pixi](https://img.shields.io/badge/Powered_by-Pixi-facc15)](https://pixi.sh)

This environment is used to run Molecular Studio V Workflows.It uses `pixi` and `direnv` to manage the environment. To use this repo, you need to have `pixi` and `direnv` installed. To copy this for your project, click the green `Use this template` button in the top right of this page.

## Installation

> [!NOTE]
> Windows Users: Please use WSL for running the Molecule Studio V environment

### Pixi

To install pixi you can run the following command in your terminal:

```sh
curl -fsSL https://pixi.sh/install.sh | sh
```

if your system does not have `curl` installed, you can install it with `wget`:

```sh
wget -qO- https://pixi.sh/install.sh | sh
```

#### Direnv

See [direnv](https://direnv.net/) for more information on how to install it.

## Getting Started
Once you have `pixi` and `direnv` installed, you can use the following commands to get started:
```sh
pixi run setup
```

You will be required to enter your MongoDB URI for your `Fireworks` database. If you are starting from scratch without any workflows in your database, you can run the following command to initialize the database:
```sh
pixi run fireworks_setup
```

You will need to allow `direnv` to load the environment via `direnv allow .`. The environment should now automagically load/unload every time you `cd` into/out of the directory.

## Running Workflows

To run a workflow, you can use the following command:
```sh
pixi run launch
```

