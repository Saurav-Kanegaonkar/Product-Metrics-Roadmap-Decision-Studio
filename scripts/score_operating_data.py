import csv
from collections import defaultdict

scores = defaultdict(list)
value = defaultdict(float)
failures = defaultdict(float)

with open("data/daily_metrics.csv", newline="") as f:
    for row in csv.DictReader(f):
        scores[row["entity_id"]].append(float(row["priority_score"]))

with open("data/recommended_actions.csv", newline="") as f:
    for row in csv.DictReader(f):
        value[row["entity_id"]] += float(row["expected_value_or_cost_avoidance"])

with open("data/data_quality_checks.csv", newline="") as f:
    for row in csv.DictReader(f):
        failures[row["source_system"]] += float(row["failed_records"])

ranked = []
for entity_id, values in scores.items():
    ranked.append((sum(values) / len(values) + value[entity_id] / 50000, entity_id, value[entity_id]))

print("Top priorities")
for score, entity_id, action_value in sorted(ranked, reverse=True)[:10]:
    print(f"{entity_id}: score={score:.1f}, action_value=$" + format(action_value, ",.0f"))

print("\nSource quality hotspots")
for system, failed in sorted(failures.items(), key=lambda item: item[1], reverse=True)[:5]:
    print(f"{system}: failed_records=" + format(failed, ",.0f"))
