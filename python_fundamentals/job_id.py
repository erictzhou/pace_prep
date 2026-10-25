jobs = ["A123", "B789", "C123", "C123"]

id_to_count = {}
for j in jobs:
    if j in id_to_count:
        id_to_count[j] += 1
    else:
        id_to_count[j] = 1

unique_job_id = set(id_to_count)
print(id_to_count)
print(unique_job_id)


# Challenge 1 — Frequency analysis
jobs = ["A", "B", "A", "C", "B", "A"]

counts = {}
for j in jobs:
    counts[j] = counts.get(j, 0) + 1

print(min(counts.items(), key = lambda kv: (-kv[1], kv[0])))


# Challenge 2 — Job execution telemetry
events = [
    ("A", "start", 10),
    ("B", "start", 12),
    ("A", "finish", 18),
    ("B", "finish", 20),
    ("C", "start", 22),
]

durations = {}
buffer = {}

for i, (job, kind, t) in enumerate(events):
    if job in durations:
        print(f"ERROR: duplicate jobID {job} index: {i}")
    elif job not in buffer:
        if kind == "start":
            buffer[job] = t
        else:
            print(f"ERROR: finish without start {job} index: {i}")
    else:
        if kind == "start":
            print(f"ERROR: double start {job} index: {i}")
        else:
            durations[job] = t - buffer[job]

for job in buffer:
    if job not in durations:
        print(f"NOTICE: unfinished job {job}")

print(durations)

# Challenge 3 — GPU resource accounting

events = [
    ("A", "start", 2),
    ("B", "start", 3),
    ("A", "finish", 2),
    ("C", "start", 4),
    ("B", "finish", 3),
]

max_gpu = 0
cur_gpu = 0

executing = {}
executed = set()
for i, (job, action, count) in enumerate(events):
    if job in executed:
        print(f"ERROR: duplicate job ID {job} index: {i}")
    if job not in executing:
        if action == "finish":
            print(f"ERROR: finish before start {job} index: {i}")
        else:
            executing[job] = count
            cur_gpu += count
            max_gpu = max(cur_gpu, max_gpu)
           # print(f"max: {max_gpu} action: {action}")
    else:
        if action == "start":
            print(f"ERROR: double start {job} index: {i}")   
        else:
            if count != executing[job]:
                print(f"ERROR: deallocation mismatch {job} index: {i}") 
                break
            else:
                cur_gpu -= count
                del executing[job]
                executed.add(job)

print(max_gpu)

                
