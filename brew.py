import os, subprocess, dotbot, sys
from typing import Iterable, Mapping, Any

Context = Mapping[str, Any]


class Brew(dotbot.Plugin):
    default_context = {
        "brew": {
            "stdin": False,
            "stderr": False,
            "stdout": False,
            "force_intel": False,
        },
        "cask": {
            "stdin": False,
            "stderr": False,
            "stdout": False,
            "force_intel": False,
        },
        "brewfile": {
            "stdin": True,
            "stderr": True,
            "stdout": True,
            "force_intel": False,
        },
    }

    def __init__(self, *args, **kwargs):
        self.directives = {
            "brew": self._brew,
            "cask": self._cask,
            "tap": self._tap,
            "brewfile": self._brew_file,
            "app-store": self._mas,
        }

        super().__init__(*args, **kwargs)

    def can_handle(self, directive):
        return directive in self.directives

    def handle(self, directive: str, data: Iterable[str]) -> bool:
        user_context = self._context.defaults().get(directive, {})
        local_context = self.default_context.get(directive, {})
        context = {**local_context, **user_context}

        return self.directives[directive](data, context)

    def _tap(self, tap_list: Iterable[str], context: Context) -> bool:
        if not self._brew_exist(context):
            if not self._install_brew(context):
                self._log.error("Failed to install brew")
                return False

        result = True

        for tap in tap_list:
            self._log.info(f"Tapping {tap}")
            cmd_result = self._invoke_shell_command(f"brew tap {tap}", context)
            if cmd_result != 0:
                self._log.warning(f"Failed to tap [{tap}]")
                result = False

        return result

    def _brew(self, packages_list: Iterable[str], context: Context):
        if not self._brew_exist(context):
            if not self._install_brew(context):
                self._log.error("Failed to install brew")
                return False

        result = True

        for pkg in packages_list:
            self._log.info(f"Install {pkg}")
            success = self._invoke_shell_command(f"brew install {pkg}", context)

            if not success:
                self._log.warning(f"Failed to install [{pkg}]")
                result = False

        return result

    def _brew_file(self, brew_files: Iterable[str], context: Context):
        if not self._brew_exist(context):
            if not self._install_brew(context):
                self._log.error("Failed to install brew")
                return False

        result = True

        for file in brew_files:
            self._log.info(f"Installing from file {file}")
            success = self._invoke_shell_command(f"brew bundle --verbose --file={file}", context)

            if not success:
                self._log.warning(f"Failed to install file [{file}]")
                result = False

        return result

    def _cask(self, packages: Iterable[str], context: Context) -> bool:
        if not self._brew_exist(context):
            if not self._install_brew(context):
                self._log.error("Failed to install brew")
                return False

        result = True

        for pkg in packages:
            self._log.info(f"Install cask {pkg}")
            success = self._invoke_shell_command(
                f"brew install --cask {pkg} || brew ls --cask --versions {pkg}",
                context,
            )
            if not success:
                self._log.warning(f"Failed to install cask [{pkg}]")
                result = False

        return result

    def _mas(self, apps: Iterable[str], context: Context):
        if not self._mas_exist(context):
            if not self._install_mas(context):
                self._log.error("Failed to install mas")
                return False

        result = True

        for app in apps:
            self._log.info(f"Install app {app} for appStore")
            success = self._invoke_shell_command(f"mas install {app}", context)

            if success != 0:
                self._log.warning(f"Failed to install app [{app}]")
                result = False

        return result

    def _brew_exist(self, context: Context) -> bool:
        return self._invoke_shell_command("hash brew", context) == 0

    def _mas_exist(self, context: Context) -> bool:
        return self._invoke_shell_command("hash mas", context) == 0

    def _install_brew(self, context: Context) -> bool:
        link = "https://raw.githubusercontent.com/Homebrew/install/master/install.sh"
        cmd = """hash brew || /bin/bash -c "$(curl -fsSL {0})";
              brew update""".format(link)

        return self._invoke_shell_command(cmd, context)

    def _install_mas(self, context: Context) -> bool:
        return self._brew(["mas"], context)

    def _invoke_shell_command(self, cmd: str, context: Context) -> bool:
        with open(os.devnull, "w") as devnull:
            if context["force_intel"]:
                cmd = "arch --x86_64 " + cmd

            return subprocess.call(
                cmd,
                shell=True,
                cwd=self._context.base_directory(),
                stdin=devnull if context["stdin"] else None,
                stdout=devnull if context["stdout"] else None,
                stderr=devnull if context["stderr"] else None,
            ) == 0
