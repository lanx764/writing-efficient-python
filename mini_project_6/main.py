import cProfile
import time
import random
import pstats

def fetch_records():
    records = []
    for i in range(10000):
        records.append({"id": i, "value": random.randint(1, 1000)})
    return records

def validate_records(records):
    valid = []
    for record in records:
        if record["value"] > 0:
            valid.append(record)
    return valid

def transform_records(records):
    transformed = []
    for record in records:
        time.sleep(0.0001)
        transformed.append({"id": record["id"], "value": record["value"] * 2})
    return transformed

def summarise_records(records):
    total = sum(r["value"] for r in records)
    return {"total": total, "count": len(records)}

def run_pipeline():
    records = fetch_records()
    valid = validate_records(records)
    transformed = transform_records(valid)
    summary = summarise_records(transformed)
    return summary

cProfile.run("run_pipeline()")

profiler = cProfile.Profile()
profiler.enable()

run_pipeline()

profiler.disable()

stats = pstats.Stats(profiler)
stats.sort_stats('cumtime')
stats.print_stats(10)

# transform_records is the bottleneck, not run_pipeline, and time.sleep called 10, 000 # times is the specific cause


