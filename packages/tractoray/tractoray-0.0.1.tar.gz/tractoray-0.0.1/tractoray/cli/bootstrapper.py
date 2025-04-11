import argparse
import logging
import os

from tractoray.internal.bootstrap import (
    BootstrapperHead,
    BootstrapperNode,
)
from tractoray.internal.logs import setup_logging
from tractoray.ytpath import YtPath


_LOGGER = logging.getLogger(__name__)


def main() -> None:
    setup_logging()
    _LOGGER.info("Starting bootstrapper")
    parser = argparse.ArgumentParser(description="Bootstrap Ray in YT operation")
    subparsers = parser.add_subparsers(dest="command", required=True)

    head_parser = subparsers.add_parser("head", help="Run head node")
    node_parser = subparsers.add_parser("node", help="Run worker node")

    for subparser in (head_parser, node_parser):
        subparser.add_argument(
            "--workdir",
            required=True,
            type=str,
            help="Working directory path in YT",
        )
        subparser.add_argument(
            "--proxy",
            required=True,
            type=str,
            help="YT proxy URL",
        )
        subparser.add_argument(
            "--cpu-limit",
            required=True,
            type=int,
            help="CPU limit per node",
        )
        subparser.add_argument(
            "--node-count",
            required=True,
            type=int,
            help="Number of nodes in cluster",
        )

    args = parser.parse_args()
    if args.command == "head":
        BootstrapperHead(
            yt_proxy=args.proxy,
            yt_token=os.environ["YT_SECURE_VAULT_USER_YT_TOKEN"],
            workdir=YtPath(args.workdir),
            cpu_limit=args.cpu_limit,
            node_count=args.node_count,
            node_index=int(os.environ["YT_JOB_COOKIE"]),
            operation_id=os.environ["YT_OPERATION_ID"],
            job_id=os.environ["YT_JOB_ID"],
            head_port=int(os.environ["YT_PORT_0"]),
            dashboard_port=int(os.environ["YT_PORT_1"]),
            dashboard_agent_listen_port=int(os.environ["YT_PORT_2"]),
            public_dashboard_port=int(os.environ["YT_PORT_3"]),
            client_port=int(os.environ["YT_PORT_4"]),
            runtime_env_agent_port=int(os.environ["YT_PORT_5"]),
        ).run()
    else:
        BootstrapperNode(
            yt_proxy=args.proxy,
            yt_token=os.environ["YT_SECURE_VAULT_USER_YT_TOKEN"],
            workdir=YtPath(args.workdir),
            cpu_limit=args.cpu_limit,
            node_count=args.node_count,
            node_index=int(os.environ["YT_JOB_COOKIE"]) + 1,
            operation_id=os.environ["YT_OPERATION_ID"],
            job_id=os.environ["YT_JOB_ID"],
            runtime_env_agent_port=int(os.environ["YT_PORT_0"]),
        ).run()


if __name__ == "__main__":
    main()
