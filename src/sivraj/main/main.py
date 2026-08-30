






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

            # ----------------------------------------------------------
            # Text input
            # ----------------------------------------------------------

            if user_input.prompt:
                if renderer.is_exit_command(
                    user_input.prompt
                ):
                    renderer.render_goodbye()
                    break

                renderer.thinking()

                result = orchestrator.process(
                    prompt=user_input.prompt,
                    voice=False,
                )

                renderer.processing()
                renderer.render(result)

                continue

            # ----------------------------------------------------------
            # Voice input
            # ----------------------------------------------------------

            if user_input.voice:
                renderer.listening()

                voice = orchestrator.voice

                voice.start_recording()

                try:
                    # F2 stops recording.
                    # ESC cancels recording.
                    while voice.recording:
                        key = renderer.console.input(
                            ""
                        )

                except KeyboardInterrupt:
                    voice.cancel_recording()
                    raise

                audio = voice.stop_recording()

                renderer.processing()

                text = voice.parse(audio)

                result = orchestrator.process(
                    prompt=text,
                    voice=False,
                )

                renderer.render(result)

        except KeyboardInterrupt:
            renderer.render_goodbye()
            break

        except Exception as error:
            renderer.render_error(error)


