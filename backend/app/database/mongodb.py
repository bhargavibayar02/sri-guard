# mongodb.py
# Sets up the connection to MongoDB and exposes each "collection"
# (a collection in MongoDB is like a table in a normal SQL database).

from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

# Create the MongoDB client using our connection string
client = AsyncIOMotorClient(settings.MONGO_URI)

# Select the database by name
db = client[settings.DB_NAME]

# Expose each collection so other files can import them directly
users_collection = db["users"]
employees_collection = db["employees"]
logs_collection = db["logs"]
incidents_collection = db["incidents"]
alerts_collection = db["alerts"]