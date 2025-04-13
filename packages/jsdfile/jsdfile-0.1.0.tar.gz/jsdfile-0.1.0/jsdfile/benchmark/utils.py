import os
import shutil
from pathlib import Path

import msgspec
import pandas as pd

from jsdfile.benchmark.config import generate_test_data
from jsdfile.core.main import JSD


class BenchmarkResults:
    """Class to store and process benchmark results."""

    def __init__(self):
        self.results = []

    def add_result(
        self,
        size,
        operation,
        jsd_time,
        orjson_time,
        msgspec_time,
        jsd_mem,
        orjson_mem,
        msgspec_mem,
        jsd_size,
        json_size,
    ):
        """Add a benchmark result to the collection."""
        jsd_orjson_ratio = (jsd_time / orjson_time) * 100 if orjson_time > 0 else 0
        jsd_msgspec_ratio = (jsd_time / msgspec_time) * 100 if msgspec_time > 0 else 0

        self.results.append(
            {
                "size": size,
                "operation": operation,
                "jsd_time": jsd_time,
                "orjson_time": orjson_time,
                "msgspec_time": msgspec_time,
                "jsd_orjson_ratio": jsd_orjson_ratio,
                "jsd_msgspec_ratio": jsd_msgspec_ratio,
                "jsd_size": jsd_size,
                "json_size": json_size,
                "jsd_mem": jsd_mem,
                "orjson_mem": orjson_mem,
                "msgspec_mem": msgspec_mem,
            }
        )

    def to_dataframe(self):
        """Convert results to a pandas DataFrame."""
        return pd.DataFrame(self.results)


def warmup(orjson=None):
    """Perform a warmup run to mitigate cold-start effects."""
    warmup_data = generate_test_data(100)
    tmp = Path("./benchmark_tmp")
    tmp.mkdir(exist_ok=True)

    # Warmup for JSD
    warm_jsd_path = tmp / "warm_jsd.jsdfile"
    jsd_file = JSD(warm_jsd_path)
    jsd_file.write(warmup_data)
    _ = jsd_file.read()

    # Warmup for orjson
    warm_json_path = tmp / "warm_json.json"
    with open(warm_json_path, "wb") as f:
        f.write(orjson.dumps(warmup_data))
    with open(warm_json_path, "rb") as f:
        _ = orjson.loads(f.read())

    # Warmup for msgspec
    warm_msgspec_path = tmp / "warm_msgspec.msgspec"
    msgspec_encoder = msgspec.json.Encoder()
    msgspec_decoder = msgspec.json.Decoder()
    try:
        encoded = msgspec_encoder.encode(warmup_data)
        with open(warm_msgspec_path, "wb") as f:
            f.write(encoded)
        with open(warm_msgspec_path, "rb") as f:
            _ = msgspec_decoder.decode(f.read())
    except Exception as e:
        print("Warmup msgspec error:", e)

    shutil.rmtree(tmp)


def get_file_size(path):
    """Get file size in human-readable format."""
    size_bytes = os.path.getsize(path)
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024.0 or unit == "GB":
            break
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} {unit}"
