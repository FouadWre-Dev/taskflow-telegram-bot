import asyncio
import logging

from aiogram import Router, F
from aiogram.exceptions import TelegramForbiddenError, TelegramRetryAfter
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.config import BotConfig
from bot.database import Database
from bot.keyboards import confirm_broadcast_keyboard
from bot.states import BroadcastStates

router = Router(name="admin")
logger = logging.getLogger(__name__)


class IsAdmin:
    def __init__(self, config: BotConfig):
        self._admin_ids = set(config.admin_ids)

    def __call__(self, message: Message) -> bool:
        return message.from_user.id in self._admin_ids


@router.message(Command("adminstats"))
async def admin_stats(message: Message, db: Database, config: BotConfig) -> None:
    if message.from_user.id not in config.admin_ids:
        return

    stats = await db.global_stats()
    await message.answer(
        "📈 إحصائيات عامة:\n\n"
        f"عدد المستخدمين: {stats['total_users']}\n"
        f"إجمالي المهام: {stats['total_tasks']}\n"
        f"المهام المنجزة: {stats['done_tasks']}"
    )


@router.message(Command("broadcast"))
async def start_broadcast(message: Message, state: FSMContext, config: BotConfig) -> None:
    if message.from_user.id not in config.admin_ids:
        return

    await state.set_state(BroadcastStates.waiting_message)
    await message.answer("أرسل الرسالة التي تريد بثها لجميع المستخدمين:")


@router.message(BroadcastStates.waiting_message)
async def preview_broadcast(message: Message, state: FSMContext) -> None:
    await state.update_data(text=message.text)
    await state.set_state(BroadcastStates.waiting_confirmation)
    await message.answer(
        f"معاينة الرسالة:\n\n{message.text}\n\nهل تريد المتابعة؟",
        reply_markup=confirm_broadcast_keyboard(),
    )


@router.callback_query(BroadcastStates.waiting_confirmation, F.data == "broadcast:cancel")
async def cancel_broadcast(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text("تم إلغاء البث.")
    await callback.answer()


@router.callback_query(BroadcastStates.waiting_confirmation, F.data == "broadcast:confirm")
async def confirm_broadcast(callback: CallbackQuery, state: FSMContext, db: Database) -> None:
    data = await state.get_data()
    text = data["text"]
    await state.clear()

    user_ids = await db.all_user_ids()
    sent, failed = 0, 0

    await callback.message.edit_text(f"جاري إرسال الرسالة إلى {len(user_ids)} مستخدم...")

    for user_id in user_ids:
        try:
            await callback.bot.send_message(user_id, text)
            sent += 1
        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after)
            failed += 1
        except TelegramForbiddenError:
            failed += 1
        except Exception:
            logger.exception("Failed to send broadcast message to %s", user_id)
            failed += 1
        await asyncio.sleep(0.05)

    await callback.message.answer(f"اكتمل البث ✅\nتم الإرسال: {sent}\nفشل: {failed}")
    await callback.answer()
