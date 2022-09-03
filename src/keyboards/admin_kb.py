from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# button_load = KeyboardButton('/Загрузить')
# button_count_votes = KeyboardButton('/Подсчёт_голосов')
button_count_votes = KeyboardButton('/Count_votes')
# button_delete = KeyboardButton("/Удалить")
button_umenu = KeyboardButton("/user_menu")

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True)\
    .add(button_count_votes).add(button_umenu)
    # .add(button_load)\    
    # .add(button_delete)