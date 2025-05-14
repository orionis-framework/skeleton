from orionis.luminate.services.environment.env import Env, env
from orionis.luminate.config.contracts.config import IConfig
from orionis.luminate.config.app import App
from orionis.luminate.config.app.enums.environments import Environments
from orionis.luminate.config.app.enums.ciphers import Cipher
from orionis.luminate.config.auth import Auth

__all__ = [
    "Env",
    "env",
    "App",
    "IConfig",
    "Environments",
    "Cipher",
    "Auth",
]

__description__ = (
    "This configuration module adopts an approach inspired by modern frameworks, "
    "managing the initialization and bootstrapping of the application. It allows the definition of essential parameters "
    "and services through configuration files, streamlining the loading and organization of options into the service container. "
    "This enables a flexible, secure, and environment-adaptable bootstrap process."
)