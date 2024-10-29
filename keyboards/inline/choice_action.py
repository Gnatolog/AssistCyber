from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def choice_button():
    """
    Функция реализует inline кнопки основного меню
    :return: клавиатуру с кнопками

    """
    button_1 = InlineKeyboardButton(
        text="Поиск уязвимостей", callback_data="search_vuln"
    )

    button_2 = InlineKeyboardButton(text="История запросов", callback_data="history")

    keyboard = InlineKeyboardMarkup()
    keyboard.add(button_1, button_2)
    return keyboard


def search_menu():
    """
    Функция реализует inline кнопки меню выбора вариантов поиска
    :return: клавиатуру с кнопками

    """
    button_1 = InlineKeyboardButton(text="Поиск по id", callback_data="search_vuln_id")

    button_2 = InlineKeyboardButton(
        text="Поиск по rating", callback_data="search_vuln_rating"
    )

    button_3 = InlineKeyboardButton(
        text="Поиск по ключевому слову", callback_data="search_vuln_key_word"
    )

    button_4 = InlineKeyboardButton(text="ТОП 5", callback_data="search_vuln_top5")

    button_5 = InlineKeyboardButton(
        text="Oval Mitre", callback_data="search_vuln_oval_mitre"
    )

    keyboard = InlineKeyboardMarkup()
    keyboard.add(button_1, button_2, button_3, button_4, button_5)
    return keyboard


def rating_vuln():
    """
    Функция реализует inline кнопки меню выбора вариантов поиска по рейтингу
    :return: клавиатуру с кнопками

    """

    button_1 = InlineKeyboardButton(text="LOW", callback_data="LOW")

    button_2 = InlineKeyboardButton(text="MEDIUM", callback_data="MEDIUM")

    button_3 = InlineKeyboardButton(text="HARD", callback_data="HARD")

    keyboard = InlineKeyboardMarkup()
    keyboard.add(button_1, button_2, button_3)

    return keyboard
