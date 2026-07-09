# seed_data.py
# Loads employees.csv and employee_logs.csv from the dataset/ folder
# into MongoDB. Run this ONCE after generating the dataset.
#
# Command: python seed/seed_data.py   (from inside backend/)

import asyncio
import sys
import os
import csv

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.database.mongodb import employees_collection, logs_collection

DATASET_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "dataset")
EMPLOYEES_CSV = os.path.join(DATASET_DIR, "employees.csv")
LOGS_CSV = os.path.join(DATASET_DIR, "employee_logs.csv")


def str_to_bool(value: str) -> bool:
    return str(value).strip().lower() in ["true", "1", "yes"]


async def seed():
    # --- Seed Employees ---
    await employees_collection.delete_many({})  # clear old data first
    employees = []
    with open(EMPLOYEES_CSV, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["risk_score"] = 0.0
            row["risk_level"] = "Safe"
            employees.append(row)
    if employees:
        await employees_collection.insert_many(employees)
    print(f"Seeded {len(employees)} employees into MongoDB.")

    # --- Seed Logs ---
    await logs_collection.delete_many({})  # clear old data first
    logs = []
    with open(LOGS_CSV, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["failed_logins"] = int(row["failed_logins"])
            row["files_downloaded"] = int(row["files_downloaded"])
            row["usb_connected"] = str_to_bool(row["usb_connected"])
            row["admin_access"] = str_to_bool(row["admin_access"])
            row["risk_score"] = None
            row["risk_reasons"] = []
            row["mitre_tags"] = []
            logs.append(row)
    if logs:
        await logs_collection.insert_many(logs)
    print(f"Seeded {len(logs)} log entries into MongoDB.")


if __name__ == "__main__":
    asyncio.run(seed())