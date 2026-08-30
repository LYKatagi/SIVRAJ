

from __future__ import annotations

import urllib.parse
import webbrowser
from typing import Any

import requests

from sivraj.commands.base import Command


class MapsCommand(Command):
    """Comando responsável por mapas e localização."""

    name = "maps"

    def execute(self, query: str = "current_location", **kwargs: Any) -> dict[str, Any]:
        """Executa uma operação de mapas.

        Args:
            query: Localização a pesquisar ou ``current_location``.
            **kwargs: Argumentos adicionais ignorados pelo comando.

        Returns:
            Resultado da operação.
        """

        if query == "current_location":
            return self._current_location()

        return self._search_location(query)

    
    def _current_location(self) -> dict[str, Any]:
        """Obtém uma localização aproximada através do IP."""

        providers = (
            "https://ipapi.co/json/",
            "https://ipwho.is/",
        )

        last_error: str | None = None

        for provider in providers:
            try:
                response = requests.get(
                    provider,
                    timeout=5,
                    headers={
                        "User-Agent": "SIVRAJ/0.1",
                    },
                )

                response.raise_for_status()

                data = response.json()

                # ipwho.is informa explicitamente se a consulta falhou.
                if data.get("success") is False:
                    last_error = data.get(
                        "response",
                        "Location provider failed",
                    )
                    continue

                latitude = data.get("latitude")
                longitude = data.get("longitude")

                if latitude is None or longitude is None:
                    last_error = "Latitude/longitude não encontradas."
                    continue

                url = (
                    "https://www.openstreetmap.org/"
                    f"?mlat={latitude}&mlon={longitude}"
                    f"#map=15/{latitude}/{longitude}"
                )

                webbrowser.open(url)

                city = data.get("city")
                region = data.get("region")

                location = ", ".join(
                    value
                    for value in (city, region)
                    if value
                )

                return {
                    "success": True,
                    "command": self.name,
                    "show": "location",
                    "latitude": latitude,
                    "longitude": longitude,
                    "location": location,
                    "url": url,
                    "response": (
                        f"Localização aproximada: {location}"
                        if location
                        else "Mapa aberto com sua localização aproximada."
                    ),
                }

            except requests.RequestException as exc:
                last_error = str(exc)

        return {
            "success": False,
            "command": self.name,
            "show": "location",
            "response": "Não foi possível obter sua localização.",
            "error": last_error,
        }


    def _search_location(self, query: str) -> dict[str, Any]:
        """Abre uma pesquisa no OpenStreetMap."""

        encoded_query = urllib.parse.quote_plus(query)

        url = (
            "https://www.openstreetmap.org/"
            f"search?query={encoded_query}"
        )

        webbrowser.open(url)

        return {
            "success": True,
            "command": self.name,
            "show": "location",
            "query": query,
            "url": url,
            "response": f"Abrindo o mapa para {query}.",
        }

