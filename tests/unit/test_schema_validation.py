import pytest

from sivraj.ai.schema import Schema


class TestSchemaValidation:
    def test_valid_maps_command(self):
        data = {
            "cmd": "maps",
            "response": "Aqui está sua localização.",
            "show": "location",
        }

        assert Schema.validate_data(data) is True

    def test_valid_open_app_command(self):
        data = {
            "cmd": "open_app",
            "response": "Abrindo o VS Code.",
            "show": None,
        }

        assert Schema.validate_data(data) is True

    def test_missing_cmd(self):
        data = {
            "response": "Aqui está sua localização.",
            "show": "location",
        }

        assert Schema.validate_data(data) is False

    def test_missing_response(self):
        data = {
            "cmd": "maps",
            "show": "location",
        }

        assert Schema.validate_data(data) is False

    def test_missing_show(self):
        data = {
            "cmd": "maps",
            "response": "Aqui está sua localização.",
        }

        assert Schema.validate_data(data) is False

    def test_invalid_command(self):
        data = {
            "cmd": "unknown_command",
            "response": "Comando desconhecido.",
            "show": None,
        }

        assert Schema.validate_data(data) is False

    def test_invalid_cmd_type(self):
        data = {
            "cmd": 123,
            "response": "Resposta.",
            "show": None,
        }

        assert Schema.validate_data(data) is False

    def test_invalid_response_type(self):
        data = {
            "cmd": "maps",
            "response": 123,
            "show": "location",
        }

        assert Schema.validate_data(data) is False

    def test_invalid_show_value(self):
        data = {
            "cmd": "maps",
            "response": "Aqui está sua localização.",
            "show": "banana",
        }

        assert Schema.validate_data(data) is False

    def test_show_can_be_null(self):
        data = {
            "cmd": "system",
            "response": "Tudo certo.",
            "show": None,
        }

        assert Schema.validate_data(data) is True

    def test_additional_properties_are_rejected(self):
        data = {
            "cmd": "maps",
            "response": "Aqui está sua localização.",
            "show": "location",
            "malicious_field": "unexpected value",
        }

        assert Schema.validate_data(data) is False

    @pytest.mark.parametrize(
        "data",
        [
            None,
            [],
            "string",
            123,
            True,
        ],
    )
    def test_non_object_data_is_rejected(self, data):
        assert Schema.validate_data(data) is False
