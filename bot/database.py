from contextlib import asynccontextmanager
from datetime import datetime

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from bot.models import Base, Task, TaskPriority, User


class Database:
    def __init__(self, url: str):
        self._engine = create_async_engine(url, echo=False)
        self._session_factory = async_sessionmaker(
            self._engine, expire_on_commit=False, class_=AsyncSession
        )

    async def init_models(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @asynccontextmanager
    async def session(self):
        async with self._session_factory() as session:
            yield session

    async def get_or_create_user(self, user_id: int, full_name: str, username: str | None) -> User:
        async with self.session() as session:
            user = await session.get(User, user_id)
            if user is None:
                user = User(id=user_id, full_name=full_name, username=username)
                session.add(user)
                await session.commit()
                await session.refresh(user)
            elif user.username != username or user.full_name != full_name:
                user.username = username
                user.full_name = full_name
                await session.commit()
            return user

    async def count_active_tasks(self, user_id: int) -> int:
        async with self.session() as session:
            stmt = select(func.count(Task.id)).where(
                Task.user_id == user_id, Task.is_done.is_(False)
            )
            result = await session.execute(stmt)
            return result.scalar_one()

    async def add_task(
        self, user_id: int, title: str, description: str | None, priority: TaskPriority
    ) -> Task:
        async with self.session() as session:
            task = Task(
                user_id=user_id, title=title, description=description, priority=priority
            )
            session.add(task)
            await session.commit()
            await session.refresh(task)
            return task

    async def list_tasks(self, user_id: int, include_done: bool = False) -> list[Task]:
        async with self.session() as session:
            stmt = select(Task).where(Task.user_id == user_id)
            if not include_done:
                stmt = stmt.where(Task.is_done.is_(False))
            stmt = stmt.order_by(Task.priority.desc(), Task.created_at.asc())
            result = await session.execute(stmt)
            return list(result.scalars().all())

    async def get_task(self, task_id: int, user_id: int) -> Task | None:
        async with self.session() as session:
            stmt = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    async def mark_done(self, task_id: int, user_id: int) -> bool:
        async with self.session() as session:
            stmt = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            result = await session.execute(stmt)
            task = result.scalar_one_or_none()
            if task is None:
                return False
            task.is_done = True
            task.completed_at = datetime.utcnow()
            await session.commit()
            return True

    async def delete_task(self, task_id: int, user_id: int) -> bool:
        async with self.session() as session:
            stmt = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            result = await session.execute(stmt)
            task = result.scalar_one_or_none()
            if task is None:
                return False
            await session.delete(task)
            await session.commit()
            return True

    async def global_stats(self) -> dict:
        async with self.session() as session:
            total_users = await session.scalar(select(func.count(User.id)))
            total_tasks = await session.scalar(select(func.count(Task.id)))
            done_tasks = await session.scalar(
                select(func.count(Task.id)).where(Task.is_done.is_(True))
            )
            return {
                "total_users": total_users or 0,
                "total_tasks": total_tasks or 0,
                "done_tasks": done_tasks or 0,
            }

    async def all_user_ids(self) -> list[int]:
        async with self.session() as session:
            result = await session.execute(select(User.id).where(User.is_blocked.is_(False)))
            return list(result.scalars().all())
