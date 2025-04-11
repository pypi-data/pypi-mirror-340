import argparse
import logging
import time

import yt.wrapper as yt
from yt.wrapper.operation_commands import OperationState

from tractoray.internal.coordinator import CoordinationInfoFactory
from tractoray.internal.logs import setup_logging
from tractoray.internal.ray import (
    AriadneTransformer,
    RayInfo,
)
from tractoray.runner import (
    _DEFAULT_CPU_LIMIT,
    _DEFAULT_GPU_LIMIT,
    _DEFAULT_MEMORY_LIMIT,
    _DEFAULT_POOL_TREES,
    YtRunner,
    _get_docker_image,
)
from tractoray.ytpath import YtPath


_LOGGER = logging.getLogger(__name__)
_DEFAULT_TIMEOUT = 5.0


def main() -> None:
    log_level = setup_logging()
    parser = argparse.ArgumentParser(
        description="Tractoray CLI tool",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    start_parser = subparsers.add_parser(
        "start",
        help="Start Ray cluster on Tracto",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    start_parser.add_argument(
        "--workdir",
        required=True,
        type=str,
        help="Working directory path in YT",
    )
    start_parser.add_argument(
        "--node-count",
        type=int,
        default=1,
        help="Number of nodes in cluster",
    )
    start_parser.add_argument(
        "--docker-image",
        type=str,
        help="Docker image for nodes",
    )
    start_parser.add_argument(
        "--cpu-limit",
        type=int,
        default=_DEFAULT_CPU_LIMIT,
        help="CPU limit per node",
    )
    start_parser.add_argument(
        "--gpu-limit",
        type=int,
        default=_DEFAULT_GPU_LIMIT,
        help="GPU limit per node",
    )
    start_parser.add_argument(
        "--memory-limit",
        type=int,
        default=_DEFAULT_MEMORY_LIMIT,
        help="Memory limit per node in bytes",
    )
    start_parser.add_argument(
        "--pool-trees",
        nargs="+",
        default=_DEFAULT_POOL_TREES,
        help="Pool trees to use",
    )

    status_parser = subparsers.add_parser(
        "status",
        help="Status of Ray cluster",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    status_parser.add_argument(
        "--workdir",
        required=True,
        type=str,
        help="Working directory path in YT",
    )

    stop_parser = subparsers.add_parser(
        "stop",
        help="Stop running Ray cluster",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    stop_parser.add_argument(
        "--workdir",
        required=True,
        type=str,
        help="Working directory path in YT",
    )

    args = parser.parse_args()

    yt_client = yt.YtClient(config=yt.default_config.get_config_from_env())

    if args.command == "start":
        print("Starting Ray cluster.")
        docker_image = args.docker_image
        if docker_image is None:
            docker_image = _get_docker_image()
        runner = YtRunner(
            workdir=args.workdir,
            node_count=args.node_count,
            docker_image=docker_image,
            cpu_limit=args.cpu_limit,
            gpu_limit=args.gpu_limit,
            memory_limit=args.memory_limit,
            pool_trees=args.pool_trees,
            log_level=log_level,
            yt_client=yt_client,
        )
        run_info = runner.run()
        print(f"Tracto operation: {run_info.operation_url}")
        while True:
            run_info.check_operation()
            coordination_info = run_info.get_coordination_info()
            if coordination_info:
                print("Ray cluster started.")
                break
            time.sleep(_DEFAULT_TIMEOUT)
        ray_info = RayInfo(
            coordination_info=coordination_info,
            yt_client=yt_client,
            transformer=AriadneTransformer.create(yt_client),
        )
        print(ray_info.dashboard_instruction)
        print(ray_info.cli_instruction)
        print(ray_info.client_instruction)
    elif args.command == "status":
        coordination_info = CoordinationInfoFactory(
            yt_client=yt.YtClient(config=yt.default_config.get_config_from_env()),
            coordinator_path=YtPath(f"{args.workdir}/coordinator"),
        ).get()
        if not coordination_info:
            print("Ray cluster not found.")
            return
        status: OperationState = yt_client.get_operation_state(
            coordination_info.operation_id,
        )
        if not status.is_running():
            print("Ray cluster is not running.")
            return
        ray_info = RayInfo(
            coordination_info=coordination_info,
            yt_client=yt_client,
            transformer=AriadneTransformer.create(yt_client),
        )
        print(f"Ray operation: {ray_info.operation_url}\n")
        print(ray_info.dashboard_instruction)
        print(ray_info.cli_instruction)
        print(ray_info.client_instruction)
    elif args.command == "stop":
        coordination_info = CoordinationInfoFactory(
            yt_client=yt.YtClient(config=yt.default_config.get_config_from_env()),
            coordinator_path=YtPath(f"{args.workdir}/coordinator"),
        ).get()
        if not coordination_info:
            print("Ray cluster not found.")
            return
        operation_status: OperationState = yt_client.get_operation_state(
            coordination_info.operation_id
        )
        if not operation_status.is_running():
            print("Ray cluster is not running.")
            return
        yt_client.abort_operation(coordination_info.operation_id)
        print(
            f"Ray cluster stopped, operation {coordination_info.operation_url} has been aborted."
        )


if __name__ == "__main__":
    main()
