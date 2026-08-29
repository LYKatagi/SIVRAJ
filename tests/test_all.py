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
from sivraj.core.orchestrator import Orchestrator
from sivraj.core.registry import CommandRegistry
from sivraj.core.recovery import RecoveryManager
from sivraj.core.router import CommandRouter
from sivraj.load.loader import CommandLoader
from sivraj.voice.voice import Voice, VoiceError


def print_header() -> None:
    print("╭────────────────────────────╮")
    print("│          S I V R A J       │")
    print("│      Integration Test      │")
    print("╰────────────────────────────╯")
    print()
    print("Pipeline:")
    print("Input → Ollama → Schema → Router → Registry → Command")
    print()
    print("Modos:")
    print("  [1] Terminal")
    print("  [2] Voice")
    print()
    print("Digite 'exit' no modo terminal para sair.")
    print()


def print_json(title: str, data: object) -> None:
    print(f"\n{title}")
    print(
        json.dumps(
            data,
            indent=4,
            ensure_ascii=False,
        )
    )


def create_orchestrator() -> Orchestrator:
    """Create the complete SIVRAJ pipeline."""

    registry = CommandRegistry()
    router = CommandRouter(registry)

    loader = CommandLoader(registry)
    loaded = loader.load()

    print(f"📦 Commands loaded: {loaded}")

    if loaded == 0:
        raise RuntimeError("Nenhum comando foi carregado.")

    print("📋 Registry:")

    for name in registry.list_commands():
        print(f"   ✓ {name}")

    print()

    ollama = OllamaClient()
    recovery = RecoveryManager()

    return Orchestrator(
        ollama=ollama,
        router=router,
        recovery=recovery,
    )


def run_terminal(orchestrator: Orchestrator) -> None:
    """Run SIVRAJ using terminal input."""

    print("⌨️ Modo Terminal")
    print()

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
            print("\n🤖 Processando...")

            result = orchestrator.process(prompt)

            print_json("📦 Resultado:", result)

            if result.get("executed"):
                print("\n🚦 Comando executado:")
                print(result.get("response"))

            else:
                print("\n💬 Conversa:")
                print(result.get("response"))

            print()

        except Exception as error:
            print(f"\n❌ TEST FAILED: {error}\n")


def run_voice(orchestrator: Orchestrator) -> None:
    """Run SIVRAJ using offline voice recognition."""

    print("🎙️ Modo Voice")
    print()
    print("Whisper será carregado localmente.")
    print("Pressione Ctrl+C para sair.")
    print()

    try:
        voice = Voice()

    except VoiceError as error:
        print(f"❌ Falha ao inicializar Voice: {error}")
        return

    while True:
        try:
            print("🎙️ Fale agora...")

            audio = voice.get_input()

            print("🧠 Processando áudio...")

            text = voice.parse(audio)

            print(f"📝 Você disse: {text}")

            print("\n🤖 SIVRAJ processando...")

            result = orchestrator.process(text)

            print_json("📦 Resultado:", result)

            if result.get("executed"):
                print("\n🚦 Comando executado:")
                print(result.get("response"))

            else:
                print("\n💬 Conversa:")
                print(result.get("response"))

            print()

        except VoiceError as error:
            print(f"\n⚠️ Voice: {error}\n")

        except KeyboardInterrupt:
            print("\n👋 SIVRAJ encerrado.")
            break

        except Exception as error:
            print(f"\n❌ TEST FAILED: {error}\n")


def main() -> None:
    print_header()

    try:
        orchestrator = create_orchestrator()

    except Exception as error:
        print(f"❌ Failed to initialize SIVRAJ: {error}")
        return

    try:
        mode = input("Escolha o modo [1/2]: ").strip()

    except (KeyboardInterrupt, EOFError):
        print("\n👋 SIVRAJ encerrado.")
        return

    print()

    if mode == "1":
        run_terminal(orchestrator)

    elif mode == "2":
        run_voice(orchestrator)

    else:
        print("❌ Modo inválido.")


if __name__ == "__main__":
    main()
