import asyncio
from bot import Bot

async def start_bot():
    print("Starting Bot...")
    await Bot().start()
    # This keeps the bot alive
    await asyncio.Event().wait()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bot())
