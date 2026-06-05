import pandas as pd
import numpy as np

# mao hasnt run yet when we assing map it just gives back something like iterator or hash or object or where it is stored i dont
# know what to calll that was why i used all that the only time it runs is when list is used on filtereed records so as to show us what we will see

raw_records = [
    {"id": 1, "name": "  alice johnson ", "department": "engineering", "salary": 85000},
    {"id": 2, "name": "BOB SMITH", "department": "Marketing", "salary": 120000},
    {"id": 3, "name": "  carol white", "department": "engineering", "salary": 54000},
    {"id": 4, "name": "david brown  ", "department": "HR", "salary": 43000},
    {"id": 5, "name": "EVE DAVIS", "department": "marketing", "salary": 97000},
    {"id": 6, "name": "  frank miller ", "department": "Engineering", "salary": 61000},
    {"id": 7, "name": "grace lee", "department": "hr", "salary": 38000},
    {"id": 8, "name": "HENRY WILSON", "department": "engineering", "salary": 72000},
]


def clean_record(record):
    clean_name = record["name"].strip().title()
    clean_department = record["department"].lower()

    return {
        "id": record["id"],
        "name": clean_name,
        "department": clean_department,
        "salary": record["salary"],
    }

cleaned_records = map(clean_record, raw_records)

filtered_records = filter(lambda x: x["department"] == "engineering" or x["department"] == "marketing", cleaned_records)

final_records = list(filtered_records)

df = pd.DataFrame(final_records)

df["name_upper"] = df["name"].str.upper()
df["salary_band"] = np.where(df["salary"] >= 70000, "senior","junior")
df["department_display"] = df["department"].str.title()

print(df)




