import logging
import os

import attrs
import yt.wrapper as yt

from tractoray.internal.coordinator import (
    HeadCoordinatorFactory,
    WorkerCoordinatorFactory,
)
from tractoray.internal.ray import (
    HeadNode,
    WorkerNode,
)
from tractoray.ytpath import YtPath


_LOGGER = logging.getLogger(__name__)


@attrs.define(kw_only=True, slots=True, auto_attribs=True)
class BootstrapperHead:
    _yt_proxy: str
    _yt_token: str
    _workdir: YtPath
    _cpu_limit: int
    _node_count: int

    _node_index: int
    _operation_id: str
    _job_id: str

    _head_port: int
    _dashboard_port: int
    _dashboard_agent_listen_port: int
    _public_dashboard_port: int
    _client_port: int
    _runtime_env_agent_port: int

    def run(self) -> None:
        yt_client = yt.YtClient(proxy=self._yt_proxy, token=self._yt_token)
        hostname = _get_hostname(
            yt_client=yt_client,
            job_id=self._job_id,
            operation_id=self._operation_id,
        )
        _fix_hosts(hostname=hostname)

        HeadCoordinatorFactory(
            self_endpoint=hostname,
            node_index=self._node_index,
            node_count=self._node_count,
            coordinator_path=_make_coordinator_path(self._workdir),
            yt_client=yt_client,
            operation_id=self._operation_id,
            wait_barrier=True,
            head_port=self._head_port,
            public_dashboard_port=self._public_dashboard_port,
            client_port=self._client_port,
        ).make()

        head_node = HeadNode(
            self_endpoint=hostname,
            cpu_limit=self._cpu_limit,
            head_port=self._head_port,
            dashboard_port=self._dashboard_port,
            dashboard_agent_listen_port=self._dashboard_agent_listen_port,
            client_port=self._client_port,
            runtime_env_agent_port=self._runtime_env_agent_port,
            yt_client=yt_client,
            public_dashboard_port=self._public_dashboard_port,
        )
        head_node.run()


@attrs.define(kw_only=True, slots=True, auto_attribs=True)
class BootstrapperNode:
    _yt_proxy: str
    _yt_token: str
    _workdir: YtPath
    _cpu_limit: int
    _node_count: int

    _node_index: int
    _operation_id: str
    _job_id: str

    _runtime_env_agent_port: int

    def run(self) -> None:
        yt_client = yt.YtClient(proxy=self._yt_proxy, token=self._yt_token)
        hostname = _get_hostname(
            yt_client=yt_client,
            job_id=self._job_id,
            operation_id=self._operation_id,
        )
        _fix_hosts(hostname=hostname)

        runtime_env_agent_port = int(os.environ["YT_PORT_0"])

        coordinator = WorkerCoordinatorFactory(
            self_endpoint=hostname,
            node_index=self._node_index,
            node_count=self._node_count,
            coordinator_path=_make_coordinator_path(self._workdir),
            yt_client=yt_client,
            operation_id=self._operation_id,
            wait_barrier=True,
        ).make()

        WorkerNode(
            cpu_limit=self._cpu_limit,
            head_endpoint=coordinator.head_endpoint,
            head_port=coordinator.head_port,
            self_endpoint=hostname,
            runtime_env_agent_port=runtime_env_agent_port,
        ).run()


def _make_coordinator_path(workdir: YtPath) -> YtPath:
    return YtPath(f"{workdir}/coordinator")


def _get_hostname(operation_id: str, job_id: str, yt_client: yt.YtClient) -> str:
    return str(
        yt_client.get_job(operation_id=operation_id, job_id=job_id)["address"]
    ).split(":")[0]


def _fix_hosts(hostname: str) -> None:
    with open("/etc/hosts", "a") as f:
        f.write(f"\n127.0.0.1\t{hostname}\n")
