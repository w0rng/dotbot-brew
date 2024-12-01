# Dotbot-brew

This is a plugin for [dotbot](https://github.com/anishathalye/dotbot) that adds `brew`,
`cask`, `tap`, `brewfile`, and `app-store` directives. It allows installation of
packages using either `brew` or `brew --cask` and `mas`.

## Installation

Add it as submodule of your dotfiles repository (per the [dotbot plugin installation
guidelines](https://github.com/anishathalye/dotbot#plugins)).

```shell
git submodule add https://github.com/wren/dotbot-brew.git
```

Modify your `install` script, so it automatically enables `brew` plugin.

```shell
"${BASEDIR}/${DOTBOT_DIR}/${DOTBOT_BIN}" -d "${BASEDIR}" --plugin-dir dotbot-brew -c "${CONFIG}" "${@}"
```

## Usage

In your `install.conf.yaml` use `brew` directive to list all packages to be installed
using `brew`. The same works with `cask` and `brewfile`.

Also, if you plan on having multiple directives, you should consider using defaults to
set your preferred settings.

For example, your config might look something like:

```yaml
# Sets default config for certain directives
- defaults:
    - brewfile:
        - stdout: true
    - brew:
        - stderr: False
        - stdout: False

# Reads brewfile for packages to install
- brewfile:
    - Brewfile
    - brew/Brewfile

# Adds a tap
- tap:
    - caskroom/fonts

# Installs certain brew packages
- brew:
    - age
    - git
    - git-lfs
    - jrnl
    - neovim --HEAD
    - yq
    - zsh

# Installs certain casks
- cask:
    - signal
    - vlc
    - font-fira-code-nerd-font

# Install apps from the app store
- app-store:
    - 6720708363 # obsidian web clipper
    - 1458969831 # JSONPeep for safari
```

## Special Thanks

This project owes special thanks to
[d12frosted](https://github.com/d12frosted/dotbot-brew) and
[wren](https://github.com/wren/dotbot-brew) for their work in their own
versions of `dotbot-brew` (which this project was originally forked from).
