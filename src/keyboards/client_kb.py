from aiogram.types import ReplyKeyboardMarkup, KeyboardButton#, ReplyKeyboardRemove



btimetable = KeyboardButton('timetable')
bhalls = KeyboardButton('locations')
bsearch = KeyboardButton('search for report')
bcontacts = KeyboardButton('contacts')
bvote = KeyboardButton('my votes')

s_author = KeyboardButton('by author')
s_title = KeyboardButton('by words in title')
s_abstracts = KeyboardButton('by words in abstract')
s_cancel = KeyboardButton('cancel search')

# btimetable = KeyboardButton('расписание')
# bhalls = KeyboardButton('расположение залов')
# bsearch = KeyboardButton('поиск доклада')
# bcontacts = KeyboardButton('контакты')
# bvote = KeyboardButton('мой голос')

# s_author = KeyboardButton('по автору')
# s_title = KeyboardButton('по словам в названии')
# s_abstracts = KeyboardButton('по словам в аннотации')
# s_cancel = KeyboardButton('отменить поиск')

# bt01 = KeyboardButton('Поделиться номером', request_contact=True)
# bt02 = KeyboardButton('Отправить где я ', request_location=True)


# kb_client = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
kb_client_main = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client_main.add(btimetable).insert(bhalls).add(bsearch).insert(bvote).insert(bcontacts)
# kb_client.add(b03).insert(b02).add(b10).row(bt01, bt02)

kb_client_search = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client_search.add(s_author).insert(s_title).\
    add(s_cancel)
    # add(s_abstracts).\
    

kb_client_cancel = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
kb_client_cancel.add(s_cancel)