



"""SIVRAJ application"""

from sivraj.ai.ollama import OllamaClient
from sivraj.core.orchestrator import Orchestrator
from sivraj.core.recovery import RecoveryManager
from sivraj.core.registry import CommandRegistry
from sivraj.core.router import CommandRouter
from sivraj.load.loader import CommandLoader
from sivraj.voice.voice import Voice


def create_orchestrator() -> Orchestrator:
    """Build and configure the SIVRAJ orchestrator."""

    registry = CommandRegistry()

    loader = CommandLoader(registry)
    loader.load()

    router = CommandRouter(registry)

    return Orchestrator(
        ollama=OllamaClient(),
        router=router,
        recovery=RecoveryManager(),
        voice=Voice(),
    )


def main() -> None:
    """Start SIVRAJ."""

    orchestrator = create_orchestrator()

    print("SIVRAJ")
    print("Digite 'exit' para sair.\n")

    while True:
        try:
            prompt = input("Você: ").strip()

            if prompt.lower() in {"exit", "quit"}:
                print("SIVRAJ: Até mais!")
                break

            if not prompt:
                continue

            result = orchestrator.process(
                prompt=prompt,
                voice=False,
            )

            print(f"SIVRAJ: {result['response']}")

        except KeyboardInterrupt:
            print("\nSIVRAJ: Até mais!")
            break

        except Exception as error:
            print(f"SIVRAJ: Erro: {error}")



