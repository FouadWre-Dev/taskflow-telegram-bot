from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

from bot.models import Task


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ إضافة مهمة"), KeyboardButton(text="📋 مهامي")],
            [KeyboardButton(text="📊 إحصائياتي"), KeyboardButton(text="ℹ️ مساعدة")],
        ],
        resize_keyboard=True,
    )


def priority_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🟢 منخفضة", callback_data="priority:low"),
                InlineKeyboardButton(text="🟡 متوسطة", callback_data="priority:medium"),
                InlineKeyboardButton(text="🔴 عالية", callback_data="priority:high"),
            ]
        ]
    )


def task_actions_keyboard(task: Task) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ إنهاء", callback_data=f"task:done:{task.id}"),
                InlineKeyboardButton(text="🗑 حذف", callback_data=f"task:delete:{task.id}"),
            ]
        ]
    )


def confirm_broadcast_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ تأكيد الإرسال", callback_data="broadcast:confirm"),
                InlineKeyboardButton(text="❌ إلغاء", callback_data="broadcast:cancel"),
            ]
        ]
    )
