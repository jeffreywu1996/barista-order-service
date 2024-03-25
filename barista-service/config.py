import os

from dotenv import load_dotenv
from pydantic import ConfigDict

load_dotenv()


class GlobalConfig(ConfigDict):
    title: str = "Barista Worker"
    version: str = "1.0.0"
    debug: bool = os.environ.get("DEBUG")

    rabbitmq_server: str = os.environ.get("RABBITMQ_SERVER", 'rabbitmq')



settings = GlobalConfig()
