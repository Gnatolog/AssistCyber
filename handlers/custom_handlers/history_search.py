from telebot.types import Message
from loader import bot
from keyboards.inline.choice_action import choice_button, search_menu
from database.db_code import User, SearchHistory
from loguru import logger

logger.add("bot.log", rotation="1 MB", level="INFO", format="{time} {level} {message}")


@bot.callback_query_handler(
    func=lambda callback_query: callback_query.data == "history"
)
def get_history_search(callback_query):

    logger.info(
        f"Пользователь: {callback_query.from_user.username} запрашивал историю поиска "
    )

    search_history = (
        SearchHistory.select()
        .where(SearchHistory.user_id == callback_query.from_user.id)
        .order_by(SearchHistory.due_date.desc())
    )

    if search_history:
        history_text = "История ваших запросов:\n"
        for record in search_history:
            history_text += f"Запрос: {record}\n"
    else:
        history_text = "У вас нет истории запросов."

    bot.send_message(
        chat_id=callback_query.message.chat.id,
        text=history_text,
    )

    bot.send_message(
        callback_query.from_user.id, f"Что хотите сделать", reply_markup=choice_button()
    )


@bot.message_handler(commands=["history"])
def get_history_search(message: Message):

    logger.info(f"Пользователь: {message.from_user.username} запрашивал историю поиска")
    search_history = (
        SearchHistory.select()
        .where(SearchHistory.user_id == message.from_user.id)
        .order_by(SearchHistory.due_date.desc())
    )

    if search_history:
        history_text = "История ваших запросов:\n"
        for record in search_history:
            history_text += f"Запрос: {record}\n"
    else:
        history_text = "У вас нет истории запросов."

    bot.send_message(
        chat_id=message.chat.id,
        text=history_text,
    )

    bot.send_message(
        message.from_user.id, f"Что хотите сделать", reply_markup=choice_button()
    )
