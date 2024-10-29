from loader import bot
from telebot.types import Message
from states.state_user import UserStates
from keyboards.inline.choice_action import choice_button, search_menu, rating_vuln
from api import api_nvd
from loguru import logger
from utils.set_bot_commands import (
    save_db_history,
    save_db_history_callback,
    parsing_result_single_reqeust,
    parsing_result_list_reqeust,
    parsing_result_list_reqeust_callback_query,
)

logger.add("bot.log", rotation="1 MB", level="INFO", format="{time} {level} {message}")


@bot.callback_query_handler(
    func=lambda callback_query: callback_query.data == "search_vuln"
)
def search_vuln(callback_query):
    """
    Функция реализует меню выбора вариантов поиска и переходит
    в статут выбранного варианта
    :param callback_query: значение выбранное в базовом меню
    """

    bot.send_message(
        chat_id=callback_query.message.chat.id,
        text="Выберите параметры поиска:",
        reply_markup=search_menu(),
    )

    bot.set_state(
        callback_query.from_user.id,
        UserStates.search_vuln,
        callback_query.message.chat.id,
    )


@bot.callback_query_handler(
    func=lambda callback_query: callback_query.data == "search_vuln_id"
)
def search_vuln_id(callback_query):
    """
    Функция реализует интерфейс ввода
    данных для поиска по id уязвимости
    :param callback_query: значение выбранное в меню поиска
    """
    bot.send_message(
        chat_id=callback_query.message.chat.id,
        text="Введите id уязвимости:",
    )

    bot.set_state(
        callback_query.from_user.id,
        UserStates.search_vuln_nvd_id,
        callback_query.message.chat.id,
    )


@bot.message_handler(state=UserStates.search_vuln_nvd_id)
def get_search_id(message: Message):
    """
    Функция реализует запрос по api для поиска по id уязвимости
    Выводит полученный данные в чат по результатам парсинга данных
    :param message: чат
    """

    result_request = api_nvd.get_vuln_id(message.text)

    logger.info(
        f"Пользователь: {message.from_user.username} "
        f"искал уязвимость (ID: {message.text})"
    )

    save_db_history(message=message)
    logger.info(
        f"Запрос записан в бд для пользователя: {message.from_user.username}"
        f"Запрос({message.text})"
    )

    parsing_result_single_reqeust(
        result_request=result_request, message=message, bot=bot
    )

    # Возвращаем к базовому состоянию

    bot.send_message(
        message.from_user.id, f"Что хотите сделать", reply_markup=choice_button()
    )

    bot.set_state(message.from_user.id, UserStates.base)


@bot.callback_query_handler(
    func=lambda callback_query: callback_query.data == "search_vuln_rating"
)
def search_vuln_rating(callback_query):
    """
    Функция реализует интерфейс выбора вариантов
    выбора поиска по рейтингу уязвимости
    :param callback_query: значение выбранное в меню поиска
    """

    bot.send_message(
        chat_id=callback_query.message.chat.id,
        text="Выберите интересующий рейтинг:",
        reply_markup=rating_vuln(),
    )

    bot.set_state(
        callback_query.from_user.id,
        UserStates.search_vuln_nvd_rating,
        callback_query.message.chat.id,
    )


@bot.callback_query_handler(
    func=lambda callback_query: callback_query.data in ["LOW", "MEDIUM", "HARD"]
)
def get_search_rating(callback_query):
    """
    Функция реализует запрос по api для поиска по выбранному рейтингу
    выводит полученный данные в чат по результатам парсинга данных
    :param callback_query: значение выбранное на этапе выбора рейтинга
    """

    logger.info(
        f"Пользователь: {callback_query.from_user.username} "
        f"искал уязвимость по рейтингу (Rating: {callback_query.data})"
    )
    result_request = api_nvd.get_vuln_rating(callback_query.data)

    save_db_history_callback(callback_query=callback_query)

    logger.info(
        f"Запрос записан в бд для пользователя: {callback_query.from_user.username}"
        f"Запрос({callback_query.data})"
    )

    parsing_result_list_reqeust_callback_query(
        result_request=result_request, callback_query=callback_query, bot=bot
    )

    # Возвращаем к базовому состоянию

    bot.send_message(
        callback_query.from_user.id, "Что хотите сделать?", reply_markup=choice_button()
    )

    bot.set_state(callback_query.from_user.id, UserStates.base)


@bot.callback_query_handler(
    func=lambda callback_query: callback_query.data == "search_vuln_key_word"
)
def search_vuln_key_word(callback_query):
    """
    Функция реализует интерфейс выбора вариантов
    выбора поиска по ключевому слову
    :param callback_query: значение выбранное в меню поиска
    """

    bot.send_message(
        chat_id=callback_query.message.chat.id,
        text="Введите ключевое слово:",
    )

    bot.set_state(
        callback_query.from_user.id,
        UserStates.search_vuln_nvd_key,
        callback_query.message.chat.id,
    )


@bot.message_handler(state=UserStates.search_vuln_nvd_key)
def get_search_key(message: Message):
    """
    Функция реализует запрос по api для поиска по ключевому слову
    выводит полученный данные в чат по результатам парсинга данных
    :param message: чат хранит ключевое слово пользователя
    """
    result_request = api_nvd.get_vuln_keyword(message.text)

    logger.info(
        f"Пользователь: {message.from_user.username} "
        f"искал уязвимость по ключевому слову (KeyWord: {message.text})"
    )

    save_db_history(message=message)

    logger.info(
        f"Запрос записан в бд для пользователя: {message.from_user.username}"
        f"Запрос({message.text})"
    )

    parsing_result_list_reqeust(result_request=result_request, message=message, bot=bot)

    # Возвращаем к базовому состоянию

    bot.send_message(
        message.from_user.id, f"Что хотите сделать", reply_markup=choice_button()
    )

    bot.set_state(message.from_user.id, UserStates.base)


@bot.callback_query_handler(
    func=lambda callback_query: callback_query.data == "search_vuln_top5"
)
def get_top_5_vuln(callback_query):
    """
    Функция реализует запрос по api для поиска топ 5 уязвимостей за последний месяц
    выводит полученный данные в чат по результатам парсинга данных
    :param callback_query: значение выбранное в меню поиска
    """
    result_request = api_nvd.get_vuln_first_5()

    logger.info(
        f"Пользователь: {callback_query.from_user.username} " f"Искал топ 5 уязвимостей"
    )

    save_db_history_callback(callback_query=callback_query)

    logger.info(
        f"Запрос записан в бд для пользователя: {callback_query.from_user.username}"
    )

    parsing_result_list_reqeust_callback_query(
        result_request=result_request, callback_query=callback_query, bot=bot
    )

    bot.send_message(
        callback_query.from_user.id, "Что хотите сделать?", reply_markup=choice_button()
    )

    bot.set_state(callback_query.from_user.id, UserStates.base)


@bot.callback_query_handler(
    func=lambda callback_query: callback_query.data == "search_vuln_oval_mitre"
)
def get_oval_mitre(callback_query):
    """
    Функция реализует запрос по api для поиска oval Mitre
    выводит полученный данные в чат по результатам парсинга данных
    :param callback_query: значение выбранное в меню поиска
    """

    result_request = api_nvd.get_vuln_oval_mitre()

    logger.info(
        f"Пользователь: {callback_query.from_user.username} " f"Искал OVAl MITRE"
    )

    save_db_history_callback(callback_query=callback_query)

    logger.info(
        f"Запрос записан в бд для пользователя: {callback_query.from_user.username}"
    )
    parsing_result_list_reqeust_callback_query(
        result_request=result_request, callback_query=callback_query, bot=bot
    )

    bot.send_message(
        callback_query.from_user.id, "Что хотите сделать?", reply_markup=choice_button()
    )

    bot.set_state(callback_query.from_user.id, UserStates.base)
