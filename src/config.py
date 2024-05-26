from pathlib import Path

from environs import Env

env = Env()
env.read_env()

BASE_DIR = Path(__file__).parent.parent

class Settings:
    DB_CONFIG = env(
        "DB_CONFIG",
        "postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}".format(
            DB_USER=env("DATABASE_USER", None),
            DB_PASSWORD=env("DATABASE_PASS", None),
            DB_HOST=env("DATABASE_HOST", None),
            DB_NAME=env("DATABASE_NAME", None),
        ),
    )
    CERT_PATH = env("CERT_PATH")
    PRIVATE_KEY_PATH: Path = Path(BASE_DIR / "src" / "certs" / "private.pem")
    PUBLIC_KEY_PATH: Path = Path(BASE_DIR / "src" / "certs" / "public.pem")

    JWT_ALGORITHM: str = env("JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = env("ACCESS_TOKEN_EXPIRE_MINUTES")

    MEDIA_ROOT: str = env("MEDIA_ROOT")
    BUCKET_NAME: str = env("BUCKET_NAME")
    AWS_ACCESS_TOKEN: str = env("AWS_ACCESS_TOKEN")
    AWS_SECRET_KEY: str = env("AWS_SECRET_KEY")

settings = Settings
