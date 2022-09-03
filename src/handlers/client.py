from create_bot import dp, bot
from aiogram import types, Dispatcher
from keyboards import client_kb #kb_client_main, kb_client_search
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext 
from data_base import sqlite_db
from datetime import datetime, timedelta

""" client part """
async def commands_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, 'Have a good day! \nMy menu:', reply_markup=client_kb.kb_client_main)
        if message.chat.type == 'supergroup':
            await message.delete()        
    except:
        await message.reply('To communicate with bot, write to him:\nhttps://t.me/Conference_Admin_bot')
    

async def hall_locations(message: types.Message):
        # return_message = """Зал 1. Первый этаж 121 ...\nЗал 2. Второй этаж 245 ..."""
        sql_reply = await sqlite_db.sql_location_all()
        return_message = []
        for loc in sql_reply:            
            return_message.append('\n'.join([f"{ikeys}: {loc[ikeys]}"  for i, ikeys in enumerate(loc.keys()) if i>0]))
            return_message.append('\n--------\n')
            # return_message.append(f"location name: {loc['name_location']}\n")
            # return_message.append(f"description: {loc['location_description']}\n\n")            
        await bot.send_message(message.from_user.id, ''.join(return_message)) #, reply_markup=ReplyKeyboardRemove())
        if message.chat.type == 'supergroup':
            await message.delete()


async def general_schedule(message: types.Message):
        # return_message = """С 9 до 12 Общие доклады\nС 14 до 18 секционные доклады в залах 1 и 2...\nТут будет обращение к БД"""        
        dt_m=timedelta(minutes = 15)
        # dt_d=timedelta(days = 1)
        curtime = datetime.now()
        lower_time = (curtime - dt_m).isoformat()
        upper_time = (curtime + 2*dt_m).isoformat()
        return_message = []
        sql_reply = await sqlite_db.sql_timetable_select((lower_time, upper_time, ))
        for event in sql_reply:
            return_message.append('\n'.join([f"{ikeys}: {event[ikeys]}"  for ikeys in event.keys() ]))
            return_message.append('\n--------------\n')
            # event_key = event.keys()
            # for i,event_val in enumerate(event):
            #     return_message.append(f"{event_key[i]}: {event_val}\n")
            # return_message.append('-----------\n')
        return_message = ''.join(return_message)
        print(f'len(sql_reply) = {len(sql_reply)}')
        if len(sql_reply)==0:            
            return_message = "We don't have any events at the moment"
        await bot.send_message(message.from_user.id, return_message)
        if message.chat.type == 'supergroup':
            await message.delete()


async def information(message: types.Message):
        return_message = """How to contact with us ..."""
        await bot.send_message(message.from_user.id, return_message)
        if message.chat.type == 'supergroup':
            await message.delete()


async def vote(message: types.Message):
        # return_message = """ Для голосования найдите доклад (поиск доклада), а бот выдаст кнопку для голосования."""
        return_message = [""" To vote, find a report (by "report search"), and the bot will give a button to vote.\n"""]
        # пройтись и выдать статьи за которые голосовал message.from_user.id,        
        sql_reply = await sqlite_db.sql_voting_request_votes_by_telegram( (message.from_user.id,) )
        # add_m = 'Вы уже проголосовали за:' if len(sqlreq)>0 else 'Вы еще не голосовали за доклады.'
        return_message.append('You have already voted for:' if len(sql_reply)>0 else "You haven't voted for reports yet.")
        await bot.send_message(message.from_user.id, ''.join(return_message))        
        for vote in sql_reply:
            return_message ='\n'.join([f"{ikeys}: {vote[ikeys]}"  for i, ikeys in enumerate(vote.keys()) if i>0])                
            await bot.send_message(message.from_user.id, ''.join(return_message))
        # for item in sql_reply:
        #     await bot.send_message(message.from_user.id, ''.join(item[1:]))
            
        if message.chat.type == 'supergroup':
            await message.delete()


#функции для поиска
class FSMsearch(StatesGroup):    
    search_type = State()        
    search_words = State()
#     vote = State()


async def start_search(message: types.Message):
    await FSMsearch.search_type.set()
    # await bot.send_message(message.from_user.id, 'Как будем искать доклад?', reply_markup=client_kb.kb_client_search)
    await bot.send_message(message.from_user.id, 'How should we look for the report?', reply_markup=client_kb.kb_client_search)    
    if message.chat.type == 'supergroup':
        await message.delete()


async def cancel_handler(message: types.Message, state: FSMContext):    
    current_state = await state.get_state()
    if current_state is None:
        return 
    await state.finish()
    # await bot.send_message(message.from_user.id, 'Поиск отменен', reply_markup=client_kb.kb_client_main)
    await bot.send_message(message.from_user.id, 'Search is canceled', reply_markup=client_kb.kb_client_main)
    if message.chat.type == 'supergroup':
        await message.delete()


async def search_type(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['search_type'] = message.text
    
    # return_message = """Тут будет выдан результат поиска, 
    # а после каждой статьи инлайн кнопка 
    # проголосовать за эту статью 
    # или снять голос с этой статьи"""
    # await bot.send_message(message.from_user.id, return_message, reply_markup=client_kb.kb_client_main)
    
    await FSMsearch.next()
    # await bot.send_message(message.from_user.id, 'Введите слова для поиска ' + data['search_type'],reply_markup=client_kb.kb_client_cancel)    
    await bot.send_message(message.from_user.id, 'Input words to search '
                + data['search_type'] + 
                '.\nFor example: "Desai, Singh" or "NLP, COVID-19 news"',
                reply_markup=client_kb.kb_client_cancel)    
    if message.chat.type == 'supergroup':
        await message.delete()
    
async def search_words(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['search_words'] = message.text
    # await FSMsearch.next()
    # return_message = """Тут будет выдан результат поиска, 
    # а после каждой статьи инлайн кнопка 
    # проголосовать за эту статью 
    # или снять голос с этой статьи"""
    # await bot.send_message(message.from_user.id, return_message, reply_markup=client_kb.kb_client_main)
    # await bot.send_message(message.from_user.id, 'поиск делаем по: ' + data['search_type'])    
    
    
    # if 'автор' in data['search_type']:
    #     vote_results = await sql_count_votes()
    async with state.proxy() as data:
        reply= None        
        # await bot.send_message(message.from_user.id, f'Здесь мы выдадим результат поиска {data.values()} и предложим проголосовать инлайн кнопками', reply_markup=client_kb.kb_client_main)    
        # if 'автор' in data['search_type']:
        if 'author' in data['search_type']:
            input_data = tuple(map(str, ['%' + item + '%' for item in data['search_words'].split(',')]))
            print(f"input_data={input_data}")
            print(f"type(input_data) = {type(input_data)}")
            reply = await sqlite_db.sql_search_by_author(input_data)
        # elif 'назван' in data['search_type']:
        elif 'title' in data['search_type']:
            # input_data = tuple(map(str, data['search_words'].split(',')))
            input_data = tuple(map(str, ['%' + item + '%' for item in data['search_words'].split(',')]))
            print(f"input_data={input_data}")
            print(f"type(input_data) = {type(input_data)}")
            reply = await sqlite_db.sql_search_by_title(input_data)
        # elif 'аннотац' in data['search_type']:
        # elif 'abstract' in data['search_type']:
        #     # reply = [(-1,'А тут ищем в аннотациях')]            
        #     reply = [(-1,'And here we are looking in the abstracts')]            
        print(reply)
        if len(reply)>0:
            
            for item in reply:
                return_message = '\n'.join([f"{ikeys}: {item[ikeys]}"
                                for i, ikeys in enumerate(item.keys()) 
                                if (i>0 and i<(len(item)-1))])
                await bot.send_message(message.from_user.id, ''.join(return_message),\
                    reply_markup=InlineKeyboardMarkup().\
                    add(InlineKeyboardButton(f'ссылка(url) на доклад',\
                        # url='https://yandex.ru/search/?text=%D0%BA%D0%BE%D0%BD%D1%84%D0%B5%D1%80%D0%B5%D0%BD%D1%86%D0%B8%D1%8F')).\
                        url=item[item.keys()[-1]])).\
                    # add(InlineKeyboardButton(f'Голосовать за статью', callback_data=f'vote_for#{item[0]}#1')).\
                    add(InlineKeyboardButton(f'Vote for the article', callback_data=f'vote_for#{item[0]}#1')).\
                    # insert(InlineKeyboardButton(f'Отозвать свой голос', callback_data=f'vote_for#{item[0]}#0')))                        
                    insert(InlineKeyboardButton(f'Withdraw your vote', callback_data=f'vote_for#{item[0]}#0')))
                
                
            # await bot.send_message(message.from_user.id, ''.join(reply[-1][1:]), reply_markup=client_kb.kb_client_main)
            # Как мне перейти в меню??? 
            # await bot.send_message(message.from_user.id, f"Основное меню:", reply_markup=client_kb.kb_client_main)
            await bot.send_message(message.from_user.id, f"Here is the menu:", reply_markup=client_kb.kb_client_main)
        else:
            # await bot.send_message(message.from_user.id, f"Не смогли найти по запросу: {data['search_words']}", reply_markup=client_kb.kb_client_main)
            await bot.send_message(message.from_user.id, f"Couldn't find on request: {data['search_words']}", reply_markup=client_kb.kb_client_main)

    
    await state.finish()
    if message.chat.type == 'supergroup':
        await message.delete()

# @dp.callback_query_handler(lambda x: x.data and x.data.startswith('vote_for#'))
async def vote_for(callback: types.CallbackQuery):
    # print("\n\n I am in function VOTE_FOR")
    id, vote = tuple(map( int, callback.data.split('#')[1:]))
    # print(f"callback.data: {callback.data}, id = {id}, vote = {vote}")
    # reply = 'Ваш голос учтен' if vote == 1 else 'Ваш голос был отозван'
    reply = 'Your vote has been counted' if vote == 1 else 'Your vote has been withdraw'
    if vote==0:
        await sqlite_db.sql_voting_update_one_vote( (vote, id, callback.from_user.id, ))
    else:
        sqlreq = await sqlite_db.sql_voting_request_votes_by_report_telegram( (id, callback.from_user.id,) )
        for item in sqlreq:
            print(item)
        if len(sqlreq)>0:
            if sqlreq[0][3] == 1:
                # reply = 'Вы уже голосовали за эту статью.\nЗа 1 статью можно отдать 1 голос.'
                reply = 'You have already voted for this article.\nYou can give 1 vote for 1 article.'
            else:
                await sqlite_db.sql_voting_update_one_vote( (vote, id, callback.from_user.id, ))                           
        else:
            await sqlite_db.sql_voting_insert_one_vote( (id, callback.from_user.id, 1,))            
                                                
    # await bot.send_message(callback.from_user.id, reply)
    await callback.answer(reply)
    



def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(commands_start, commands=['start', 'help'])
    dp.register_message_handler(commands_start, Text(equals=['помоги','help','bot','бот','menu','меню'],ignore_case=True))
    # dp.register_message_handler(hall_locations, commands=['Расположение_залов'])
    dp.register_message_handler(hall_locations, commands=['locations'])
    # dp.register_message_handler(hall_locations, Text(equals=['Расположение_залов','расположение залов','залы'],ignore_case=True))
    dp.register_message_handler(hall_locations, Text(equals=['locations','hall'],ignore_case=True))
    # dp.register_message_handler(information, commands=['Контакты'])
    dp.register_message_handler(information, commands=['contacts'])
    # dp.register_message_handler(information, Text(equals=['Инфо','информация','контакты'],ignore_case=True))
    dp.register_message_handler(information, Text(equals=['info','informatoin','contacts'],ignore_case=True))
    # dp.register_message_handler(general_schedule, commands=['Расписание'])
    dp.register_message_handler(general_schedule, commands=['timetable'])
    # dp.register_message_handler(general_schedule, Text(equals=['Сейчас идет','расписание','now','сейчас'],ignore_case=True))
    dp.register_message_handler(general_schedule, Text(equals=['now','timetable','schedule'],ignore_case=True))
    # dp.register_message_handler(vote, Text(equals=['мой голос'],ignore_case=True))
    dp.register_message_handler(vote, Text(equals=['my votes'],ignore_case=True))
    dp.register_callback_query_handler(vote_for, lambda x: x.data and x.data.startswith('vote_for#'))
    
    # dp.register_message_handler(start_search, Text(equals='поиск доклада',ignore_case=True), state=None)
    dp.register_message_handler(start_search, Text(equals='search for report', ignore_case=True), state=None)
    # dp.register_message_handler(cancel_handler, state='*', commands='отменить поиск')
    dp.register_message_handler(cancel_handler, state='*', commands='cancel search')
    # dp.register_message_handler(cancel_handler, Text(equals='отменить поиск',ignore_case=True), state='*')
    dp.register_message_handler(cancel_handler, Text(equals='cancel search',ignore_case=True), state='*')
    # dp.register_message_handler(search_type, Text(equals=['по автору', 'по словам в названии', 'по словам в аннотации',],ignore_case=True), state=FSMsearch.search_type)
    dp.register_message_handler(search_type, Text(equals=['by author', 'by words in title'], ignore_case=True), state=FSMsearch.search_type)
    dp.register_message_handler(search_words, state=FSMsearch.search_words)
    
    # 