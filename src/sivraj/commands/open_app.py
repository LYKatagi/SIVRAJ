
from typing import Any
import os
import shutil
import subprocess

from .base import Command


class OpenAppCommand(Command):
    """Command responsible for opening allowed applications."""

    name = "open_app"

    # Applications explicitly allowed by SIVRAJ.
    APPS: dict[str, str] = {
        "vscode": "code",
        "code": "code",
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "explorer": "explorer.exe",
    }

    def execute(self, **kwargs: Any) -> dict[str, Any]:
        app = kwargs.get("app")

        if not isinstance(app, str) or not app.strip():
            return {
                "success": False,
                "response": "Nenhum aplicativo foi especificado.",
            }

        app = app.strip().lower()
        executable = self.APPS.get(app)

        if executable is None:
            return {
                "success": False,
                "response": f"O aplicativo '{app}' não está disponível.",
            }

        try:
            if shutil.which(executable) or os.path.isabs(executable):
                subprocess.Popen(
                    [executable],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            else:
                return {
                    "success": False,
                    "response": f"O aplicativo '{app}' não foi encontrado no sistema.",
                }

        except OSError as exc:
            return {
                "success": False,
                "response": f"Não foi possível abrir '{app}': {exc}",
            }

        return {
            "success": True,
            "response": f"Abrindo {app}...",
        }

