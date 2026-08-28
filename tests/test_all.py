

from __future__ import annotations

import json
import sys
from pathlib import Path

# Allow running directly with:
# py tests/test_all.py
ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sivraj.ai.ollama import OllamaClient
from sivraj.core.registry import CommandRegistry
from sivraj.core.router import CommandRouter
from sivraj.load.loader import CommandLoader


def print_header() -> None:
    print("╭────────────────────────────╮")
    print("│          S I V R A J       │")
    print("│      Integration Test      │")
    print("╰────────────────────────────╯")
    print()
    print("Pipeline:")
    print("Input → Ollama → Schema → Router → Registry → Command")
    print("Digite 'exit' para sair.")
    print()


def main() -> None:
    print_header()

    # Core components
    registry = CommandRegistry()
    router = CommandRouter(registry)

    # Automatically load every command
    loader = CommandLoader(registry)
    loaded = loader.load()

    print(f"📦 Commands loaded: {loaded}")

    if loaded == 0:
        print("⚠️ Nenhum comando foi carregado.")
        return

    print("📋 Registry:")

    for name in registry._commands:
        print(f"   ✓ {name}")

    print()

    # Ollama client
    ollama = OllamaClient()

    while True:
        try:
            prompt = input("> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n")
            break

        if prompt.lower() == "exit":
            print("👋 SIVRAJ encerrado.")
            break

        if not prompt:
            continue

        try:
            print("\n🤖 Ollama...")

            data = ollama.generate(prompt)

            print("\n📦 JSON:")
            print(
                json.dumps(
                    data,
                    indent=4,
                    ensure_ascii=False,
                )
            )

            command_name = data["cmd"]

            if command_name == "none":
                print("\n💬 Conversa:")
                print(data["response"])
                print()
                continue

            print("\n🚦 Router...")

            result = router.route(data)

            print("\n✅ Resultado:")
            print(
                json.dumps(
                    result,
                    indent=4,
                    ensure_ascii=False,
                )
            )

            print()

        except Exception as error:
            print(f"\n❌ TEST FAILED: {error}\n")


if __name__ == "__main__":
    main()

