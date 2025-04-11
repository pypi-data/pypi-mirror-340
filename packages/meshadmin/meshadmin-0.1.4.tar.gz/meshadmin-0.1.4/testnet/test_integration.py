import json
import subprocess
import time
from pathlib import Path

import pytest


def run_docker_compose(command, project_dir, env=None, check=False, text=True):
    return subprocess.run(
        ["docker", "compose"] + command,
        cwd=project_dir,
        env=env,
        capture_output=True,
        text=text,
        check=check,
    )


@pytest.fixture(scope="session")
def mesh_admin():
    return "https://dmeshadmin.hydo.ch"


@pytest.fixture(scope="session", autouse=True)
def build_test_image():
    run_docker_compose(
        ["build", "-t", "meshadmin-testnet", "-f", "testnet/Dockerfile", "."],
        project_dir=Path(__file__).parent,
        check=True,
    )


@pytest.fixture(scope="session")
def project_dir():
    return Path(__file__).parent


@pytest.fixture(scope="session")
def base_env(mesh_admin):
    auth_file = Path("auth.json")
    if not auth_file.exists():
        pytest.skip("No auth file found. Please run 'meshadmin login' first.")

    return {
        "MESH_SERVER_URL": mesh_admin,
        "KEYCLOAK_BASE_URL": "http://auth.dmeshadmin.hydo.ch",
        "KEYCLOAK_REALM": "meshadmin",
        "KEYCLOAK_ADMIN_CLIENT": "admin-cli",
    }


@pytest.fixture(scope="session")
def test_templates(base_env, test_network, project_dir):
    try:
        # Create lighthouse template
        result = run_docker_compose(
            [
                "run",
                "--rm",
                "admin",
                "meshadmin",
                "create-template",
                "lighthouse",
                test_network,
                "true",
                "true",
                "true",
            ],
            project_dir,
            env=base_env,
        )
        assert result.returncode == 0, (
            f"Failed to create lighthouse template: {result.stderr}"
        )
        lighthouse_key = json.loads(result.stdout)["enrollment_key"]

        # Create host template
        result = run_docker_compose(
            [
                "run",
                "--rm",
                "admin",
                "meshadmin",
                "create-template",
                "host",
                test_network,
                "false",
                "false",
                "true",
            ],
            project_dir,
            env=base_env,
        )
        assert result.returncode == 0, (
            f"Failed to create host template: {result.stderr}"
        )
        host_key = json.loads(result.stdout)["enrollment_key"]

        yield {
            "network_name": test_network,
            "lighthouse_key": lighthouse_key,
            "host_key": host_key,
        }
    finally:
        # Cleanup
        for template in ["lighthouse", "host"]:
            run_docker_compose(
                [
                    "run",
                    "--rm",
                    "admin",
                    "meshadmin",
                    "delete-template",
                    template,
                ],
                project_dir,
                env=base_env,
            )
        for host in ["lighthouse_hetzner", "host1", "host2"]:
            run_docker_compose(
                [
                    "run",
                    "--rm",
                    "admin",
                    "meshadmin",
                    "delete-host",
                    host,
                ],
                project_dir,
                env=base_env,
            )


@pytest.fixture(scope="session")
def test_env(base_env, test_templates):
    full_env = base_env.copy()
    full_env.update(
        {
            "LIGHTHOUSE_ENROLLMENT_KEY": test_templates["lighthouse_key"],
            "HOST_ENROLLMENT_KEY": test_templates["host_key"],
            "MESH_ADMIN_ENDPOINT": mesh_admin,
            "MESH_CONFIG_PATH": "/tmp/",
            "LIGHTHOUSE_PUBLIC_IP": "128.140.42.121",
            "LIGHTHOUSE_HOSTNAME": "lighthouse_hetzner",
            "HOST_PUBLIC_IP": "127.0.0.1",
        }
    )
    return full_env


@pytest.fixture(scope="session")
def test_network(test_env, project_dir):
    result = run_docker_compose(
        [
            "run",
            "--rm",
            "admin",
            "meshadmin",
            "create-network",
            "test_network",
            "100.100.64.0/24",
        ],
        project_dir,
        env=test_env,
    )
    assert result.returncode == 0, f"Failed to create network: {result.stderr}"
    return "test_network"


def print_container_logs(project_dir):
    for service in ["lighthouse_hetzner", "host1", "host2"]:
        logs = run_docker_compose(["logs", service], project_dir)
        print(f"\n=== {service} logs ===\n{logs.stdout}")


def wait_for_enrollment(project_dir, service_name, max_attempts=3, delay=5):
    for _ in range(max_attempts):
        logs = run_docker_compose(["logs", service_name], project_dir)
        if "enrollment finished" in logs.stdout:
            return True
        time.sleep(delay)
    return False


@pytest.mark.runtime
def test_network_setup(project_dir, test_env, mesh_admin, test_templates):
    try:
        # Check lighthouse enrollment and startup
        subprocess.run(
            ["docker", "compose", "up", "-d", "lighthouse_hetzner"],
            cwd=project_dir,
            env=test_env,
            capture_output=True,
            text=True,
            check=True,
        )
        time.sleep(10)
        assert wait_for_enrollment(project_dir, "lighthouse_hetzner"), (
            "Lighthouse enrollment failed"
        )
        assert (
            "starting nebula"
            in subprocess.run(
                ["docker", "compose", "logs", "lighthouse_hetzner"],
                cwd=project_dir,
                capture_output=True,
                text=True,
            ).stdout
        ), "Lighthouse nebula startup failed"

        # Check host1 enrollment and startup
        subprocess.run(
            ["docker", "compose", "up", "-d", "host1"],
            cwd=project_dir,
            env=test_env,
            capture_output=True,
            text=True,
            check=True,
        )
        time.sleep(10)
        assert wait_for_enrollment(project_dir, "host1"), "Host1 enrollment failed"
        assert (
            "starting nebula"
            in subprocess.run(
                ["docker", "compose", "logs", "host1"],
                cwd=project_dir,
                capture_output=True,
                text=True,
            ).stdout
        ), "Host1 nebula startup failed"

        # Check host2 enrollment and startup
        subprocess.run(
            ["docker", "compose", "up", "-d", "host2"],
            cwd=project_dir,
            env=test_env,
            capture_output=True,
            text=True,
            check=True,
        )
        time.sleep(10)
        assert wait_for_enrollment(project_dir, "host2"), "Host2 enrollment failed"
        assert (
            "starting nebula"
            in subprocess.run(
                ["docker", "compose", "logs", "host2"],
                cwd=project_dir,
                capture_output=True,
                text=True,
            ).stdout
        ), "Host2 nebula startup failed"
    except AssertionError:
        print_container_logs(project_dir)
        raise
    finally:
        subprocess.run(
            ["docker", "compose", "down", "-v"],
            cwd=project_dir,
            capture_output=True,
        )
