
import json

from sivraj.ai.ollama import OllamaClient
from sivraj.core.registry import CommandRegistry
from sivraj.core.router import CommandRouter


def maps_command(data: dict) -> dict:
    return {
        "executed": True,
        "command": "maps",
        "show": data["show"],
    }


def open_app_command(data: dict) -> dict:
    return {
        "executed": True,
        "command": "open_app",
    }


def system_command(data: dict) -> dict:
    return {
        "executed": True,
        "command": "system",
    }


def main() -> None:
    registry = CommandRegistry()

    registry.register("maps", maps_command)
    registry.register("open_app", open_app_command)
    registry.register("system", system_command)

    router = CommandRouter(registry)
    ollama = OllamaClient()

    print("╭────────────────────────────╮")
    print("│          S I V R A J       │")
    print("│      Integration Test      │")
    print("╰────────────────────────────╯")
    print()
    print("Pipeline: Ollama → Schema → Router → Registry")
    print("Digite 'exit' para sair.")
    print()

    while True:
        try:
            prompt = input("> ").strip()

            if not prompt:
                continue

            if prompt.lower() in {"exit", "quit"}:
                break

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

            if data["cmd"] == "none":
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

        except KeyboardInterrupt:
            print("\n\nSIVRAJ encerrado.")
            break

        except Exception as error:
            print(f"\n❌ TEST FAILED: {error}\n")


if __name__ == "__main__":
    main()

