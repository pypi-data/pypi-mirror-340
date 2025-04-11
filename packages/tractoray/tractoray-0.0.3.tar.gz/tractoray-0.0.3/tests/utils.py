from pathlib import Path
import random
import string
import time


def get_data_path(filename: str | Path) -> Path:
    return (Path(__file__).parent / "data" / filename).resolve()


def get_random_string(length: int) -> str:
    return (
        str(int(time.time()))
        + "_"
        + "".join(random.choice(string.ascii_letters) for _ in range(length))
    )
