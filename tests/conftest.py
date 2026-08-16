import json
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def temp_data_file(tmp_path, monkeypatch):
    data_file = tmp_path / "inventory.json"
    data_file.write_text(json.dumps({"items": []}))

    from src.models import inventory as inventory_model

    monkeypatch.setattr(inventory_model, "DATA_FILE", str(data_file))
    return data_file


@pytest.fixture
def app(temp_data_file):
    from src.app import create_app

    application = create_app()
    application.config.update({"TESTING": True})
    return application


@pytest.fixture
def client(app):
    return app.test_client()
