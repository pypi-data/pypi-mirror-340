from setuptools import setup, find_packages

setup(
    name="tgBotGen",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "tg-bot-init=tgBotGen.scaffold:run_scaffold",
        ],
    },
    install_requires=[
        "aiogram==3.3.0",
        "SQLAlchemy==2.0.40",
        "python-dotenv==0.9.0",
        "APScheduler==3.11.0"
    ],
    author="Александр Аваков",
    description="Генератор структуры проекта для Telegram-бота",
    python_requires=">=3.8",
)
