def parse_telemetry(lines: list[str]) -> tuple[dict[str, float], int]:
    errors = 0
    agent_to_util = {}
    for line in lines:
        values = [val.strip() for val in line.split(",")]

        if len(values) != 2:
            errors += 1
            continue

        try:
            util = float(values[1])
        except ValueError:
            errors += 1
            continue
        
        if util < 0 or util > 100 or \
        values[0] == "":
            errors += 1
            continue

        agent_to_util[values[0]] = util
    return (agent_to_util, errors)

logs = [
    "agent-a,75.5",
    "agent-b,abc",
    "agent-c,102",
    "agent-a,80",
    "invalid",
    "agent-d,45",
    "  ,50",
    "agent-e,0"
]

result, errors = parse_telemetry(logs)

print(result)
# {
#     "agent-a": 80.0,
#     "agent-d": 45.0,
#     "agent-e": 0.0
# }

print(errors)
# 4