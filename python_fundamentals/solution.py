from pathlib import Path
import csv
import math
import json

def process_telemetry(
    config_path: Path,
    telemetry_path: Path,
    output_path: Path
) -> dict:
    try:
        with open(config_path, 'r', encoding="utf-8") as config:
            data = json.load(config)
    except OSError as exc:
        raise RuntimeError("Configuration unavailable") from exc
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid configuration") from exc

    # Check if data is a dict and if key exists
    if not isinstance(data, dict):
        raise ValueError("Invalid configuration")
    threshold = data.get("gpu_threshold")
    if threshold is None:
        raise ValueError("Invalid configuration")

    # Value checks
    if (
        isinstance(threshold, bool)
        or not isinstance(threshold, (int, float))
        or not math.isfinite(threshold)
        or not (0 <= threshold <= 100)
    ):
        raise ValueError("Invalid configuration")

    try:
        with open(telemetry_path, 'r', encoding="utf-8", newline="") as telemetry:
            reader = csv.reader(telemetry)
            # Header check
            header = next(reader) 
            if (len(header) != 2
                or header[0] != "agent_id" 
                or header[1] != "gpu_utilization"):
                raise ValueError("Invalid telemetry schema")
        
            total_records = 0
            valid_records = 0
            high_gpu_agents = []
            for row in reader:
                total_records += 1
                if (len(row) != 2):
                    continue
        
                try:
                    true_util = float(row[1])
                except ValueError:
                    continue
        
                if true_util < 0 or true_util > 100:
                    continue
        
                if not row[0].strip() or not math.isfinite(true_util):
                    continue
        
                if true_util > threshold:
                    high_gpu_agents.append(row[0])
                valid_records += 1
        
            invalid_records = total_records - valid_records
        
            ret = {}
        
            ret["total_records"] = total_records
            ret["valid_records"] = valid_records
            ret["invalid_records"] = invalid_records
            ret["high_gpu_agents"] = high_gpu_agents
            
    except StopIteration:
        raise ValueError("Invalid telemetry schema")
    except OSError as exc:
        raise RuntimeError("Telemetry unavailable") from exc


    # 'w' opens the file for writing (overwrites existing contents)
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(ret, file)
    return ret
