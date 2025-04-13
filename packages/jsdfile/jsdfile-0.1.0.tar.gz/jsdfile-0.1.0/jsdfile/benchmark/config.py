import random
from tqdm import tqdm
import string
import uuid
import base64


def generate_test_data(num_records=1000):
    """Generate random test data with nested structures."""
    data = {}
    for i in tqdm(range(num_records), desc="Generating dataset"):
        key = f"item_{i}"
        data[key] = {
            "id": i,
            "name": "".join(random.choices(string.ascii_letters, k=10)),
            "value": random.random() * 1000,
            "active": random.choice([True, False]),
            "tags": [
                random.choice(["tag1", "tag2", "tag3", "tag4", "tag5"])
                for _ in range(random.randint(1, 5))
            ],
            "metadata": {
                "created": random.randint(1600000000, 1700000000),
                "modified": random.randint(1600000000, 1700000000),
                "version": f"{random.randint(1, 5)}.{random.randint(0, 9)}",
                "priority": random.choice(["low", "medium", "high"]),
                "nested": {
                    "depth1": random.randint(1, 100),
                    "depth2": {"value": random.random() * 100},
                },
            },
        }
    return data


def generate_large_dataset(size=1000):
    dataset = []
    for i in tqdm(range(size), desc="Generating data"):
        record = {
            "id": i,
            "uuid": str(uuid.uuid4()),  # Unique identifier
            "secondary_uuid": str(uuid.uuid4()),  # Extra UUID for complexity
            "value": f"record_{i}",
            "number": i
            * random.uniform(1.1, 5.0),  # Large range for floating-point numbers
            "big_text": " ".join(
                [f"word_{random.randint(0, 1000)}" for _ in range(100)]
            ),  # Large text block
            "binary_data": base64.b64encode(f"binary_{i}".encode()).decode("utf-8")
            if i % 500 == 0
            else "no_binary",
            "nested": {
                "level1": {
                    "level2": {
                        "level3": {
                            "level4": {
                                "level5": {
                                    "level6": {
                                        "list_data": [
                                            random.randint(1, 100) for _ in range(50)
                                        ],  # 50 random numbers
                                        "deep_text": f"deep_record_{i}",
                                        "bool_flag": i % 2
                                        == 0,  # Alternating True/False
                                        "deep_nested": {
                                            "array": [
                                                {
                                                    "key": f"sub_{j}",
                                                    "value": j
                                                    * random.uniform(0.5, 2.5),
                                                    "inner_binary": base64.b64encode(
                                                        f"inner_binary_{j}".encode()
                                                    ).decode("utf-8"),
                                                }
                                                for j in range(10)
                                            ],
                                            "mega_list": [
                                                {
                                                    "id": str(uuid.uuid4()),
                                                    "value": f"mega_{k}",
                                                    "extra_data": [
                                                        random.random()
                                                        for _ in range(20)
                                                    ],  # 20 floats
                                                }
                                                for k in range(10)
                                            ],
                                        },
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "tags": [
                f"tag_{j}" for j in range(random.randint(5, 20))
            ],  # Random number of tags
            "meta_info": {
                "source": "generated",
                "timestamp": random.randint(
                    1609459200, 1672531199
                ),  # Random UNIX timestamp (2021-2023)
                "flag": bool(random.getrandbits(1)),
            },
        }
        dataset.append(record)

    return dataset
