

jobs = [
    ("job-c", 45),
    ("job-a", 20),
    ("job-b", 80),
    ("job-d", 20),
    ("job-e", 60)
]

under_50 = [job for job in jobs if job[1] < 50]

sort_list = sorted(under_50, key = lambda x: (x[1], x[0]))

print([job[0] for job in sort_list])

agents = [
    {"name": "alpha", "tasks": 8, "failures": 2},
    {"name": "beta", "tasks": 12, "failures": 1},
    {"name": "gamma", "tasks": 12, "failures": 3},
    {"name": "delta", "tasks": 8, "failures": 1},
    {"name": "epsilon", "tasks": 12, "failures": 1}
]

sorted_agents = sorted(agents, key=lambda x: (-x["tasks"], x["failures"], x["name"]))

print([row["name"] for row in sorted_agents])


events = [
    ("agent-a", "tool", 120),
    ("agent-b", "llm", 400),
    ("agent-a", "llm", 300),
    ("agent-c", "tool", 100),
    ("agent-b", "tool", 150),
    ("agent-a", "tool", 80),
    ("agent-c", "llm", 500),
    ("agent-b", "tool", 50),
    ("agent-c", "tool", 100),
    ("agent-d", "llm", 200)
]


totals = {}

for name, type, duration in events:
    if (type == "tool"):
        totals[name] = totals.get(name, 0) + duration

ls_agents = list(totals.items())

ls_agents.sort(key = lambda x: (-x[1], x[0]))
print(ls_agents[0])
print(ls_agents[1])



