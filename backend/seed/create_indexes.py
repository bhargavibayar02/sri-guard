# create_indexes.py
# Creates MongoDB indexes on frequently-queried fields to speed up
# lookups, filters, and sorts. Run this ONCE after seeding data.
#
# Command: python seed/create_indexes.py   (from inside backend/)

import asyncio
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.database.mongodb import employees_collection, logs_collection


async def create_indexes():
    # --- Employees collection ---

    # unique=True means MongoDB will REJECT two employees with the same
    # employee_id -- this protects our data from accidental duplicates.
    await employees_collection.create_index("employee_id", unique=True)
    print("Created unique index on employees.employee_id")

    # Index on department -- speeds up the department filter dropdown
    await employees_collection.create_index("department")
    print("Created index on employees.department")

    # Index on risk_level -- speeds up dashboard count queries
    # (e.g. count_documents({"risk_level": "Critical"}))
    await employees_collection.create_index("risk_level")
    print("Created index on employees.risk_level")

    # --- Logs collection ---

    # Index on employee_id -- speeds up "get all logs for this employee"
    await logs_collection.create_index("employee_id")
    print("Created index on logs.employee_id")

    # Index on login_time, DESCENDING (-1) -- speeds up sorting logs
    # by most-recent-first, which is what our /logs/ endpoint always does
    await logs_collection.create_index([("login_time", -1)])
    print("Created index on logs.login_time (descending)")

    # Index on risk_score -- speeds up the "recent alerts" query
    # that filters logs where risk_score >= 71
    await logs_collection.create_index("risk_score")
    print("Created index on logs.risk_score")

    print("\nAll indexes created successfully!")


if __name__ == "__main__":
    asyncio.run(create_indexes())