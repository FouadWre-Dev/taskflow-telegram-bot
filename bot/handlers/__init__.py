from aiogram import Router

from bot.handlers import admin, errors, start, tasks


def setup_routers() -> Router:
    root = Router()
    root.include_router(start.router)
    root.include_router(tasks.router)
    root.include_router(admin.router)
    root.include_router(errors.router)
    return root
