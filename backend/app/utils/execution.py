from __future__ import annotations

import io
import json
from dataclasses import dataclass
from typing import Optional

import os
import docker
from docker.errors import DockerException, ContainerError


EXECUTION_IMAGE = "devpreplab-execution:latest"
DEFAULT_TIME_LIMIT_SECONDS = 5
DEFAULT_MEMORY_LIMIT_MB = 256


@dataclass
class ExecutionOutcome:
    status: str  # "passed", "failed", "error", "timeout"
    stdout: str
    stderr: str
    execution_time_ms: Optional[int] = None
    memory_kb: Optional[int] = None


def _build_python_command(code: str, test_input: str) -> list[str]:
    # A tiny harness: read input from a file and print result. In Phase 3 we
    # focus on safe execution with limits; richer harnessing can be added later.
    runner_source = f"""
import json
import sys

user_ns = {{}}

code = {code!r}
exec(code, user_ns)

if "solution" not in user_ns:
    raise SystemExit("No `solution` function defined")

fn = user_ns["solution"]

with open("input.json", "r", encoding="utf-8") as f:
        payload = json.load(f)

        result = fn(**payload)
print(json.dumps(result))
"""
    return [
        "python",
        "-c",
        runner_source,
    ]


def run_python_code_against_input(
    code: str,
    test_input: dict,
    time_limit_seconds: int = DEFAULT_TIME_LIMIT_SECONDS,
    memory_limit_mb: int = DEFAULT_MEMORY_LIMIT_MB,
) -> ExecutionOutcome:
    # Create Docker client with explicit base_url to avoid DOCKER_HOST issues
    # Use the default Unix socket directly
    try:
        client = docker.from_env()
    except Exception as e:
        return ExecutionOutcome(
            status="error",
            stdout="",
            stderr=f"Failed to connect to Docker: {str(e)}"
        )


    input_bytes = json.dumps(test_input).encode("utf-8")

    container = None
    try:
        # Create container with resource limits and no network
        container = client.containers.create(
            image=EXECUTION_IMAGE,
            command=_build_python_command(code, "input.json"),
            network_disabled=True,
            mem_limit=f"{memory_limit_mb}m",
            nano_cpus=1_000_000_000,  # 1 CPU
            working_dir="/workspace",
            stdin_open=False,
            tty=False,
        )

        # Put input.json into the container
        tar_stream = io.BytesIO()
        import tarfile

        with tarfile.open(fileobj=tar_stream, mode="w") as tar:
            tarinfo = tarfile.TarInfo(name="input.json")
            tarinfo.size = len(input_bytes)
            tar.addfile(tarinfo, io.BytesIO(input_bytes))
        tar_stream.seek(0)
        container.put_archive("/workspace", tar_stream.read())

        container.start()

        result = container.wait(timeout=time_limit_seconds)
        exit_code = result.get("StatusCode", 1)
        logs = container.logs(stdout=True, stderr=True)
        stdout_text = logs.decode("utf-8", errors="replace")

        if exit_code == 0:
            try:
                # If it exited cleanly we treat as "passed"; higher level can
                # compare against expected output.
                return ExecutionOutcome(status="passed", stdout=stdout_text, stderr="")
            except json.JSONDecodeError as exc:  # pragma: no cover - defensive
                return ExecutionOutcome(
                    status="error",
                    stdout=stdout_text,
                    stderr=f"Invalid JSON output: {exc}",
                )
        else:
            return ExecutionOutcome(status="error", stdout=stdout_text, stderr="")

    except docker.errors.APIError as exc:  # pragma: no cover - infrastructure
        return ExecutionOutcome(status="error", stdout="", stderr=str(exc))
    except ContainerError as exc:  # pragma: no cover - defensive
        return ExecutionOutcome(status="error", stdout=str(exc), stderr="")
    except DockerException as exc:  # pragma: no cover - infrastructure
        return ExecutionOutcome(status="error", stdout="", stderr=str(exc))
    except Exception as exc:  # pragma: no cover - catch-all
        return ExecutionOutcome(status="error", stdout="", stderr=str(exc))
    finally:
        try:
            container.remove(force=True)  # type: ignore[name-defined]
        except Exception:
            pass