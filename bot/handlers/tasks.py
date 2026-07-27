from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.config import BotConfig
from bot.database import Database
from bot.keyboards import main_menu_keyboard, priority_keyboard, task_actions_keyboard
from bot.models import Task, TaskPriority
from bot.states import AddTaskStates

router = Router(name="tasks")

PRIORITY_LABELS = {
    TaskPriority.LOW: "🟢 منخفضة",
    TaskPriority.MEDIUM: "🟡 متوسطة",
    TaskPriority.HIGH: "🔴 عالية",
}


def _format_task(task: Task) -> str:
    lines = [f"#{task.id} — {task.title}", f"الأولوية: {PRIORITY_LABELS[task.priority]}"]
    if task.description:
        lines.append(f"التفاصيل: {task.description}")
    return "\n".join(lines)


@router.message(Command("add"))
@router.message(F.text == "➕ إضافة مهمة")
async def start_add_task(message: Message, state: FSMContext, db: Database, config: BotConfig) -> None:
    active_count = await db.count_active_tasks(message.from_user.id)
    if active_count >= config.max_tasks_per_user:
        await message.answer(
            f"لقد وصلت للحد الأقصى ({config.max_tasks_per_user}) من المهام النشطة. "
            "أنهِ بعض المهام أولاً."
        )
        return

    await state.set_state(AddTaskStates.waiting_title)
    await message.answer("اكتب عنوان المهمة:")


@router.message(AddTaskStates.waiting_title)
async def receive_title(message: Message, state: FSMContext) -> None:
    title = (message.text or "").strip()
    if not title or len(title) > 256:
        await message.answer("عنوان غير صالح. حاول مرة أخرى بعنوان أقصر من 256 حرف.")
        return

    await state.update_data(title=title)
    await state.set_state(AddTaskStates.waiting_description)
    await message.answer("أضف وصفاً اختيارياً للمهمة، أو أرسل /skip لتخطي هذه الخطوة.")


@router.message(AddTaskStates.waiting_description, Command("skip"))
@router.message(AddTaskStates.waiting_description)
async def receive_description(message: Message, state: FSMContext) -> None:
    description = None if message.text == "/skip" else (message.text or "").strip()
    await state.update_data(description=description)
    await state.set_state(AddTaskStates.waiting_priority)
    await message.answer("اختر أولوية المهمة:", reply_markup=priority_keyboard())


@router.callback_query(AddTaskStates.waiting_priority, F.data.startswith("priority:"))
async def receive_priority(callback: CallbackQuery, state: FSMContext, db: Database) -> None:
    priority_value = callback.data.split(":", 1)[1]
    priority = TaskPriority(priority_value)

    data = await state.get_data()
    task = await db.add_task(
        user_id=callback.from_user.id,
        title=data["title"],
        description=data.get("description"),
        priority=priority,
    )
    await state.clear()

    await callback.message.edit_text(f"تمت إضافة المهمة بنجاح ✅\n\n{_format_task(task)}")
    await callback.answer()


@router.message(Command("tasks"))
@router.message(F.text == "📋 مهامي")
async def list_tasks(message: Message, db: Database) -> None:
    tasks = await db.list_tasks(message.from_user.id)
    if not tasks:
        await message.answer("لا توجد لديك مهام نشطة حالياً 🎉", reply_markup=main_menu_keyboard())
        return

    for task in tasks:
        await message.answer(_format_task(task), reply_markup=task_actions_keyboard(task))


@router.callback_query(F.data.startswith("task:done:"))
async def mark_task_done(callback: CallbackQuery, db: Database) -> None:
    task_id = int(callback.data.split(":")[2])
    success = await db.mark_done(task_id, callback.from_user.id)

    if success:
        await callback.message.edit_text(f"{callback.message.text}\n\n✅ تم إنهاء المهمة")
    else:
        await callback.answer("لم يتم العثور على المهمة", show_alert=True)
        return
    await callback.answer()


@router.callback_query(F.data.startswith("task:delete:"))
async def delete_task(callback: CallbackQuery, db: Database) -> None:
    task_id = int(callback.data.split(":")[2])
    success = await db.delete_task(task_id, callback.from_user.id)

    if success:
        await callback.message.edit_text(f"{callback.message.text}\n\n🗑 تم حذف المهمة")
    else:
        await callback.answer("لم يتم العثور على المهمة", show_alert=True)
        return
    await callback.answer()


@router.message(Command("stats"))
@router.message(F.text == "📊 إحصائياتي")
async def user_stats(message: Message, db: Database) -> None:
    active = await db.list_tasks(message.from_user.id, include_done=False)
    all_tasks = await db.list_tasks(message.from_user.id, include_done=True)
    done = len(all_tasks) - len(active)

    await message.answer(
        f"📊 إحصائياتك:\n\n"
        f"المهام النشطة: {len(active)}\n"
        f"المهام المنجزة: {done}\n"
        f"إجمالي المهام: {len(all_tasks)}"
    )
