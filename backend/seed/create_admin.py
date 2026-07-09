# create_admin.py
# Run this ONCE to create a test SOC Analyst login.
# Command: python seed/create_admin.py

import asyncio
import sys
import os

# Allow this script to import from the 'app' package
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.database.mongodb import users_collection
from app.core.security import hash_password


async def create_admin():
    existing = await users_collection.find_one({"username": "admin"})
    if existing:
        print("Admin user already exists. Skipping.")
        return

    admin_user = {
        "username": "admin",
        "hashed_password": hash_password("admin123"),  # change this password later!
        "role": "SOC Analyst"
    }
    await users_collection.insert_one(admin_user)
    print("Admin user created successfully.")
    print("Username: admin")
    print("Password: admin123")


if __name__ == "__main__":
    asyncio.run(create_admin())