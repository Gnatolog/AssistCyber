from loader import bot
from telebot.types import Message
from states.state_user import UserStates
from keyboards.inline.choice_action import choice_button


@bot.message_handler(state=UserStates.base)

def get_base(message: Message):
    print("MENU_base")
    bot.send_message(message.from_user.id, f'Что хотите сделать',
                     reply_markup=choice_button())