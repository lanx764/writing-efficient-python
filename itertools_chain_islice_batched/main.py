# i couldnt re use the all records becuase when i used slice it took 5 rows away from all_records the thing is
# i can still use it to batch but the result won be accurate because 5 rows have been removed already


import itertools

africa_records = [
    {"id": 1, "region": "africa", "currency": "NGN", "amount": 15000},
    {"id": 2, "region": "africa", "currency": "KES", "amount": 8200},
    {"id": 3, "region": "africa", "currency": "ZAR", "amount": 3300},
]

europe_records = [
    {"id": 4, "region": "europe", "currency": "GBP", "amount": 750},
    {"id": 5, "region": "europe", "currency": "EUR", "amount": 420},
    {"id": 6, "region": "europe", "currency": "CHF", "amount": 990},
]

americas_records = [
    {"id": 7, "region": "americas", "currency": "USD", "amount": 500},
    {"id": 8, "region": "americas", "currency": "CAD", "amount": 310},
    {"id": 9, "region": "americas", "currency": "USD", "amount": 880},
]

all_records = itertools.chain(africa_records,europe_records,americas_records)

for record in itertools.islice(all_records, 5):
    print(record)

all_records_fresh = itertools.chain(africa_records,europe_records,americas_records)

for i, batch in enumerate(itertools.batched(all_records_fresh, 3),1):
    print(f"batch {i} : {batch}")
