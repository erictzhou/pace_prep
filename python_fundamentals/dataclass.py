from __future__ import annotations
from dataclasses import dataclass, field

import copy

# Implement Metric here

@dataclass(frozen=True)
class Metric:
    name: str  
    timestamp: float
    value: float

    def __post_init__(self):
        if self.name == "" or self.name.strip() == "":
            raise ValueError
        if self.timestamp < 0:
            raise ValueError
        if self.value < 0:
            raise ValueError

    def is_above(self, threshold: float) -> bool:
        return self.value > threshold


m = Metric("gpu_memory_mb", 10.5, 8192.0)

print(m.name)
# gpu_memory_mb

print(m.is_above(4096))
# True

print(m.is_above(8192))
# False

try:
    Metric("   ", 10.0, 100.0)
except ValueError:
    print("Invalid metric name")

try:
    m.value = 100.0
except Exception:
    print("Metric is immutable")


@dataclass
class AgentTelemetry:
    agent_id: str
    metrics: list[Metric] = field(default_factory=list)

    # Implement the five methods
    def add_metric(self, metric: Metric) -> None:
        self.metrics.append(metric)

    def latest(self, name: str) -> Metric | None:
        only_name = [val for val in self.metrics if val.name == name]
        if not only_name:
            return None
        return max(reversed(only_name), key = lambda metric: metric.timestamp)
    
    def average(self, name: str) -> float | None:
        matching = [metric.value for metric in self.metrics if metric.name == name]
        if not matching:
            return None
        return sum(matching) / len(matching)

    def filter_above(self, name: str, threshold: float) -> list[Metric]:
        matching = [metric for metric in self.metrics if m.name == name and metric.value > threshold]
        ret = sorted(matching, key = lambda x: x.timestamp)
        return ret

    def merge(self, other: AgentTelemetry) -> None:
        if other.agent_id != self.agent_id:
            raise ValueError
        for m in other.metrics:
            self.metrics.append(copy.deepcopy(m))


a = AgentTelemetry("agent-1")
b = AgentTelemetry("agent-1")

a.add_metric(Metric("cpu", 1.0, 40.0))
a.add_metric(Metric("cpu", 3.0, 80.0))
a.add_metric(Metric("memory", 2.0, 200.0))

b.add_metric(Metric("cpu", 2.0, 60.0))
b.add_metric(Metric("cpu", 3.0, 90.0))

a.merge(b)

print(a.latest("cpu").value)
# 90.0

print(a.average("cpu"))
# 67.5

print([m.value for m in a.filter_above("cpu", 50)])
# [60.0, 80.0, 90.0]

print(a.latest("gpu"))
# None

c = AgentTelemetry("agent-2")

try:
    a.merge(c)
except ValueError:
    print("Cannot merge different agents")
