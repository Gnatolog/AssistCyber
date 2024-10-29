import requests
from config_data.config import API_KEY_NVD
from utils.set_bot_commands import get_cve_data


def get_vuln_id(id_vuln: str) -> dict:
    """
    Функция получения информации по id уязвимости
    :param id_vuln: CVE уязвимости
    :return:  словарь с ответом от api
    """

    base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=" + id_vuln

    headers = {
        "apiKey": API_KEY_NVD,
    }

    response = requests.get(base_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data

    else:
        data = dict()
        print(f"Ошибка: {response.status_code} - {response.text}")
        return data


def get_vuln_rating(rating_vuln: str) -> dict:
    """
    Функция получения информации по рейтингу уязвимости
    :param rating_vuln: рейтинг уязвимости
    :return:  словарь с ответом от api
    """
    date_month = get_cve_data()
    base_url = (
        "https://services.nvd.nist.gov/rest/json/cves/2.0?cvssV3Severity="
        + rating_vuln
        + "&resultsPerPage=5&startIndex=0&pubStartDate="
        + date_month[0]
        + "&pubEndDate="
        + date_month[1]
    )

    headers = {
        "apiKey": API_KEY_NVD,
    }

    response = requests.get(base_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data

    else:
        data = dict()
        print(f"Ошибка: {response.status_code} - {response.text}")
        return data


def get_vuln_keyword(key_word: str) -> dict:
    """
    Функция получения информации по рейтингу уязвимости
    :param key_word: ключевое слово для поиска
    :return:  словарь с ответом от api
    """

    date_month = get_cve_data()

    base_url = (
        "https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch="
        + key_word
        + "&resultsPerPage=5&startIndex=0&pubStartDate="
        + date_month[0]
        + "&pubEndDate="
        + date_month[1]
    )

    headers = {
        "apiKey": API_KEY_NVD,
    }

    response = requests.get(base_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data

    else:
        data = dict()
        print(f"Ошибка: {response.status_code} - {response.text}")
        return data


def get_vuln_first_5() -> dict:
    """
    Функция получения информации по топ 5 уязвимостей
    :return:  словарь с ответом от api
    """
    date_month = get_cve_data()
    base_url = (
        "https://services.nvd.nist.gov/rest/json/cves/2.0/?resultsPerPage=5&startIndex=0&"
        "pubStartDate=" + date_month[0] + "&pubEndDate=" + date_month[1]
    )

    headers = {
        "apiKey": API_KEY_NVD,
    }

    response = requests.get(base_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data

    else:
        data = dict()
        print(f"Ошибка: {response.status_code} - {response.text}")
        return data


def get_vuln_oval_mitre() -> dict:
    """
    Функция получения информации по топ 5 уязвимостей
    :return:  словарь с ответом от api
    """

    base_url = (
        "https://services.nvd.nist.gov/rest/json/cves/2.0?hasOval"
        "&resultsPerPage=5&startIndex=0"
    )

    headers = {
        "apiKey": API_KEY_NVD,
    }

    response = requests.get(base_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data

    else:
        data = dict()
        print(f"Ошибка: {response.status_code} - {response.text}")
        return data
