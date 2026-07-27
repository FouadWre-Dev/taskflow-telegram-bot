from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from bot.keyboards import main_menu_keyboard

router = Router(name="start")

WELCOME_TEXT = (
    "أهلاً بك في TaskFlow 👋\n\n"
    "بوت بسيط لإدارة مهامك اليومية مباشرة من تيليجرام.\n"
    "استخدم الأزرار بالأسفل أو الأوامر التالية:\n\n"
    "/add - إضافة مهمة جديدة\n"
    "/tasks - عرض المهام النشطة\n"
    "/stats - إحصائياتك الشخصية\n"
    "/help - عرض هذه الرسالة"
)


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(WELCOME_TEXT, reply_markup=main_menu_keyboard())


@router.message(Command("help"))
@router.message(F.text == "ℹ️ مساعدة")
async def cmd_help(message: Message) -> None:
    await message.answer(WELCOME_TEXT, reply_markup=main_menu_keyboard())
