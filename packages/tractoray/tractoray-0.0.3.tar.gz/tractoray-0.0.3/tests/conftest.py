import os
from typing import Generator

import pytest

from tests.utils import get_random_string
from tests.yt_instances import (
    YtInstance,
    YtInstanceExternal,
    YtInstanceTestContainers,
)
from tractoray.ytpath import YtPath


@pytest.fixture(scope="session")
def yt_instance() -> Generator[YtInstance, None, None]:
    yt_mode = os.environ.get("YT_MODE", "testcontainers")
    if yt_mode == "testcontainers":
        with YtInstanceTestContainers() as yt_instance:
            yield yt_instance
    elif yt_mode == "external":
        proxy_url = os.environ["YT_PROXY"]
        yt_token = os.environ.get("YT_TOKEN")
        assert yt_token is not None
        yield YtInstanceExternal(proxy_url=proxy_url, token=yt_token)
    else:
        raise ValueError(f"Unknown yt_mode: {yt_mode}")


@pytest.fixture(scope="session")
def yt_base_dir(yt_instance: YtInstance) -> YtPath:
    yt_client = yt_instance.get_client()

    path = f"//tmp/tractoray_tests/run_{get_random_string(4)}"
    yt_client.create("map_node", path, recursive=True)
    return YtPath(path)


@pytest.fixture(scope="function")
def yt_path(yt_instance: YtInstance, yt_base_dir: YtPath) -> YtPath:
    yt_client = yt_instance.get_client()
    path = f"{yt_base_dir}/{get_random_string(8)}"
    yt_client.create("map_node", path)
    return YtPath(path)
