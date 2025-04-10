import os
from pathlib import Path


def create_file(path: Path, content: str = ''):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(content, encoding='utf-8')


def run_scaffold():
    base = Path.cwd()

    files = {
        ".env": "",
        ".env.local": "",
        ".gitignore": """.idea/
__pycache__/
.venv/
.qodo/
*.sqlite3
.env.local
""",
        "README.md": "",
        "config.py": '''import os

from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Загрузка переменных окружения
if os.path.exists(os.path.join(BASE_DIR, '.env.local')):
    load_dotenv(os.path.join(BASE_DIR, '.env.local'))
else:
    load_dotenv(os.path.join(BASE_DIR, '.env'))

    
class Config:
    BOT_TOKEN = os.getenv('BOT_TOKEN')
''',
        "main.py": '''import asyncio
import logging

from bot.handler import main


if __name__ == '__main__':
    try:
        logging.basicConfig(level=logging.DEBUG)
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
''',
        "bot/handler.py": '''import asyncio
import re
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, FSInputFile
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger

from config import Config
from bot import keyboards as kb

dp = Dispatcher()
bot = Bot(token=Config.BOT_TOKEN)


async def main():
    await dp.start_polling(bot)
''',
        "bot/keyboards.py": '''from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton''',
        "db/models.py": '''from sqlalchemy import String, Float, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession

engine = create_async_engine(url='sqlite+aiosqlite:///db/database/products.sqlite3')
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass

    
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
''',
        "db/requests.py": '''from typing import Optional

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
# from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete

from db.models import async_session
''',
        "db/database/.gitignore": "*.sqlite3",
        "keys/.gitignore": "*.*"
    }

    dirs = ["static/"]

    for path_str, content in files.items():
        create_file(base / path_str, content)

    for dir_str in dirs:
        (base / dir_str).mkdir(parents=True, exist_ok=True)

    print("✅ Структура проекта успешно создана.")
