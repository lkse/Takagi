from app import logger, discord, config
import asyncio
from rich.traceback import install
install(show_locals=True)

async def init():
    if not await logger.init(): # log init failed
        raise SystemExit(211)
    await discord.init()
    
async def shutdown():
    await discord.shutdown()
    await config.database.disconnect()
        
if __name__ == "__main__":
    try:
        asyncio.run(init())
    except Exception as e:
        print(f"Error In Main: {e}")
        raise SystemExit(42069)

    except KeyboardInterrupt:
        asyncio.run_until_complete(shutdown())
    
    finally:
        print("Exiting")
        raise SystemExit(0)

