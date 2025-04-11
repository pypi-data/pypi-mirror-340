import logging
import os
import shlex
import time

import attrs
import yt.wrapper as yt
from yt.wrapper.operation_commands import OperationState

from tractoray.errors import RunError
from tractoray.internal.coordinator import (
    CoordinationInfo,
    CoordinationInfoFactory,
)
from tractoray.internal.logs import setup_logging
from tractoray.internal.ray import (
    AriadneTransformer,
    RayInfo,
)
from tractoray.ytpath import YtPath


_LOGGER = logging.getLogger(__name__)
_DEFAULT_TIMEOUT = 5.0
_DEFAULT_MEMORY_LIMIT = 32 * 1024 * 1024 * 1024
_DEFAULT_DOCKER_IMAGE: str = (
    "cr.eu-north1.nebius.cloud/e00faee7vas5hpsh3s/chiffa/tractoray/jupyter:2025-04-09-21-12-04-f0cc63c31"
)
_DEFAULT_CPU_LIMIT = 100
_DEFAULT_GPU_LIMIT = 0
_DEFAULT_POOL_TREES = ["default"]


@attrs.define(kw_only=True, slots=True, auto_attribs=True)
class RunInfo:
    _operation_id: str
    _coordinator_path: YtPath
    _yt_client: yt.YtClient

    def get_coordination_info(self) -> CoordinationInfo | None:
        info = CoordinationInfoFactory(
            yt_client=yt.YtClient(config=yt.default_config.get_config_from_env()),
            coordinator_path=self._coordinator_path,
        ).get()
        if info and info.operation_id == self._operation_id and info.is_ready():
            return info
        return None

    def check_operation(self) -> None:
        current_operation_state: OperationState = yt.get_operation_state(
            self._operation_id
        )
        if current_operation_state.is_unsuccessfully_finished():
            raise RunError(
                f"Current operation {self._operation_id} is failed",
            )

    @property
    def operation_url(self) -> str:
        url = yt.operation_commands.get_operation_url(
            self._operation_id,
            client=self._yt_client,
        )
        assert isinstance(url, str)
        return url


@attrs.define(kw_only=True, slots=True, auto_attribs=True)
class YtRunner:
    _workdir: str
    _yt_client: yt.YtClient
    _node_count: int
    _docker_image: str
    _cpu_limit: int
    _gpu_limit: int
    _memory_limit: int
    _pool_trees: list[str]
    _log_level: str | None

    def _make_env(self) -> dict[str, str]:
        env = {
            "YT_ALLOW_HTTP_REQUESTS_TO_YT_FROM_JOB": "1",
            "PYTHONDONTWRITEBYTECODE": "1",
        }
        if self._log_level is not None:
            env["YT_LOG_LEVEL"] = self._log_level
        return env

    def _make_head_task(
        self, operation_spec: yt.VanillaSpecBuilder
    ) -> yt.VanillaSpecBuilder:
        task_spec = operation_spec.begin_task("head")
        command = [
            "python3 -m tractoray.cli.bootstrapper head",
            f"--workdir {shlex.quote(self._workdir)}",
            # node count here is a total node count in the cluster, including head node
            f"--node-count {self._node_count}",
            f"--cpu-limit {self._cpu_limit}",
            f"--proxy {self._yt_proxy}",
        ]
        escaped_command = " ".join(command)
        _LOGGER.debug("Running command: %s", escaped_command)

        task_spec.command(escaped_command)
        task_spec.environment(self._make_env())
        task_spec.job_count(1)
        task_spec.docker_image(self._docker_image)
        task_spec.cpu_limit(self._cpu_limit)
        task_spec.port_count(6)
        task_spec.gpu_limit(self._gpu_limit)
        task_spec.memory_limit(self._memory_limit)
        return task_spec.end_task()

    def _make_node_task(
        self, operation_spec: yt.VanillaSpecBuilder
    ) -> yt.VanillaSpecBuilder:
        node_count = self._node_count - 1
        if node_count <= 0:
            return operation_spec
        task_spec = operation_spec.begin_task("node")
        command = [
            "python3 -m tractoray.cli.bootstrapper node",
            f"--workdir {shlex.quote(self._workdir)}",
            # node count here is a total node count in the cluster, including head node
            f"--node-count {self._node_count}",
            f"--cpu-limit {self._cpu_limit}",
            f"--proxy {self._yt_proxy}",
        ]
        escaped_command = " ".join(command)
        _LOGGER.debug("Running command: %s", escaped_command)

        task_spec.command(escaped_command)
        task_spec.environment(self._make_env())
        task_spec.job_count(node_count)
        task_spec.docker_image(self._docker_image)
        task_spec.cpu_limit(self._cpu_limit)
        task_spec.port_count(1)
        task_spec.gpu_limit(self._gpu_limit)
        task_spec.memory_limit(self._memory_limit)
        return task_spec.end_task()

    @property
    def _yt_token(self) -> str:
        token = yt.http_helpers.get_token(client=self._yt_client)
        assert isinstance(token, str)
        return token

    @property
    def _yt_proxy(self) -> str:
        proxy = self._yt_client.config["proxy"]["url"]
        assert isinstance(proxy, str)
        return proxy

    def run(self) -> RunInfo:
        coordinator_path = YtPath(f"{self._workdir}/coordinator")
        info = CoordinationInfoFactory(
            yt_client=self._yt_client,
            coordinator_path=coordinator_path,
        ).get()
        if info and info.operation_id:
            prev_operation_state: OperationState = yt.get_operation_state(
                info.operation_id
            )
            if prev_operation_state.is_running():
                operation_url = yt.operation_commands.get_operation_url(
                    info.operation_id, client=self._yt_client
                )
                raise RunError(
                    f"Previous operation {operation_url} is still running",
                )

        operation_spec = yt.VanillaSpecBuilder()
        operation_spec = self._make_head_task(operation_spec)
        operation_spec = self._make_node_task(operation_spec)
        operation_spec.title(f"ray {self._workdir}")
        operation_spec.secure_vault(
            {
                "USER_YT_TOKEN": self._yt_token,
            },
        )
        operation_spec.pool_trees(self._pool_trees)
        operation = self._yt_client.run_operation(operation_spec, sync=False)
        return RunInfo(
            operation_id=operation.id,
            coordinator_path=coordinator_path,
            yt_client=self._yt_client,
        )


def _get_docker_image() -> str:
    return (
        os.environ.get("YT_BASE_LAYER")
        or os.environ.get("YT_JOB_DOCKER_IMAGE")
        or _DEFAULT_DOCKER_IMAGE
    )


def run(
    workdir: str,
    node_count: int = 1,
    docker_image: str | None = None,
    cpu_limit: int = _DEFAULT_CPU_LIMIT,
    gpu_limit: int = _DEFAULT_GPU_LIMIT,
    memory_limit: int = _DEFAULT_MEMORY_LIMIT,
    pool_trees: list[str] | None = None,
    yt_client: yt.YtClient | None = None,
) -> RayInfo:
    log_level = setup_logging()
    if pool_trees is None:
        pool_trees = _DEFAULT_POOL_TREES
    if docker_image is None:
        docker_image = _get_docker_image()

    if yt_client is None:
        yt_client = yt.YtClient(config=yt.default_config.get_config_from_env())

    runner = YtRunner(
        workdir=workdir,
        yt_client=yt_client,
        node_count=node_count,
        docker_image=docker_image,
        cpu_limit=cpu_limit,
        gpu_limit=gpu_limit,
        memory_limit=memory_limit,
        pool_trees=pool_trees,
        log_level=log_level,
    )
    info = runner.run()
    while True:
        info.check_operation()
        coordination_info = info.get_coordination_info()
        if coordination_info:
            return RayInfo(
                coordination_info=coordination_info,
                yt_client=yt_client,
                transformer=AriadneTransformer.create(yt_client),
            )
        time.sleep(_DEFAULT_TIMEOUT)
