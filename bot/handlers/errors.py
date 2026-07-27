import logging

from aiogram import Router
from aiogram.types import ErrorEvent

router = Router(name="errors")
logger = logging.getLogger(__name__)


@router.error()
async def handle_errors(event: ErrorEvent) -> None:
    logger.exception(
        "Update caused an exception: %s", event.exception, exc_info=event.exception
    )

    update = event.update
    chat = None
    if update.message:
        chat = update.message.chat
    elif update.callback_query and update.callback_query.message:
        chat = update.callback_query.message.chat

    if chat is not None:
        try:
            await event.update.bot.send_message(
                chat.id, "حدث خطأ غير متوقع، تم تسجيله وسيتم إصلاحه قريباً."
            )
        except Exception:
            logger.exception("Failed to notify user about the error")
