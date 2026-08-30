





"""SIVRAJ application."""

from sivraj.ai.ollama import OllamaClient
from sivraj.core.orchestrator import Orchestrator
from sivraj.core.recovery import RecoveryManager
from sivraj.core.registry import CommandRegistry
from sivraj.core.router import CommandRouter
from sivraj.load.loader import CommandLoader
from sivraj.ui.terminal import Renderer
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
    renderer = Renderer(rich=True)

    renderer.start()

    while True:
        try:
            user_input = renderer.input()

            if user_input.prompt:
                if user_input.prompt.lower() in {"exit", "quit"}:
                    renderer.render_goodbye()
                    break

                renderer.thinking()

                result = orchestrator.process(
                    prompt=user_input.prompt,
                    voice=False,
                )

            elif user_input.voice:
                renderer.listening()

                result = orchestrator.process(
                    prompt=None,
                    voice=True,
                )

            else:
                continue

            renderer.processing()
            renderer.render(result)

        except KeyboardInterrupt:
            renderer.render_goodbye()
            break

        except Exception as error:
            renderer.render_error(error)


if __name__ == "__main__":
    main()

