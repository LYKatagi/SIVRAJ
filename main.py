
import json

from sivraj.ai.ollama import OllamaClient


def main() -> None:
    client = OllamaClient()

    print("╭────────────────────────────╮")
    print("│          S I V R A J       │")
    print("│       Terminal Mode        │")
    print("╰────────────────────────────╯")
    print()
    print("Digite 'exit' para sair.")
    print()

    while True:
        try:
            prompt = input("> ").strip()

            if not prompt:
                continue

            if prompt.lower() in {"exit", "quit"}:
                break

            print("\n🤖 Processando...\n")

            result = client.generate(prompt)

            print(json.dumps(
                result,
                indent=4,
                ensure_ascii=False,
            ))

            print()

        except KeyboardInterrupt:
            print("\n\nSIVRAJ encerrado.")
            break

        except Exception as error:
            print(f"\n❌ Erro: {error}\n")


if __name__ == "__main__":
    main()

