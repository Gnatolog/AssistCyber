from telebot.handler_backends import State, StatesGroup


class UserStates(StatesGroup):
    base = State()
    search_vuln = State()
    search_vuln_nvd_id = State()
    search_vuln_nvd_key = State()
    search_vuln_nvd_rating = State()
    search_vuln_nvd_oval = State()
    search_vuln_nvd_first_5 = State()
    history = State()
