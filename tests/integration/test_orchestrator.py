
from __future__ import annotations

from unittest.mock import Mock

import pytest

from sivraj.ai.schema import Schema
from sivraj.core.orchestrator import Orchestrator
from sivraj.core.recovery import RecoveryManager


class TestOrchestrator:
    def create_orchestrator(
        self,
        ollama_response: dict,
        router_result=None,
    ):
        ollama = Mock()
        ollama.generate.return_value = ollama_response

        router = Mock()

        if router_result is not None:
            router.route.return_value = router_result

        recovery = RecoveryManager(
            max_retries=0,
            retry_delay=0,
        )

        orchestrator = Orchestrator(
            ollama=ollama,
            router=router,
            recovery=recovery,
        )

        return orchestrator, ollama, router

    def test_conversation_response(self):
        """Conversation responses must not execute a command."""

        response = {
            "cmd": "none",
            "response": "Olá! Como posso ajudar?",
            "show": None,
        }

        orchestrator, ollama, router = self.create_orchestrator(response)

        result = orchestrator.process("Olá")

        assert result == {
            "success": True,
            "executed": False,
            "response": "Olá! Como posso ajudar?",
            "show": None,
        }

        ollama.generate.assert_called_once_with("Olá")
        router.route.assert_not_called()

    def test_command_is_sent_to_router(self):
        """Valid commands must be sent to the router."""

        response = {
            "cmd": "maps",
            "response": "Mostrando sua localização",
            "show": "location",
        }

        router_result = {
            "success": True,
            "command": "maps",
            "show": "location",
            "message": "Solicitação de localização recebida.",
        }

        orchestrator, ollama, router = self.create_orchestrator(
            response,
            router_result,
        )

        result = orchestrator.process("Mostre minha localização")

        assert result == {
            "success": True,
            "executed": True,
            "response": "Mostrando sua localização",
            "result": router_result,
            "show": "location",
        }

        ollama.generate.assert_called_once_with(
            "Mostre minha localização"
        )

        router.route.assert_called_once_with(response)

    def test_invalid_ollama_response_is_rejected(self):
        """Invalid Ollama data must be rejected by the Schema."""

        response = {
            "cmd": "invalid",
            "response": "Resposta inválida",
            "show": None,
        }

        orchestrator, _, router = self.create_orchestrator(response)

        with pytest.raises(
            ValueError,
            match="Ollama returned an invalid SIVRAJ response",
        ):
            orchestrator.process("Teste")

        router.route.assert_not_called()

    def test_router_result_is_preserved(self):
        """The router result must be preserved inside the orchestrator result."""

        response = {
            "cmd": "maps",
            "response": "Localização",
            "show": "location",
        }

        expected_result = {
            "success": True,
            "command": "maps",
            "show": "location",
            "message": "Solicitação de localização recebida.",
            "extra": "test",
        }

        orchestrator, _, router = self.create_orchestrator(
            response,
            expected_result,
        )

        result = orchestrator.process("Onde estou?")

        assert result["success"] is True
        assert result["executed"] is True
        assert result["response"] == "Localização"
        assert result["show"] == "location"

        # The exact object returned by the router is preserved.
        assert result["result"] is expected_result

    def test_conversation_does_not_call_router(self):
        """Conversation responses must bypass the router."""

        response = {
            "cmd": "none",
            "response": "Tudo certo!",
            "show": None,
        }

        orchestrator, _, router = self.create_orchestrator(response)

        orchestrator.process("Oi")

        router.route.assert_not_called()

    def test_ollama_is_called_with_original_prompt(self):
        """The original user prompt must be passed to Ollama."""

        response = {
            "cmd": "none",
            "response": "Olá!",
            "show": None,
        }

        orchestrator, ollama, _ = self.create_orchestrator(response)

        prompt = "Como você está?"

        orchestrator.process(prompt)

        ollama.generate.assert_called_once_with(prompt)

    def test_schema_validation_happens_before_routing(self):
        """Schema validation must happen before a command reaches the router."""

        response = {
            "cmd": "invalid",
            "response": "Resposta inválida",
            "show": None,
        }

        orchestrator, _, router = self.create_orchestrator(response)

        with pytest.raises(ValueError):
            orchestrator.process("Teste")

        router.route.assert_not_called()

