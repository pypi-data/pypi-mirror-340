import pytest
import yaml
from typer.testing import CliRunner

from meshadmin.cli.main import app

runner = CliRunner()


@pytest.fixture
def temp_config_dir(tmp_path):
    config_dir = tmp_path / "meshadmin"
    config_dir.mkdir()
    return config_dir


@pytest.fixture
def sample_context(temp_config_dir):
    contexts = {
        "test-context": {
            "endpoint": "http://localhost:8000",
            "interface": "nebula1",
            "active": True,
        }
    }
    contexts_file = temp_config_dir / "contexts.yaml"
    with open(contexts_file, "w") as f:
        yaml.dump(contexts, f)
    return contexts


def test_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "meshadmin version" in result.stdout


def test_context_list_no_contexts(temp_config_dir):
    result = runner.invoke(
        app, ["--config-path", str(temp_config_dir), "context", "list"]
    )
    assert result.exit_code == 0
    assert "No contexts found" in result.stdout


def test_context_create(temp_config_dir):
    result = runner.invoke(
        app,
        [
            "--config-path",
            str(temp_config_dir),
            "context",
            "create",
            "test-context",
            "--endpoint",
            "http://localhost:8000",
        ],
    )
    assert result.exit_code == 0
    assert "Created context 'test-context'" in result.stdout
    assert "Set 'test-context' as active context" in result.stdout


def test_context_switch(temp_config_dir, sample_context):
    result = runner.invoke(
        app,
        [
            "--config-path",
            str(temp_config_dir),
            "context",
            "create",
            "second-context",
            "--endpoint",
            "http://localhost:8001",
        ],
    )
    assert result.exit_code == 0
    result = runner.invoke(
        app, ["--config-path", str(temp_config_dir), "context", "use", "second-context"]
    )
    assert result.exit_code == 0
    assert "Switched to context 'second-context'" in result.stdout


def test_context_flag_override(temp_config_dir, sample_context):
    runner.invoke(
        app,
        [
            "--config-path",
            str(temp_config_dir),
            "context",
            "create",
            "second-context",
            "--endpoint",
            "http://localhost:8001",
        ],
    )
    result = runner.invoke(
        app,
        [
            "--config-path",
            str(temp_config_dir),
            "--context",
            "second-context",
            "host",
            "config",
            "info",
        ],
    )
    assert result.exit_code == 0
    assert "second-context" in result.stdout


def test_config_info(temp_config_dir, sample_context):
    result = runner.invoke(
        app, ["--config-path", str(temp_config_dir), "host", "config", "info"]
    )
    assert result.exit_code == 0
    assert "Configuration Paths:" in result.stdout
    assert "Contexts file:" in result.stdout
    assert "test-context" in result.stdout
    assert "http://localhost:8000" in result.stdout
    assert "nebula1" in result.stdout


def test_invalid_context(temp_config_dir, sample_context):
    result = runner.invoke(
        app,
        [
            "--config-path",
            str(temp_config_dir),
            "--context",
            "nonexistent",
            "host",
            "config",
            "info",
        ],
    )
    assert result.exit_code == 1
    assert "Context 'nonexistent' not found" in result.stdout


def test_env_var_config_path(temp_config_dir, sample_context, monkeypatch):
    monkeypatch.setenv("MESHADMIN_CONFIG_PATH", str(temp_config_dir))
    result = runner.invoke(app, ["host", "config", "info"])
    assert result.exit_code == 0
    assert "Configuration Paths:" in result.stdout
    assert "Contexts file:" in result.stdout
    assert "test-context" in result.stdout
    assert "http://localhost:8000" in result.stdout


def test_env_var_context(temp_config_dir, sample_context, monkeypatch):
    runner.invoke(
        app,
        [
            "--config-path",
            str(temp_config_dir),
            "context",
            "create",
            "second-context",
            "--endpoint",
            "http://localhost:8001",
        ],
    )
    monkeypatch.setenv("MESH_CONTEXT", "second-context")
    result = runner.invoke(
        app, ["--config-path", str(temp_config_dir), "host", "config", "info"]
    )
    assert result.exit_code == 0
    assert "second-context" in result.stdout
