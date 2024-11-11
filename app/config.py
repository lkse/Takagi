from dotenv import dotenv_values
import databases

values = dotenv_values()
class Config:
    def __init__(self) -> None:
        self.__dict__.update(values)
    
config = Config()

database = databases.Database(f'mysql://{config.DB_USER}:{config.DB_PASS}@{config.DB_HOST}/{config.DB_NAME}')
