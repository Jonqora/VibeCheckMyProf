import pytest
from shared.config import Config, TSuiteConfig


@pytest.fixture(scope="session")
def session_monkeypatch():
    """ Creates a pytest-session-scoped monkeypatch fixture. """
    from _pytest.monkeypatch import MonkeyPatch
    mp = MonkeyPatch()
    yield mp
    mp.undo()


@pytest.fixture(autouse=True, scope="session")
def replace_config(session_monkeypatch):
    """ Replaces configuration with test db name to
        prevent tests from altering production db. """
    test_config_path = "infra/config.env"

    def mock_config(cls):
        return TSuiteConfig.from_file(test_config_path)

    session_monkeypatch.setattr(Config, "from_env", mock_config)
