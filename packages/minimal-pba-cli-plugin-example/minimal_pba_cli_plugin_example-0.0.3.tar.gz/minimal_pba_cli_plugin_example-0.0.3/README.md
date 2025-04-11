# Minimal command-line interface plugin for [minimal-pba-cli](https://github.com/easy-as-python/minimal-pba-cli)

This is a minimal example of a plugin that can be discovered, installed, and used in a command-line interface using a plugin-based architecture.

## Key moving parts

The main components of a working plugin are:

- The distribution name: Plugins must have a distribution name with a known prefix (in the case of this project, `minimal-pba-cli-plugin-`).
- `[project.entry-points.minimal_pba_cli]`: This section must exist in `pyproject.toml` and must contain one key-value pair,
  where the key is the "proper" name of the plugin (without the distribution name prefix)
  and the value is the dotted module path of the plugin's main entry point
- The plugin entry point: This module must contain either or both of `groups` and `commands`.
  Each of these is a dictionary whose keys are the name of the command or command group that the plugin will provide to the core CLI,
  and whose values are the [Typer](https://typer.tiangolo.com/) command group objects or command objects, respectively, to execute.
