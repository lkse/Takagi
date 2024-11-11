import logging
import os
from rich.logging import RichHandler
from .config import config 

if os.path.exists("{config.LOGGING_FOLDER}/{config.LOGGING_FILE}"):
    os.remove("{config.LOGGING_FOLDER}/{config.LOGGING_FILE}")

logging.basicConfig(
    level=config.LOGGING_LEVEL,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[
        RichHandler(markup=True, rich_tracebacks=True),
        logging.FileHandler(f"{config.LOGGING_FOLDER}/{config.LOGGING_FILE}", encoding="utf-8")
    ]
)

async def init():
    global log 
    try:
        log = logging.getLogger("rich")
    except Exception as e:
        print(f"Error In Logging Init: {e}")
        return 0
    
    log.info(f"[blink yellow]Logging started[/blink yellow]")
    log.info(f"[bold cyan1]Logging Level: [/bold cyan1][bold bright_magenta]{config.LOGGING_LEVEL}[bold bright_magenta]")
    log.info(f"[bold cyan2]Logging Path: [/bold cyan2][bold bright_magenta]{config.LOGGING_FOLDER}{config.LOGGING_FILE}[bold bright_magenta]")
    return 1 
