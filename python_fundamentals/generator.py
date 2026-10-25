def slow_jobs(lines, threshold_ms):
    for line in lines:
        parts = line.strip().split(",")

        if len(parts) != 3:
            continue

        elif parts[1] == "DONE":
            try:
                duration = int(parts[2])
            except ValueError:
                continue

            if duration >= threshold_ms:
                yield (parts[0], duration)