from dataclasses import dataclass
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("MYGEMS_APP_NAME", "MYGEMS")
    db_host: str = os.getenv("MYGEMS_DB_HOST", "localhost")
    db_port: int = int(os.getenv("MYGEMS_DB_PORT", "5432"))
    db_name: str = os.getenv("MYGEMS_DB_NAME", "mygems")
    db_user: str = os.getenv("MYGEMS_DB_USER", "myuser")
    db_password: str = os.getenv("MYGEMS_DB_PASSWORD", "")


settings = Settings()
