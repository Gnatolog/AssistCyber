from telebot.types import Message
from peewee import IntegrityError
from states.state_user import UserStates
from keyboards.inline.choice_action import choice_button
from loader import bot
from database.db_code import User
from loguru import logger

logger.add("bot.log", rotation="1 MB", level="INFO", format="{time} {level} {message}")


@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    logger.info(f"Команда '/start' от пользователя: {username} (ID: {user_id})")
    try:
        User.create(user_id=user_id, username=username)
        logger.info(f"Новый пользователь добавлен: {username} (ID: {user_id})")
        bot.reply_to(
            message,
            f"Привет {message.from_user.full_name}, "
            f"я бот ассистент в мире кибербеза !",
        )
        bot.set_state(message.chat.id, UserStates.base)
        send_base_message(message)  # Вызов функции для отправки базового сообщения

    except IntegrityError:
        bot.reply_to(message, f"Рад вас снова видеть, {username}!")
        bot.set_state(message.from_user.id, UserStates.base)
        send_base_message(message)


def send_base_message(message: Message):
    bot.send_message(
        message.from_user.id,
        "Вы находитесь в основном  меню!",
        reply_markup=choice_button(),
    )
