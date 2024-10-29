from telebot.types import BotCommand, Message
from config_data.config import DEFAULT_COMMANDS
from database.db_code import SearchHistory
from datetime import datetime, timedelta


def set_default_commands(bot):
    bot.set_my_commands([BotCommand(*i) for i in DEFAULT_COMMANDS])


def save_db_history(message: Message):
    """
    Функция для занесения истории поиска в бд через message
    и контроль количества записей для одного пользователя не более 6
    с заменой новыми запросами на более старый с сортировкой по дате и времени
    запроса
    :param message: запрос пользователя

    """
    search_history = SearchHistory.select().where(
        SearchHistory.user_id == message.from_user.id
    )

    if len(search_history) <= 5:
        SearchHistory.create(
            title=message.text,
            user=message.from_user.id,
            due_date=datetime.now(),
        )

    else:

        search_history.get().delete_instance()

        SearchHistory.create(
            title=message.text,
            user=message.from_user.id,
            due_date=datetime.now(),
        )


def save_db_history_callback(callback_query):
    """
    Функция для занесения истории поиска в бд через выбор пользователя по кнопке
    и контроль количества записей для одного пользователя не более 6
    с заменой новыми запросами на более старый с сортировкой по дате и времени
    запроса
    :param callback_query: значение выбранной пользователем кнопки

    """

    search_history = SearchHistory.select().where(
        SearchHistory.user_id == callback_query.from_user.id
    )
    if len(search_history) <= 5:

        SearchHistory.create(
            title=callback_query.data,
            user=callback_query.from_user.id,
            due_date=datetime.now(),
        )

    else:

        search_history.get().delete_instance()
        SearchHistory.create(
            title=callback_query.data,
            user=callback_query.from_user.id,
            due_date=datetime.now(),
        )


def parsing_result_single_reqeust(result_request: dict, message: Message, bot):
    """
    Функция парсит данные полученный при ответе от API в одиночном
    режиме в зависимости от версии cve
    :param result_request: результат ответа от api
    :param message: активный чат
    :param bot: бот

    """

    if len(result_request) > 0:
        vulnerabilities = result_request["vulnerabilities"]
        published = vulnerabilities[0]["cve"]["published"]
        last_modified = vulnerabilities[0]["cve"]["lastModified"]
        descriptions = vulnerabilities[0]["cve"]["descriptions"][0]["value"]
        metrics = vulnerabilities[0]["cve"]["metrics"]
        if metrics.get("cvssMetricV31"):
            metrics = metrics["cvssMetricV31"][0]["cvssData"]
            vector_string = metrics["vectorString"]
            attack_vector = metrics["attackVector"]
            attack_complexity = metrics["attackComplexity"]
            base_score = metrics["baseScore"]
            base_severity = metrics["baseSeverity"]
            bot.reply_to(
                message,
                f"Дата публикации: {published}\n"
                f"Дата последнего обновления: {last_modified}\n"
                f"Описание уязвимости: {descriptions}\n"
                f"Описание вектора атаки: {vector_string}\n"
                f"Вектор атаки: {attack_vector}\n"
                f"Тип атаки: {attack_complexity}\n"
                f"Степень атаки: {base_score}\n"
                f"Уровень угрозы: {base_severity}\n",
            )

        elif metrics.get("cvssMetricV30"):
            metrics = metrics["cvssMetricV30"][0]["cvssData"]
            vector_string = metrics["vectorString"]
            attack_vector = metrics["attackVector"]
            attack_complexity = metrics["attackComplexity"]
            base_score = metrics["baseScore"]
            base_severity = metrics["baseSeverity"]
            bot.reply_to(
                message,
                f"Дата публикации: {published}\n"
                f"Дата последнего обновления: {last_modified}\n"
                f"Описание уязвимости: {descriptions}\n"
                f"Описание вектора атаки: {vector_string}\n"
                f"Вектор атаки: {attack_vector}\n"
                f"Тип атаки: {attack_complexity}\n"
                f"Степень атаки: {base_score}\n"
                f"Уровень угрозы: {base_severity}\n",
            )

        elif metrics.get("cvssMetricV2"):
            base_severity = metrics["cvssMetricV2"][0]["baseSeverity"]
            metrics = metrics["cvssMetricV2"][0]["cvssData"]
            vector_string = metrics["vectorString"]
            attack_vector = metrics["accessVector"]
            attack_complexity = metrics["accessComplexity"]
            base_score = metrics["baseScore"]
            bot.reply_to(
                message,
                f"Дата публикации: {published}\n"
                f"Дата последнего обновления: {last_modified}\n"
                f"Описание уязвимости: {descriptions}\n"
                f"Описание вектора атаки: {vector_string}\n"
                f"Вектор атаки: {attack_vector}\n"
                f"Тип атаки: {attack_complexity}\n"
                f"Степень атаки: {base_score}\n"
                f"Уровень угрозы: {base_severity}\n",
            )

    else:
        bot.reply_to(message, "Результаты поиска нечего не дали")


def parsing_result_list_reqeust(result_request: dict, message: Message, bot):
    """
    Функция парсит данные 5-ти первых уязвимостей при ответе от API
    в зависимости от версии cve
    :param result_request: результат ответа от api
    :param message: активный чат
    :param bot: бот

    """
    if len(result_request) > 0:
        dict_res = result_request["vulnerabilities"]

        results_request = ""

        for vuln in dict_res:

            vuln_request = vuln["cve"]
            id_vuln = vuln_request["id"]
            last_modified = vuln_request["lastModified"]
            vuln_status = vuln_request["vulnStatus"]
            base_severitys = vuln_request["metrics"]
            results_request += (
                f"\nId: {id_vuln}\n"
                f"Последнее обновление: {last_modified}\n"
                f"Статус атаки: {vuln_status}\n"
            )
            if base_severitys.get("cvssMetricV31"):
                base_score = base_severitys["cvssMetricV31"][0]["cvssData"]["baseScore"]
                base_severity = base_severitys["cvssMetricV31"][0]["cvssData"][
                    "baseSeverity"
                ]
                results_request += (
                    f"Степень опасности: {base_score}\n"
                    f"Уровень реализации: {base_severity}\n"
                )
            elif base_severitys.get("cvssMetricV30"):
                base_score = base_severitys["cvssMetricV30"][0]["cvssData"]["baseScore"]
                base_severity = base_severitys["cvssMetricV30"][0]["cvssData"][
                    "baseSeverity"
                ]
                results_request += (
                    f"Степень опасности: {base_score}\n"
                    f"Уровень реализации: {base_severity}\n"
                )
            elif base_severitys.get("cvssMetricV2"):
                base_score = base_severitys["cvssMetricV2"][0]["cvssData"]["baseScore"]
                base_severity = base_severitys["cvssMetricV2"][0]["baseSeverity"]
                results_request += (
                    f"Степень опасности: {base_score}\n"
                    f"Уровень реализации: {base_severity}\n"
                )

        bot.reply_to(message, results_request)

    else:
        bot.reply_to(message, "Результаты поиска нечего не дали")


def parsing_result_list_reqeust_callback_query(
    result_request: dict, callback_query, bot
):
    """
    Функция парсит данные 5-ти первых уязвимостей при ответе от API
    на запрос выбранный при клике на кнопку в зависимости от версии cve
    :param result_request: результат ответа от api
    :param callback_query: активный чат
    :param bot: бот

    """
    if len(result_request) > 0:
        dict_res = result_request["vulnerabilities"]

        results_request = ""

        for vuln in dict_res:

            vuln_request = vuln["cve"]
            id_vuln = vuln_request["id"]
            last_modified = vuln_request["lastModified"]
            vuln_status = vuln_request["vulnStatus"]
            base_severitys = vuln_request["metrics"]
            results_request += (
                f"\nId: {id_vuln}\n"
                f"Последнее обновление: {last_modified}\n"
                f"Статус атаки: {vuln_status}\n"
            )
            if base_severitys.get("cvssMetricV31"):
                base_score = base_severitys["cvssMetricV31"][0]["cvssData"]["baseScore"]
                base_severity = base_severitys["cvssMetricV31"][0]["cvssData"][
                    "baseSeverity"
                ]
                results_request += (
                    f"Степень опасности: {base_score}\n"
                    f"Уровень реализации: {base_severity}\n"
                )
            elif base_severitys.get("cvssMetricV30"):
                base_score = base_severitys["cvssMetricV30"][0]["cvssData"]["baseScore"]
                base_severity = base_severitys["cvssMetricV30"][0]["cvssData"][
                    "baseSeverity"
                ]
                results_request += (
                    f"Степень опасности: {base_score}\n"
                    f"Уровень реализации: {base_severity}\n"
                )
            elif base_severitys.get("cvssMetricV2"):
                base_score = base_severitys["cvssMetricV2"][0]["cvssData"]["baseScore"]
                base_severity = base_severitys["cvssMetricV2"][0]["baseSeverity"]
                results_request += (
                    f"Степень опасности: {base_score}\n"
                    f"Уровень реализации: {base_severity}\n"
                )

        bot.send_message(callback_query.message.chat.id, results_request)

    else:
        bot.send_message(
            callback_query.from_user.id, "Результаты поиска нечего не дали"
        )


def get_cve_data():
    """
    Функция форматирует дату под API для получения
    результатов за последний месяц
    :return: начала отсчета и конец отсчета
    """

    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    pub_start_date = start_date.strftime("%Y-%m-%dT%H:%M:%S.000-05:00")
    pub_end_date = end_date.strftime("%Y-%m-%dT%H:%M:%S.%f-05:00")
    return pub_start_date, pub_end_date
