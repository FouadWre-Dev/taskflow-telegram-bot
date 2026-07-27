import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()


def _parse_admin_ids(raw: str) -> list[int]:
    if not raw:
        return []
    return [int(x.strip()) for x in raw.split(",") if x.strip().isdigit()]


@dataclass(frozen=True)
class BotConfig:
    token: str
    admin_ids: list[int] = field(default_factory=list)
    database_url: str = "sqlite+aiosqlite:///taskflow.db"
    max_tasks_per_user: int = 50
    rate_limit_seconds: float = 0.7
    log_level: str = "INFO"


def load_config() -> BotConfig:
    token =  os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN is not set. Check your .env file.")

    return BotConfig(
        token=token,
        admin_ids=_parse_admin_ids(os.getenv("ADMIN_IDS", "")),
        database_url=os.getenv("DATABASE_URL", "sqlite+aiosqlite:///taskflow.db"),
        max_tasks_per_user=int(os.getenv("MAX_TASKS_PER_USER", 50)),
        rate_limit_seconds=float(os.getenv("RATE_LIMIT_SECONDS", 0.7)),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
    )
