import os
import asyncio
import motor.motor_asyncio
from dotenv import load_dotenv
load_dotenv()

client = motor.motor_asyncio.AsyncIOMotorClient(
    os.getenv("MONGODB_URL"),
    serverSelectionTimeoutMS=1000,
)
client.get_io_loop = asyncio.get_event_loop

db = client.discord_bot_data