
"""
SIVRAJ - Global Test Suite

Smoke/integration tests covering the main SIVRAJ architecture.

Pipeline:

    Ollama
       ↓
    Schema
       ↓
    Orchestrator
       ↓
    Router
       ↓
    Registry
       ↓
    Command
"""

from unittest.mock import Mock

import pytest

from sivraj.ai.schema import Schema
from sivraj.core.config import SCHEMA
from sivraj.core.orchestrator import Orchestrator
from sivraj.core.registry import CommandRegistry
from sivraj.core.router import CommandRouter
from sivraj.voice.voice import Voice

# ============================================================
# Fixtures
# ============================================================


@pytest.fixture
def registry() -> CommandRegistry:
    """Create a clean command registry."""
    return CommandRegistry()


@pytest.fixture
def router(registry: CommandRegistry) -> CommandRouter:
    """Create a router using the test registry."""
    return CommandRouter(registry)
@pytest.fixture
def voice() -> Voice:
    return Voice()

@pytest.fixture
def recovery() -> Mock:
    """Create a mock recovery service."""
    recovery = Mock()

    def run(callback, name=None):
        return callback()

    recovery.run.side_effect = run

    return recovery


def create_orchestrator(
    response: dict,
    router: CommandRouter,
    recovery: Mock,
    voice: Voice
) -> Orchestrator:
    """Create an Orchestrator with mocked external dependencies."""

    ollama = Mock()
    ollama.generate.return_value = response

    return Orchestrator(
        ollama=ollama,
        router=router,
        recovery=recovery,
        voice=voice
    )


# ============================================================
# Import / Configuration
# ============================================================


class TestProjectConfiguration:
    """Tests for the project's basic configuration."""

    def test_schema_exists(self) -> None:
        """The global schema must be available."""

        assert isinstance(SCHEMA, dict)
        assert SCHEMA["type"] == "object"

    def test_schema_has_required_fields(self) -> None:
        """The SIVRAJ response contract must define all core fields."""

        required = SCHEMA["required"]

        assert "cmd" in required
        assert "args" in required
        assert "response" in required
        assert "show" in required

    def test_schema_has_core_commands(self) -> None:
        """Core SIVRAJ commands must be defined by the schema."""

        commands = SCHEMA["properties"]["cmd"]["enum"]

        assert "maps" in commands
        assert "open_app" in commands
        assert "system" in commands
        assert "none" in commands


# ============================================================
# Schema
# ============================================================


class TestGlobalSchema:
    """Global validation tests."""

    @staticmethod
    def valid_response(
        cmd: str = "none",
        args: dict | None = None,
        response: str = "OK",
        show: str | None = None,
    ) -> dict:
        """Build a valid SIVRAJ response."""

        return {
            "cmd": cmd,
            "args": {} if args is None else args,
            "response": response,
            "show": show,
        }

    def test_valid_none_response(self) -> None:
        """A normal conversation response must be valid."""

        data = self.valid_response(
            cmd="none",
            response="Olá!",
        )

        assert Schema.validate_data(data) is True

    def test_valid_maps_response(self) -> None:
        """A maps command must expose the location view."""

        data = self.valid_response(
            cmd="maps",
            response="Mostrando sua localização.",
            show="location",
        )

        assert Schema.validate_data(data) is True

    def test_valid_open_app_response(self) -> None:
        """An open_app command must allow a null show value."""

        data = self.valid_response(
            cmd="open_app",
            args={"app": "code"},
            response="Abrindo o VS Code.",
            show=None,
        )

        assert Schema.validate_data(data) is True

    def test_valid_system_response(self) -> None:
        """A system command must allow arguments."""

        data = self.valid_response(
            cmd="system",
            args={"action": "status"},
            response="Verificando o sistema.",
            show=None,
        )

        assert Schema.validate_data(data) is True

    def test_maps_requires_location(self) -> None:
        """Maps commands must use the location display."""

        data = self.valid_response(
            cmd="maps",
            response="Localização.",
            show=None,
        )

        assert Schema.validate_data(data) is False

    def test_non_maps_commands_cannot_show_location(self) -> None:
        """Non-map commands must not request the location display."""

        for command in ("open_app", "system", "none"):
            data = self.valid_response(
                cmd=command,
                response="OK",
                show="location",
            )

            assert Schema.validate_data(data) is False

    def test_invalid_command_is_rejected(self) -> None:
        """Unknown commands must be rejected."""

        data = self.valid_response(
            cmd="banana",
        )

        assert Schema.validate_data(data) is False

    def test_missing_args_is_rejected(self) -> None:
        """The args field is mandatory."""

        data = {
            "cmd": "none",
            "response": "Olá!",
            "show": None,
        }

        assert Schema.validate_data(data) is False

    def test_missing_response_is_rejected(self) -> None:
        """The response field is mandatory."""

        data = {
            "cmd": "none",
            "args": {},
            "show": None,
        }

        assert Schema.validate_data(data) is False

    def test_missing_show_is_rejected(self) -> None:
        """The show field is mandatory."""

        data = {
            "cmd": "none",
            "args": {},
            "response": "Olá!",
        }

        assert Schema.validate_data(data) is False

    def test_extra_properties_are_rejected(self) -> None:
        """Unknown top-level properties must not be accepted."""

        data = self.valid_response()

        data["unexpected"] = True

        assert Schema.validate_data(data) is False

    def test_response_must_be_string(self) -> None:
        """The response must always be text."""

        data = self.valid_response()

        data["response"] = 123

        assert Schema.validate_data(data) is False

    def test_args_must_be_object(self) -> None:
        """Command arguments must be represented by an object."""

        data = self.valid_response()

        data["args"] = "invalid"

        assert Schema.validate_data(data) is False


# ============================================================
# Registry
# ============================================================


class TestGlobalRegistry:
    """Global CommandRegistry tests."""

    def test_register_command(self, registry: CommandRegistry) -> None:
        """Commands can be registered."""

        command = Mock()

        registry.register("test", command)

        assert registry.exists("test")
        assert registry.get("test") is command

    def test_get_unknown_command(
        self,
        registry: CommandRegistry,
    ) -> None:
        """Unknown commands return None."""

        assert registry.get("unknown") is None

    def test_duplicate_command_is_rejected(
        self,
        registry: CommandRegistry,
    ) -> None:
        """The same command cannot be registered twice."""

        command = Mock()

        registry.register("test", command)

        with pytest.raises(ValueError):
            registry.register("test", command)

    def test_empty_command_name_is_rejected(
        self,
        registry: CommandRegistry,
    ) -> None:
        """Commands require a name."""

        with pytest.raises(ValueError):
            registry.register("", Mock())

    def test_list_commands(
        self,
        registry: CommandRegistry,
    ) -> None:
        """Registered commands appear in list_commands."""

        registry.register("first", Mock())
        registry.register("second", Mock())

        assert registry.list_commands() == [
            "first",
            "second",
        ]

    def test_unregister_command(
        self,
        registry: CommandRegistry,
    ) -> None:
        """Commands can be removed."""

        registry.register("test", Mock())

        registry.unregister("test")

        assert registry.exists("test") is False

    def test_clear_registry(
        self,
        registry: CommandRegistry,
    ) -> None:
        """The registry can be completely cleared."""

        registry.register("first", Mock())
        registry.register("second", Mock())

        registry.clear()

        assert registry.list_commands() == []


# ============================================================
# Router
# ============================================================


class TestGlobalRouter:
    """Global CommandRouter tests."""

    def test_router_executes_command(
        self,
        registry: CommandRegistry,
        router: CommandRouter,
    ) -> None:
        """The router must execute the registered command."""

        command = Mock()
        command.execute.return_value = {
            "success": True,
            "command": "test",
        }

        registry.register("test", command)

        result = router.route(
            {
                "cmd": "test",
                "args": {},
            }
        )

        assert result["success"] is True
        command.execute.assert_called_once_with()

    def test_router_passes_arguments(
        self,
        registry: CommandRegistry,
        router: CommandRouter,
    ) -> None:
        """The router must forward args to the command."""

        command = Mock()
        command.execute.return_value = {
            "success": True,
            "command": "test",
        }

        registry.register("test", command)

        router.route(
            {
                "cmd": "test",
                "args": {
                    "name": "Luiz",
                    "value": 42,
                },
            }
        )

        command.execute.assert_called_once_with(
            name="Luiz",
            value=42,
        )

    def test_router_does_not_pass_show(
        self,
        registry: CommandRegistry,
        router: CommandRouter,
    ) -> None:
        """The show field must remain independent from command args."""

        command = Mock()
        command.execute.return_value = {
            "success": True,
            "command": "maps",
            "show": "location",
        }

        registry.register("maps", command)

        router.route(
            {
                "cmd": "maps",
                "args": {
                    "query": "current location",
                },
                "response": "Localização.",
                "show": "location",
            }
        )

        command.execute.assert_called_once_with(
            query="current location",
        )

    def test_unknown_command_is_rejected(
        self,
        router: CommandRouter,
    ) -> None:
        """The router must reject unknown commands."""

        with pytest.raises(ValueError, match="Unknown command"):
            router.route(
                {
                    "cmd": "unknown",
                    "args": {},
                }
            )

    def test_missing_command_is_rejected(
        self,
        router: CommandRouter,
    ) -> None:
        """Routing data without cmd must fail."""

        with pytest.raises(
            ValueError,
            match="must contain 'cmd'",
        ):
            router.route(
                {
                    "args": {},
                }
            )

    def test_invalid_args_are_rejected(
        self,
        registry: CommandRegistry,
        router: CommandRouter,
    ) -> None:
        """args must be a dictionary."""

        registry.register("test", Mock())

        with pytest.raises(
            ValueError,
            match="args.*object",
        ):
            router.route(
                {
                    "cmd": "test",
                    "args": "invalid",
                }
            )


# ============================================================
# Orchestrator
# ============================================================


class TestGlobalOrchestrator:
    """End-to-end Orchestrator tests."""

    def test_conversation_pipeline(
        self,
        router: CommandRouter,
        recovery: Mock,
        voice: Voice
    ) -> None:
        """Normal conversation must not execute a command."""

        response = {
            "cmd": "none",
            "args": {},
            "response": "Olá! Como posso ajudar?",
            "show": None,
        }

        orchestrator = create_orchestrator(
            response,
            router,
            recovery,
            voice
        )

        result = orchestrator.process("Olá", voice=False)

        assert result["success"] is True
        assert result["command"] == "none"
        assert result["response"] == "Olá! Como posso ajudar?"
        assert result["show"] is None

    def test_maps_pipeline(
        self,
        registry: CommandRegistry,
        router: CommandRouter,
        recovery: Mock,
        voice: Voice,
    ) -> None:
        """A maps command must travel through the complete pipeline."""

        command = Mock()
        command.execute.return_value = {
            "success": True,
            "command": "maps",
            "message": "Solicitação de localização recebida.",
        }

        registry.register("maps", command)

        response = {
            "cmd": "maps",
            "args": {},
            "response": "Mostrando sua localização.",
            "show": "location",
        }

        orchestrator = create_orchestrator(
            response,
            router,
            recovery,
            voice
        )

        result = orchestrator.process(
            "Mostre minha localização", voice=False
        )

        assert result["success"] is True
        assert result["command"] == "maps"

        command.execute.assert_called_once_with()

    def test_arguments_reach_command(
        self,
        registry: CommandRegistry,
        router: CommandRouter,
        recovery: Mock,
        voice: Voice
    ) -> None:
        """Arguments must travel from Ollama to the command."""

        command = Mock()
        command.execute.return_value = {
            "success": True,
            "command": "system",
        }

        registry.register("system", command)

        response = {
            "cmd": "system",
            "args": {
                "action": "status",
                "verbose": True,
            },
            "response": "Verificando o sistema.",
            "show": None,
        }

        orchestrator = create_orchestrator(
            response,
            router,
            recovery,
            voice
        )

        orchestrator.process("Verifique o sistema", voice=False)

        command.execute.assert_called_once_with(
            action="status",
            verbose=True,
        )

    def test_invalid_response_is_rejected(
        self,
        router: CommandRouter,
        recovery: Mock,
        voice: Voice
    ) -> None:
        """Invalid Ollama responses must never reach the router."""

        response = {
            "cmd": "invalid",
            "args": {},
            "response": "Resposta inválida.",
            "show": None,
        }

        orchestrator = create_orchestrator(
            response,
            router,
            recovery,
            voice
        )

        with pytest.raises(
            ValueError,
            match="invalid SIVRAJ response",
        ):
            orchestrator.process("teste", voice=False)

    def test_non_dict_response_is_rejected(
        self,
        router: CommandRouter,
        recovery: Mock,
        voice: Voice,
    ) -> None:
        """Ollama must return an object."""

        orchestrator = create_orchestrator(
            "invalid",
            router,
            recovery,
            voice
        )

        with pytest.raises(
            ValueError,
            match="invalid SIVRAJ response",
        ):
            orchestrator.process("teste", voice=False)

    def test_original_prompt_reaches_ollama(
        self,
        router: CommandRouter,
        recovery: Mock,
        voice: Voice
    ) -> None:
        """The original user prompt must be passed to Ollama."""

        response = {
            "cmd": "none",
            "args": {},
            "response": "Tudo certo!",
            "show": None,
        }

        orchestrator = create_orchestrator(
            response,
            router,
            recovery,
            voice
        )

        prompt = "Como você está?"

        orchestrator.process(prompt, voice=False)

        orchestrator.ollama.generate.assert_called_once_with(prompt)

    def test_conversation_does_not_call_router(
        self,
        router: CommandRouter,
        recovery: Mock,
        voice: Voice
    ) -> None:
        """cmd=none must bypass the router."""

        router.route = Mock()

        response = {
            "cmd": "none",
            "args": {},
            "response": "Olá!",
            "show": None,
        }

        orchestrator = create_orchestrator(
            response,
            router,
            recovery,
            voice
        )

        orchestrator.process("Oi", voice=False)

        router.route.assert_not_called()

    def test_router_result_is_preserved(
        self,
        registry: CommandRegistry,
        router: CommandRouter,
        recovery: Mock,
        voice: Voice
    ) -> None:
        """The Orchestrator must preserve the command result."""

        command = Mock()
        expected = {
            "success": True,
            "command": "maps",
            "message": "Solicitação de localização recebida.",
            "extra": "value",
        }

        command.execute.return_value = expected

        registry.register("maps", command)

        response = {
            "cmd": "maps",
            "args": {},
            "response": "Localização.",
            "show": "location",
        }

        orchestrator = create_orchestrator(
            response,
            router,
            recovery,
            voice
        )

        result = orchestrator.process("Onde estou?", voice=False)

        assert result == expected

