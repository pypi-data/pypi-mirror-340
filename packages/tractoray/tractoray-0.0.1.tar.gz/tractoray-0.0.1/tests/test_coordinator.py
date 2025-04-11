from tests.yt_instances import YtInstance
from tractoray.internal.coordinator import (
    HeadCoordinatorFactory,
    WorkerCoordinatorFactory,
)
from tractoray.ytpath import YtPath


def test_coordinator(yt_instance: YtInstance, yt_path: YtPath) -> None:
    coordinator_path = YtPath(f"{yt_path}/coordinator")
    hf = HeadCoordinatorFactory(
        self_endpoint="head.local",
        node_index=0,
        node_count=2,
        coordinator_path=coordinator_path,
        yt_client=yt_instance.get_client(),
        operation_id="000000-0000-0000-000000000000",
        wait_barrier=False,
        head_port=12345,
        public_dashboard_port=12346,
        client_port=12347,
    )
    c = hf.make()
    print(c)
    wf = WorkerCoordinatorFactory(
        self_endpoint="worker.local",
        node_index=1,
        node_count=2,
        coordinator_path=coordinator_path,
        yt_client=yt_instance.get_client(),
        operation_id="000000-0000-0000-000000000000",
        wait_barrier=True,
    )
    c = wf.make()
    print(c)


# def test_ray(yt_instance: YtInstance, yt_path: YtPath) -> None:
#     yt_client = yt_instance.get_client()
#     task_spec = yt.VanillaSpecBuilder().begin_task("docker_build")
#     task_spec.command(bootstrapper)
#     task_spec.environment(
#         {"YT_ALLOW_HTTP_REQUESTS_TO_YT_FROM_JOB": "1", "PYTHONDONTWRITEBYTECODE": "1"},
#     )
#     task_spec.job_count(2)
#     task_spec.docker_image(
#         "cr.eu-north1.nebius.cloud/e00faee7vas5hpsh3s/chiffa/tractorun-ray-tests:2025-03-07-01-05-14-2a80510f5"
#     )
#     task_spec.cpu_limit(100)
#     task_spec.port_count(4)
#     task_spec.memory_limit(32 * 1024 * 1024 * 1024)
#     operation_spec = task_spec.end_task()
#     operation_spec.title("ray")
#     operation_spec.secure_vault(
#         {
#             "YT_TOKEN": yt_client.config["token"],
#         },
#     )
#     operation_spec.pool_trees(["gpu_h200"])
#
#     yt.run_operation(operation_spec)
