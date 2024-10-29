import os
from dotenv import load_dotenv, find_dotenv


if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY_NVD = os.getenv("API_KEY_NVD")
DB_PATH = "database/database.db"  # путь к БД
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"  # формат записи поискового запроса в бд

DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("history", "История поиска"),
    ("help", "Вывести справку"),
)
