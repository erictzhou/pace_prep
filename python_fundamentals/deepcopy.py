import copy
base_config = {
    "gpu": {
        "count": 2,
        "memory_gb": 24
    },
    "training": {
        "batch_size": 32,
        "epochs": 10
    },
    "tags": ["baseline"]
}

def create_job_config(base, job_name, gpu_count):
    new_config = copy.deepcopy(base)
    new_config["gpu"]["count"] = gpu_count
    new_config["tags"].append(job_name)
    return new_config

job_a = create_job_config(base_config, "job-a", 4)
job_b = create_job_config(base_config, "job-b", 8)

job_a["training"]["batch_size"] = 128
job_a["tags"].append("high-priority")

assert base_config["gpu"]["count"] == 2
assert base_config["tags"] == ["baseline"]

assert job_a["gpu"]["count"] == 4
assert job_b["gpu"]["count"] == 8

assert job_b["training"]["batch_size"] == 32
assert job_b["tags"] == ["baseline", "job-b"]

print("All tests passed!")