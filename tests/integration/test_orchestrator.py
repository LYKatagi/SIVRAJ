
from unittest.mock import Mock

import pytest

from sivraj.core.orchestrator import Orchestrator


class TestOrchestrator:

    def create_orchestrator(self, ollama_response, router_result=None):
        ollama = Mock()
        ollama.generate.return_value = ollama_response

        router = Mock()
        router.route.return_value = router_result

        return Orchestrator(
            ollama=ollama,
            router=router,
        ), ollama, router

    def test_conversation_response(self):
        response = {
            "cmd": "none",
            "response": "Olá! Como posso ajudar?",
            "show": None,
        }

        orchestrator, ollama, router = self.create_orchestrator(response)

        result = orchestrator.process("Olá")

        assert result == {
            "success": True,
            "command": None,
            "show": None,
            "message": "Olá! Como posso ajudar?",
        }

        ollama.generate.assert_called_once_with("Olá")
        router.route.assert_not_called()

    def test_command_is_sent_to_router(self):
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

        assert result == router_result

        ollama.generate.assert_called_once_with(
            "Mostre minha localização"
        )

        router.route.assert_called_once_with(response)

    def test_invalid_schema_response_is_rejected(self):
        response = {
            "cmd": "invalid_command",
            "response": "Resposta inválida",
            "show": None,
        }

        orchestrator, ollama, router = self.create_orchestrator(response)

        with pytest.raises(ValueError, match="invalid SIVRAJ response"):
            orchestrator.process("Teste")

        ollama.generate.assert_called_once_with("Teste")
        router.route.assert_not_called()

    def test_empty_prompt_is_rejected(self):
        orchestrator, ollama, router = self.create_orchestrator(
            {
                "cmd": "none",
                "response": "Resposta",
                "show": None,
            }
        )

        with pytest.raises(ValueError, match="Prompt cannot be empty"):
            orchestrator.process("")

        ollama.generate.assert_not_called()
        router.route.assert_not_called()

    def test_whitespace_prompt_is_rejected(self):
        orchestrator, ollama, router = self.create_orchestrator(
            {
                "cmd": "none",
                "response": "Resposta",
                "show": None,
            }
        )

        with pytest.raises(ValueError, match="Prompt cannot be empty"):
            orchestrator.process("   ")

        ollama.generate.assert_not_called()
        router.route.assert_not_called()

    def test_prompt_must_be_string(self):
        orchestrator, ollama, router = self.create_orchestrator(
            {
                "cmd": "none",
                "response": "Resposta",
                "show": None,
            }
        )

        with pytest.raises(TypeError, match="Prompt must be a string"):
            orchestrator.process(123)

        ollama.generate.assert_not_called()
        router.route.assert_not_called()

    def test_router_result_is_preserved(self):
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

        assert result is expected_result
        router.route.assert_called_once_with(response)

