import asyncio
import json
import os
import platform
import shutil
import signal
import subprocess
import sys
from datetime import datetime, timedelta
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from time import sleep
from typing import Annotated
from uuid import uuid4

import httpx
import jwt
import structlog
import typer
import yaml
from jwcrypto.jwk import JWK
from jwcrypto.jwt import JWT
from jwt import decode
from rich import print, print_json

from meshadmin.cli.config import load_config
from meshadmin.common import schemas
from meshadmin.common.utils import (
    create_expiration_date,
    create_keys,
    download_nebula_binaries,
    get_default_config_path,
    get_nebula_path,
    get_public_ip,
)

app = typer.Typer()
logger = structlog.get_logger(__name__)

nebula_app = typer.Typer()
app.add_typer(nebula_app, name="nebula", help="Manage the nebula service")

service_app = typer.Typer()
app.add_typer(service_app, name="service", help="Manage the meshadmin service")

network_app = typer.Typer()
app.add_typer(network_app, name="network", help="Manage networks")

template_app = typer.Typer()
app.add_typer(template_app, name="template", help="Manage templates")

host_app = typer.Typer()
app.add_typer(host_app, name="host", help="Manage hosts")

host_config_app = typer.Typer()
host_app.add_typer(host_config_app, name="config", help="Manage host configurations")

context_app = typer.Typer()
app.add_typer(context_app, name="context", help="Manage network contexts")


def version_callback(value: bool):
    if value:
        try:
            installed_version = version("meshadmin")
            typer.echo(f"meshadmin version {installed_version}")
        except PackageNotFoundError:
            typer.echo("meshadmin is not installed")
        raise typer.Exit()


def get_context_config():
    if not config.contexts_file.exists():
        print("No contexts found")
        raise typer.Exit(1)

    with open(config.contexts_file) as f:
        contexts = yaml.safe_load(f) or {}

    current = os.getenv("MESH_CONTEXT")
    if not current:
        active_contexts = [
            name for name, data in contexts.items() if data.get("active")
        ]
        current = active_contexts[0] if active_contexts else None

    if not current or current not in contexts:
        print("No active context. Please select a context with 'meshadmin context use'")
        raise typer.Exit(1)

    context_data = contexts[current]
    network_dir = config.networks_dir / current

    return {
        "name": current,
        "endpoint": context_data["endpoint"],
        "interface": context_data["interface"],
        "network_dir": network_dir,
    }


@app.callback()
def main(
    ctx: typer.Context,
    version: bool = typer.Option(
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Show the version and exit.",
    ),
    config_path: Annotated[
        Path,
        typer.Option(
            "--config-path",
            "-c",
            envvar="MESHADMIN_CONFIG_PATH",
            help="Path to the configuration directory",
        ),
    ] = get_default_config_path(),
    context: Annotated[
        str,
        typer.Option(
            "--context",
            envvar="MESH_CONTEXT",
            help="Name of the context to use",
        ),
    ] = None,
):
    global config
    config = load_config(config_path)

    if context:
        if not config.contexts_file.exists():
            print("No contexts found")
            raise typer.Exit(1)

        with open(config.contexts_file) as f:
            contexts = yaml.safe_load(f) or {}

        if context not in contexts:
            print(f"Context '{context}' not found")
            raise typer.Exit(1)

        for ctx_name in contexts:
            contexts[ctx_name]["active"] = ctx_name == context

        with open(config.contexts_file, "w") as f:
            yaml.dump(contexts, f)


@nebula_app.command()
def download():
    try:
        context = get_context_config()
        nebula_path = get_nebula_path()
        if not nebula_path or not Path(nebula_path).exists():
            logger.info("Nebula binaries not found, downloading...")
            download_nebula_binaries(context["endpoint"])
        else:
            logger.info("Nebula binaries already downloaded")
    except Exception as e:
        logger.error("Failed to download nebula binaries", error=str(e))
        raise typer.Exit(code=1)


@host_app.command(name="enroll")
def host_enroll(
    enrollment_key: Annotated[
        str,
        typer.Argument(envvar="MESH_ENROLLMENT_KEY"),
    ],
    preferred_hostname: Annotated[
        str,
        typer.Option(envvar="MESH_HOSTNAME"),
    ] = None,
    public_ip: Annotated[
        str,
        typer.Option(envvar="MESH_PUBLIC_IP"),
    ] = None,
):
    context = get_context_config()
    network_dir = context["network_dir"]

    download()
    logger.info("enrolling")

    network_dir.mkdir(parents=True, exist_ok=True)

    # Use shared auth key for all contexts
    private_auth_key_path = config.contexts_file.parent / config.private_key
    if not private_auth_key_path.exists():
        logger.info("creating auth key")
        create_auth_key(private_auth_key_path.parent)

    jwk = JWK.from_json(private_auth_key_path.read_text())
    public_auth_key = jwk.export_public()
    logger.info("public key for registration", public_key=public_auth_key)

    private_net_key_path = network_dir / config.private_net_key_file
    public_net_key_path = network_dir / config.public_net_key_file

    if public_ip is None:
        public_ip = get_public_ip()
        logger.info(
            "public ip not set, using ip reported by https://checkip.amazonaws.com/",
            public_ip=public_ip,
        )

    if preferred_hostname is None:
        preferred_hostname = platform.node()
        logger.info(
            "preferred hostname not set, using system hostname",
            hostname=preferred_hostname,
        )

    if private_net_key_path.exists() and public_net_key_path.exists():
        public_nebula_key = public_net_key_path.read_text()
        logger.info(
            "private and public nebula key already exists",
            public_key=public_nebula_key,
        )
    else:
        logger.info("creating private and public nebula key")
        private, public_nebula_key = create_keys()
        private_net_key_path.write_text(private)
        private_auth_key_path.chmod(0o600)
        public_net_key_path.write_text(public_nebula_key)
        public_net_key_path.chmod(0o600)
        logger.info(
            "private and public nebula key created", public_nebula_key=public_nebula_key
        )

    enrollment = schemas.ClientEnrollment(
        enrollment_key=enrollment_key,
        public_net_key=public_nebula_key,
        public_auth_key=public_auth_key,
        preferred_hostname=preferred_hostname,
        public_ip=public_ip,
        interface=context["interface"],
    )

    res = httpx.post(
        f"{context['endpoint']}/api/v1/enroll",
        content=enrollment.model_dump_json(),
        headers={"Content-Type": "application/json"},
    )
    res.raise_for_status()

    get_config()
    logger.info("enrollment response", enrollment=res.content)
    logger.info("enrollment finished")


@service_app.command(name="install")
def service_install():
    context = get_context_config()
    network_dir = context["network_dir"]
    context_name = context["name"]
    os_name = platform.system()
    meshadmin_path = shutil.which("meshadmin")

    if not meshadmin_path:
        logger.error("meshadmin executable not found in PATH")
        exit(1)

    (network_dir / "env").write_text(f"MESH_CONTEXT={context_name}\n")

    if os_name == "Darwin":
        plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.meshadmin.{context_name}</string>
    <key>ProgramArguments</key>
    <array>
        <string>{meshadmin_path}</string>
        <string>nebula</string>
        <string>start</string>
    </array>
    <key>EnvironmentVariables</key>
    <dict>
        <key>MESH_CONTEXT</key>
        <string>{context_name}</string>
    </dict>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardErrorPath</key>
    <string>{network_dir}/error.log</string>
    <key>StandardOutPath</key>
    <string>{network_dir}/output.log</string>
</dict>
</plist>
"""
        launch_agents_dir = Path(os.path.expanduser("~/Library/LaunchAgents"))
        if not launch_agents_dir.exists():
            launch_agents_dir.mkdir(exist_ok=True, parents=True)
        plist_path = launch_agents_dir / f"com.meshadmin.{context_name}.plist"
        plist_path.write_text(plist_content)
        subprocess.run(["launchctl", "load", str(plist_path)])
        logger.info(
            "meshadmin service installed and started",
            plist_path=str(plist_path),
            context_name=context_name,
        )
        print(f"meshadmin service installed at {plist_path}")
        print(f"Context: {context_name}")
        print("Service has been loaded and will start automatically on login")

    else:
        systemd_unit = f"""[Unit]
Description=Meshadmin {context_name}
Wants=basic.target network-online.target nss-lookup.target time-sync.target
After=basic.target network.target network-online.target
Before=sshd.service

[Service]
#Type=notify
#NotifyAccess=main
SyslogIdentifier={context_name}
EnvironmentFile={network_dir}/env
ExecReload=/bin/kill -HUP $MAINPID
ExecStart={meshadmin_path} nebula start
Restart=always

[Install]
WantedBy=multi-user.target
"""
        systemd_service_path = Path(
            f"/usr/lib/systemd/system/meshadmin-{context_name}.service"
        )
        systemd_service_path.write_text(systemd_unit)
        subprocess.run(["systemctl", "daemon-reload"])
        subprocess.run(["systemctl", "enable", f"meshadmin-{context_name}"])
        print(f"meshadmin service installed at {systemd_service_path}")
        print(f"Context: {context_name}")
        print("Service has been enabled and will start automatically on boot")


@service_app.command(name="uninstall")
def service_uninstall():
    context = get_context_config()
    context_name = context["name"]
    network_dir = context["network_dir"]
    os_name = platform.system()

    if os_name == "Darwin":
        plist_path = Path(
            os.path.expanduser(
                f"~/Library/LaunchAgents/com.meshadmin.{context_name}.plist"
            )
        )
        if plist_path.exists():
            subprocess.run(["launchctl", "unload", str(plist_path)])
            plist_path.unlink()
            env_path = network_dir / "env"
            if env_path.exists():
                env_path.unlink()
            logger.info("meshadmin service uninstalled", plist_path=str(plist_path))
            print(f"meshadmin service uninstalled from {plist_path}")
        else:
            logger.warning("meshadmin service not found", plist_path=str(plist_path))
            print("meshadmin service not found, nothing to uninstall")
    else:
        systemd_service_path = Path(
            f"/usr/lib/systemd/system/meshadmin-{context_name}.service"
        )
        if systemd_service_path.exists():
            subprocess.run(["systemctl", "stop", f"meshadmin-{context_name}"])
            subprocess.run(["systemctl", "disable", f"meshadmin-{context_name}"])
            subprocess.run(["systemctl", "daemon-reload"])
            systemd_service_path.unlink()
            env_path = network_dir / "env"
            if env_path.exists():
                env_path.unlink()
            logger.info("meshadmin service uninstalled")
            print("meshadmin service uninstalled")
        else:
            logger.warning("meshadmin service not found")
            print("meshadmin service not found, nothing to uninstall")


@service_app.command(name="start")
def service_start():
    context = get_context_config()
    context_name = context["name"]
    os_name = platform.system()

    if os_name == "Darwin":
        plist_path = Path(
            os.path.expanduser(
                f"~/Library/LaunchAgents/com.meshadmin.{context_name}.plist"
            )
        )
        if plist_path.exists():
            subprocess.run(["launchctl", "load", str(plist_path)])
            logger.info("meshadmin service started", context=context_name)
            print(f"meshadmin service started for context {context_name}")
        else:
            logger.error("meshadmin service not installed", plist_path=str(plist_path))
            print(
                f"meshadmin service not installed for context {context_name}. Run 'meshadmin service install' first."
            )
    else:
        subprocess.run(["systemctl", "start", f"meshadmin-{context_name}"])
        print(f"meshadmin service started for context {context_name}")


@service_app.command(name="stop")
def service_stop():
    context = get_context_config()
    context_name = context["name"]
    os_name = platform.system()

    if os_name == "Darwin":
        plist_path = Path(
            os.path.expanduser(
                f"~/Library/LaunchAgents/com.meshadmin.{context_name}.plist"
            )
        )
        if plist_path.exists():
            subprocess.run(["launchctl", "unload", str(plist_path)])
            logger.info("meshadmin service stopped", context=context_name)
            print(f"meshadmin service stopped for context {context_name}")
        else:
            logger.error("meshadmin service not installed", plist_path=str(plist_path))
            print(
                f"meshadmin service not installed for context {context_name}. Nothing to stop."
            )
    else:
        subprocess.run(["systemctl", "stop", f"meshadmin-{context_name}"])
        print(f"meshadmin service stopped for context {context_name}")


@service_app.command(name="logs")
def service_logs(
    follow: Annotated[
        bool,
        typer.Option("--follow", "-f", help="Follow the logs in real time"),
    ] = False,
    lines: Annotated[
        int,
        typer.Option("--lines", "-n", help="Number of lines to show"),
    ] = 50,
):
    context = get_context_config()
    context_name = context["name"]
    network_dir = context["network_dir"]
    os_name = platform.system()

    if os_name == "Darwin":
        error_log = network_dir / "error.log"
        output_log = network_dir / "output.log"

        if not error_log.exists() and not output_log.exists():
            print(
                f"No log files found for context {context_name}. Has the service been started?"
            )
            raise typer.Exit(1)

        if follow:
            try:
                process = subprocess.Popen(
                    ["tail", "-f", str(error_log), str(output_log)],
                    stdout=sys.stdout,
                    stderr=sys.stderr,
                )
                process.wait()
            except KeyboardInterrupt:
                process.terminate()
        else:
            for log_file in [output_log, error_log]:
                if log_file.exists():
                    print(f"\n=== {log_file.name} ===")
                    result = subprocess.run(
                        ["tail", f"-n{lines}", str(log_file)],
                        capture_output=True,
                        text=True,
                    )
                    print(result.stdout)
    else:
        try:
            cmd = ["journalctl", "-u", f"meshadmin-{context_name}"]
            if follow:
                cmd.append("-f")
            if lines:
                cmd.append(f"-n{lines}")

            if follow:
                process = subprocess.Popen(
                    cmd,
                    stdout=sys.stdout,
                    stderr=sys.stderr,
                )
                process.wait()
            else:
                result = subprocess.run(cmd, capture_output=True, text=True)
                print(result.stdout)

        except subprocess.CalledProcessError as e:
            print(f"Error accessing logs: {e}")
            print(
                "Make sure the service is installed and you have appropriate permissions."
            )
            raise typer.Exit(1)


@host_app.command()
def create_auth_key(
    mesh_config_path: Annotated[
        Path,
        typer.Argument(envvar="MESH_CONFIG_PATH"),
    ] = get_default_config_path(),
):
    jwk = JWK.generate(kty="RSA", kid=str(uuid4()), size=2048)
    auth_key = mesh_config_path / config.private_key
    auth_key.write_text(jwk.export_private())
    auth_key.chmod(0o600)


@host_app.command()
def show_auth_public_key(
    mesh_config_path: Annotated[
        Path,
        typer.Argument(envvar="MESH_CONFIG_PATH"),
    ] = get_default_config_path(),
):
    jwk = JWK.from_json((mesh_config_path / config.private_key).read_text())
    print(jwk.export_public())


@host_config_app.command()
def get_config():
    private_net_key, public_net_key = create_keys()
    context = get_context_config()
    private_auth_key = JWK.from_json(
        (config.contexts_file.parent / config.private_key).read_text()
    )

    loop = asyncio.get_event_loop()

    result, _ = loop.run_until_complete(
        get_config_from_mesh(context["endpoint"], private_auth_key)
    )
    (context["network_dir"] / config.config_path).write_text(result)


async def get_config_from_mesh(mesh_admin_endpoint, private_auth_key):
    jwt = JWT(
        header={"alg": "RS256", "kid": private_auth_key.thumbprint()},
        claims={
            "exp": create_expiration_date(10),
            "kid": private_auth_key.thumbprint(),
        },
    )
    jwt.make_signed_token(private_auth_key)
    token = jwt.serialize()

    async with httpx.AsyncClient() as client:
        res = await client.get(
            f"{mesh_admin_endpoint}/api/v1/config",
            headers={"Authorization": f"Bearer {token}"},
        )
        res.raise_for_status()
        config = res.text
        update_interval = int(res.headers.get("X-Update-Interval", "5"))
        return config, update_interval


async def cleanup_ephemeral_hosts(mesh_admin_endpoint, private_auth_key):
    jwt_token = JWT(
        header={"alg": "RS256", "kid": private_auth_key.thumbprint()},
        claims={
            "exp": create_expiration_date(10),
            "kid": private_auth_key.thumbprint(),
        },
    )
    jwt_token.make_signed_token(private_auth_key)
    token = jwt_token.serialize()

    async with httpx.AsyncClient() as client:
        res = await client.post(
            f"{mesh_admin_endpoint}/api/v1/cleanup-ephemeral",
            headers={"Authorization": f"Bearer {token}"},
        )
        res.raise_for_status()
        return res.json()


async def start_nebula(network_dir: Path, mesh_admin_endpoint: str):
    await logger.ainfo("starting nebula")
    conf_path = network_dir / config.config_path
    assert conf_path.exists(), f"Config at {conf_path} does not exist"

    private_auth_key_path = config.contexts_file.parent / config.private_key
    assert private_auth_key_path.exists(), (
        f"private_key at {private_auth_key_path} does not exist"
    )

    async def start_process():
        return await asyncio.create_subprocess_exec(
            get_nebula_path(),
            "-config",
            str(conf_path),
            cwd=network_dir,
        )

    proc = await start_process()

    # Default update interval in seconds
    update_interval = 5

    while True:
        await asyncio.sleep(update_interval)
        try:
            private_auth_key_path = config.contexts_file.parent / config.private_key
            private_auth_key = JWK.from_json(private_auth_key_path.read_text())

            # Check for config updates
            try:
                new_config, new_update_interval = await get_config_from_mesh(
                    mesh_admin_endpoint, private_auth_key
                )

                if update_interval != new_update_interval:
                    await logger.ainfo(
                        "update interval changed",
                        old_interval=update_interval,
                        new_interval=new_update_interval,
                    )
                    update_interval = new_update_interval

                old_config = conf_path.read_text()
                if new_config != old_config:
                    await logger.ainfo("config changed, reloading")
                    conf_path.write_text(new_config)
                    conf_path.chmod(0o600)

                    try:
                        proc.send_signal(signal.SIGHUP)
                    except ProcessLookupError:
                        await logger.ainfo("process died, restarting")
                        proc = await start_process()
                else:
                    await logger.ainfo("config not changed")
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 401:
                    await logger.aerror(
                        "Could not get config because of authentication error. Host may have been deleted.",
                        error=str(e),
                        response_text=e.response.text,
                    )
                    print(
                        "Error: Could not get config because of authentication error. Host may have been deleted."
                    )
                    print(f"Server message: {e.response.text}")
                    break
                else:
                    await logger.aerror("error getting config", error=str(e))

            # Cleanup ephemeral hosts
            try:
                result = await cleanup_ephemeral_hosts(
                    mesh_admin_endpoint, private_auth_key
                )
                if result.get("removed_count", 0) > 0:
                    await logger.ainfo(
                        "removed stale ephemeral hosts",
                        count=result["removed_count"],
                    )
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 401:
                    await logger.aerror(
                        "Could not clean up ephemeral hosts because of authentication error. Host may have been deleted.",
                        error=str(e),
                        response_text=e.response.text,
                    )
                    print(
                        "Error: Could not clean up ephemeral hosts because of authentication error. Host may have been deleted."
                    )
                    print(f"Server message: {e.response.text}")
                    break
                else:
                    await logger.aerror("error during cleanup operation", error=str(e))

        except Exception:
            await logger.aexception("could not refresh token")
            if proc.returncode is not None:
                await logger.ainfo("process died, restarting")
                proc = await start_process()

    # Clean shutdown if we get here
    if proc.returncode is None:
        await logger.ainfo("shutting down nebula process")
        proc.terminate()
        try:
            await asyncio.wait_for(proc.wait(), timeout=5.0)
        except asyncio.TimeoutError:
            await logger.awarning("nebula process didn't terminate, killing it")
            proc.kill()


@nebula_app.command()
def start():
    context = get_context_config()
    asyncio.run(start_nebula(context["network_dir"], context["endpoint"]))


@app.command()
def login():
    res = httpx.post(
        config.keycloak_device_auth_url,
        data={
            "client_id": config.keycloak_admin_client,
        },
    )
    res.raise_for_status()

    device_auth_response = res.json()
    print(device_auth_response)
    print(
        "Please open the verification url",
        device_auth_response["verification_uri_complete"],
    )

    while True:
        res = httpx.post(
            config.keycloak_token_url,
            data={
                "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                "client_id": config.keycloak_admin_client,
                "device_code": device_auth_response["device_code"],
            },
        )
        if res.status_code == 200:
            logger.info("Received auth token")
            config.authentication_path.write_bytes(res.content)
            config.authentication_path.chmod(0o600)

            access_token = res.json()["access_token"]
            refresh_token = res.json()["refresh_token"]
            print(
                jwt.decode(
                    refresh_token,
                    algorithms=["RS256"],
                    options={"verify_signature": False},
                )
            )
            logger.info("access_token", access_token=access_token)
            print("successfully authenticated")
            break
        else:
            print(res.json())
        sleep(device_auth_response["interval"])


def get_access_token():
    if config.authentication_path.exists():
        auth = json.loads(config.authentication_path.read_text())
        access_token = auth["access_token"]

        decoded_token = decode(
            access_token, options={"verify_signature": False, "verify_exp": False}
        )

        # is exp still 2/3 of the time
        if decoded_token["exp"] >= (datetime.now() + timedelta(seconds=10)).timestamp():
            return access_token
        else:
            refresh_token = auth["refresh_token"]
            res = httpx.post(
                config.keycloak_token_url,
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": refresh_token,
                    "client_id": config.keycloak_admin_client,
                },
            )
            res.raise_for_status()
            config.authentication_path.write_bytes(res.content)
            return res.json()["access_token"]

    else:
        print("authentication failed")


@network_app.command(name="create")
def create_network(name: str, cidr: str):
    try:
        access_token = get_access_token()
    except Exception:
        logger.exception("failed to get access token")
        exit(1)

    context = get_context_config()
    res = httpx.post(
        f"{context['endpoint']}/api/v1/networks",
        content=schemas.NetworkCreate(name=name, cidr=cidr).model_dump_json(),
        headers={"Authorization": f"Bearer {access_token}"},
    )

    if res.status_code >= 400:
        print("could not create network:", res.text)
        exit(1)

    print_json(res.content.decode("utf-8"))


@network_app.command(name="list")
def list_networks():
    try:
        access_token = get_access_token()
    except Exception:
        logger.exception("failed to get access token")
        exit(1)

    context = get_context_config()
    res = httpx.get(
        f"{context['endpoint']}/api/v1/networks",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    res.raise_for_status()
    print(res.json())


@template_app.command(name="create")
def create_template(
    name: str, network_name: str, is_lighthouse: bool, is_relay: bool, use_relay: bool
):
    try:
        access_token = get_access_token()
    except Exception:
        logger.exception("failed to get access token")
        exit(1)

    context = get_context_config()
    res = httpx.post(
        f"{context['endpoint']}/api/v1/templates",
        content=schemas.TemplateCreate(
            name=name,
            network_name=network_name,
            is_lighthouse=is_lighthouse,
            is_relay=is_relay,
            use_relay=use_relay,
        ).model_dump_json(),
        headers={"Authorization": f"Bearer {access_token}"},
    )
    res.raise_for_status()
    print_json(res.content.decode("utf-8"))


@template_app.command()
def get_token(name: str):
    try:
        access_token = get_access_token()
    except Exception:
        logger.exception("failed to get access token")
        exit(1)

    context = get_context_config()
    res = httpx.get(
        f"{context['endpoint']}/api/v1/templates/{name}/token",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    res.raise_for_status()
    print(res.text)


@template_app.command(name="delete")
def delete_template(name: str):
    try:
        access_token = get_access_token()
    except Exception:
        logger.exception("failed to get access token")
        exit(1)

    context = get_context_config()
    res = httpx.delete(
        f"{context['endpoint']}/api/v1/templates/{name}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    res.raise_for_status()
    print(res.json())


@host_app.command(name="delete")
def delete_host(name: str):
    try:
        access_token = get_access_token()
    except Exception:
        logger.exception("failed to get access token")
        exit(1)

    context = get_context_config()
    res = httpx.delete(
        f"{context['endpoint']}/api/v1/hosts/{name}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    res.raise_for_status()
    print(res.json())


@context_app.command(name="create")
def create_context(
    name: Annotated[str, typer.Argument()],
    endpoint: Annotated[str, typer.Option()],
    interface: Annotated[str, typer.Option()] = "nebula1",
):
    config.contexts_file.parent.mkdir(parents=True, exist_ok=True)

    contexts = {}
    if config.contexts_file.exists():
        with open(config.contexts_file) as f:
            contexts = yaml.safe_load(f) or {}

    # If this is the first context, make it active
    is_first = len(contexts) == 0

    contexts[name] = {
        "endpoint": endpoint,
        "interface": interface,
        "active": is_first,
    }

    with open(config.contexts_file, "w") as f:
        yaml.dump(contexts, f)

    print(f"Created context '{name}'")
    if is_first:
        print(f"Set '{name}' as active context")


@context_app.command(name="use")
def use_context(name: str):
    if not config.contexts_file.exists():
        print("No contexts found")
        raise typer.Exit(1)

    with open(config.contexts_file) as f:
        contexts = yaml.safe_load(f) or {}

    if name not in contexts:
        print(f"Context '{name}' not found")
        raise typer.Exit(1)

    # Deactivate all contexts and activate the selected one
    for context_name in contexts:
        contexts[context_name]["active"] = False
    contexts[name]["active"] = True

    with open(config.contexts_file, "w") as f:
        yaml.dump(contexts, f)

    print(f"Switched to context '{name}'")


@context_app.command(name="list")
def list_contexts():
    if not config.contexts_file.exists():
        print("No contexts found")
        return

    with open(config.contexts_file) as f:
        contexts = yaml.safe_load(f)

    for name, data in contexts.items():
        print(
            f"{'* ' if data.get('active') else '  '}{name} ({data['endpoint']}) ({data['interface']})"
        )


@host_config_app.command(name="info")
def show_config_info():
    print("\nConfiguration Paths:")
    print(f"Contexts file: {config.contexts_file}")
    print(f"Networks directory: {config.networks_dir}")
    print(f"Authentication file: {config.authentication_path}")
    try:
        context = get_context_config()
        print("\nCurrent Context:")
        print(f"Name: {context['name']}")
        print(f"Endpoint: {context['endpoint']}")
        print(f"Interface: {context['interface']}")
        print(f"Network directory: {context['network_dir']}")

        config_file = context["network_dir"] / config.config_path
        env_file = context["network_dir"] / "env"
        private_key = context["network_dir"] / config.private_net_key_file

        print("\nContext Files:")
        print(
            f"Config file: {config_file} {'(exists)' if config_file.exists() else '(not found)'}"
        )
        print(
            f"Environment file: {env_file} {'(exists)' if env_file.exists() else '(not found)'}"
        )
        print(
            f"Private key: {private_key} {'(exists)' if private_key.exists() else '(not found)'}"
        )
        if platform.system() == "Darwin":
            service_file = Path(
                os.path.expanduser(
                    f"~/Library/LaunchAgents/com.meshadmin.{context['name']}.plist"
                )
            )
            print(
                f"Service file: {service_file} {'(exists)' if service_file.exists() else '(not found)'}"
            )
        else:
            service_file = Path(
                f"/usr/lib/systemd/system/meshadmin-{context['name']}.service"
            )
            print(
                f"Service file: {service_file} {'(exists)' if service_file.exists() else '(not found)'}"
            )
    except typer.Exit:
        print("\nNo active context found")


if __name__ == "__main__":
    app()
