







"""SIVRAJ application."""

from sivraj.ai.ollama import OllamaClient
from sivraj.core.orchestrator import Orchestrator
from sivraj.core.recovery import RecoveryManager
from sivraj.core.registry import CommandRegistry
from sivraj.core.router import CommandRouter
from sivraj.load.loader import CommandLoader
from sivraj.ui.terminal.renderer import Renderer
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
            prompt = renderer.input()

            if prompt.lower() in {"exit", "quit"}:
                renderer.render_goodbye()
                break

            if not prompt:
                continue

            renderer.thinking()
            renderer.processing()

            result = orchestrator.process(
                prompt=prompt,
                voice=False,
            )

            renderer.render(result)

        except KeyboardInterrupt:
            renderer.render_goodbye()
            break

        except Exception as error:
            renderer.render_error(error)


if __name__ == "__main__":
    main()

