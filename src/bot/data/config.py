from dataclasses import dataclass

from environs import Env


@dataclass
class BotConfig:
    TOKEN: str


@dataclass
class MySQLConfig:
    HOST: str
    PORT: int
    USER: str
    PASSWORD: str
    DATABASE: str


@dataclass
class Config:
    bot: BotConfig
    mysql: MySQLConfig


def load_config() -> Config:
    env = Env()
    env.read_env()

    return Config(
        bot=BotConfig(
            TOKEN=env.str("TG_BOT_TOKEN"),
        ),
        mysql=MySQLConfig(
            HOST=env.str("HOST"),
            PORT=env.int("PORT"),
            USER=env.str("USER"),
            PASSWORD=env.str("PASSWORD"),
            DATABASE=env.str("DATABASE"),
        ),
    )
