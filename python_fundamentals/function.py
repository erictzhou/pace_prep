jobs = [
    ("agent-a", 100),
    ("agent-b", 250),
    ("agent-c", 400)
]

def calculate_cost(duration_ms, *, rate=0.02, minimum=1.0):
    if rate * duration_ms > minimum:
        return rate * duration_ms
    return minimum

for job in jobs:
    print(calculate_cost(job[1]))
for job in jobs:
    print(calculate_cost(job[1], rate=100, minimum=90))

def add_job(job_id, queue=None, *, priority=0):
    if queue is None:
        queue = []
    queue.append((priority, job_id))
    return queue

q1 = add_job("agent-a")
q2 = add_job("agent-b")

print(q1)
# [(0, "agent-a")]

print(q2)
# [(0, "agent-b")]

q3 = []
add_job("agent-c", q3, priority=5)
add_job("agent-d", q3, priority=2)

print(q3)
# [(5, "agent-c"), (2, "agent-d")]

def bad_add_job(job_id, queue=[]):
    queue.append(job_id)
    return queue

print(bad_add_job("a"))
print(bad_add_job("b"))

# Its bad because queue is reused. in this case its fine but if bad_add_job 
# wanted a diff queue it would be bad right


records = [
    {"agent": "alpha", "duration": 100, "status": "ok"},
    {"agent": "beta", "duration": 250, "status": "failed"},
    {"agent": "alpha", "duration": 200, "status": "ok"},
    {"agent": "gamma", "duration": 150, "status": "ok"},
    {"agent": "beta", "duration": 50, "status": "ok"}
]

def summarize(*records, include_failed=False, min_duration=0):
    total_durations = {}
    for record in records:
        if record["duration"] >= min_duration:
            if not include_failed and record["status"] != "ok":
                continue
            total_durations[record["agent"]] = \
                total_durations.get(record["agent"], 0) + record["duration"]
    
    return total_durations

print(summarize(*records, include_failed = False, min_duration=0))