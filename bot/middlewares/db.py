from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from bot.database import Database


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, db: Database):
        self._db = db

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        data["db"] = self._db

        user = data.get("event_from_user")
        if user is not None and not user.is_bot:
            await self._db.get_or_create_user(
                user_id=user.id,
                full_name=user.full_name,
                username=user.username,
            )

        return await handler(event, data)
