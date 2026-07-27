# TaskFlow Bot 🤖

A Telegram bot for personal task management, built with an asynchronous (async) architecture designed for scalability. It includes an admin permission system, persistent data storage using SQLAlchemy, and centralized error handling.

## ✨ Features

- Add, view, complete, and delete tasks through an interactive conversation flow using FSM.
- Set priorities for tasks (Low / Medium / High).
- Inline and Reply keyboards for a smooth user experience.
- Admin permission system:
  - Global statistics.
  - Broadcast messages with preview and confirmation before sending.
- Persistent data storage using SQLAlchemy (SQLite by default, easily switchable to PostgreSQL/MySQL by changing the database URL).
- Custom middlewares:
  - User-based rate limiting.
  - Automatic database session injection and new user registration.
- Centralized error handling with logging to both file and console.
- Flexible configuration using environment variables (`.env`).

## 🛠️ Technologies

| Technology | Usage |
|---|---|
| Python 3.12 | Core programming language |
| aiogram 3 | Asynchronous Telegram Bot framework |
| SQLAlchemy 2.0 (Async) | ORM for database operations |
| SQLite / aiosqlite | Default lightweight database |
| python-dotenv | Environment variables management |

## 📁 Project Structure


telegram-taskflow-bot/
├── bot/
│ ├── config.py # Load configuration from .env
│ ├── models.py # SQLAlchemy database models
│ ├── database.py # Database access layer
│ ├── keyboards.py # Telegram keyboards
│ ├── states.py # FSM states
│ ├── logging_config.py # Logging configuration
│ ├── handlers/
│ │ ├── start.py # Start and help commands
│ │ ├── tasks.py # Task management handlers
│ │ ├── admin.py # Admin control panel
│ │ └── errors.py # Error handling
│ └── middlewares/
│ ├── db.py # Database injection middleware
│ └── throttling.py # Rate limiting middleware
├── main.py
├── requirements.txt
├── .env.example
└── .gitignore


## 🚀 Installation & Setup

```bash
git clone https://github.com/FouadWre-Dev/taskflow-telegram-bot.git

cd telegram-taskflow-bot

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

Create a .env file from .env.example and configure your settings:

BOT_TOKEN=your_bot_token
ADMIN_IDS=your_telegram_id
DATABASE_URL=sqlite+aiosqlite:///taskflow.db
MAX_TASKS_PER_USER=50
RATE_LIMIT_SECONDS=0.7
LOG_LEVEL=INFO

Run the bot:

python main.py
📸 Screenshots

💼 What This Project Demonstrates

This project demonstrates the ability to:

Build asynchronous applications using Python async/await.
Design a clean and scalable layered architecture:
Handlers
Database layer
Middlewares
Configuration management
Work with modern ORM solutions using SQLAlchemy 2.0 Async.
Implement FSM workflows and middleware patterns.
Handle errors, logging, and rate limiting in a production-oriented way.
Build maintainable Telegram bots using real-world development practices.
📄 License

MIT License