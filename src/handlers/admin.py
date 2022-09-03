from aiogram.dispatcher import FSMContext 
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp, bot
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from tabulate import tabulate
from keyboards import admin_kb, client_kb


# from data_base.sqlite_db import sql_add_command
from data_base.sqlite_db import sql_count_votes

# global list with Admins IDs, to be sure that user is admin
ADMINS = None

async def make_changes_command(message: types.Message):
    global ADMINS
    admins = None
    try:    
        admins = await message.chat.get_administrators()        
    except BaseException as err:
        await bot.send_message(message.from_user.id, err)
        if ADMINS is None:
            await bot.send_message(message.from_user.id, "I don't have ADMIN IDs\nPlease write '/moder' in group chat")
    if admins is not None:             
        admin_ids = [
            admin.user.id for admin in admins if admin.is_chat_admin() and not admin.user.is_bot
            # admin.user.id for admin in admins if admin.is_chat_admin()
        ]
        # for admin in admin_ids:
        #     member = await bot.get_chat_member(message.chat.id, admin)
        #     for x in member:
        #         print(x)
            
        ADMINS = admin_ids
        await bot.send_message(message.from_user.id, "Admins IDs have been loaded")
    
    # print(f'ADMINS: {ADMINS}')
    # print(f'print(ADMINS): {type(ADMINS)}')
    # print(f'print(ADMINS[0]): {type(ADMINS[0])}')
    # print(f"message.from_user = {message.from_user}")
    # print(f"message.from_user.id = {message.from_user.id}")
    # print(f"type(message.from_user.id) = {type(message.from_user.id)}")
    # print(f"message.from_user.id in ADMINS = {message.from_user.id in ADMINS}")
    
    # member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    # for x in member:
    #     print(x)
    
    #         
    # if message.from_user.id not in ADMINS:
    #     ADMINS.append(message.from_user.id)
    # ADMINS.add(message.from_user.id)
    if message.from_user.id in ADMINS:
        await bot.send_message(message.from_user.id, 'you get "admin_menu"', reply_markup=admin_kb.button_case_admin)
    if ADMINS is None:
        await bot.send_message(message.from_user.id, "I don't have ADMIN IDs\nPlease write '/moder' in group chat")
    if message.chat.type == 'supergroup':
        await message.delete()
    

async def count_votes(message: types.Message):
    if message.from_user.id in ADMINS:
        vote_results = await sql_count_votes()        
        vote_res = [[val[:20] if type(val)==str else val for val in row] for row in vote_results]
        print(vote_res)                
        # ['id', 'title', 'votes']
        # print(vote_results[0].keys())
        #"pretty" 
        #orgtbl       
        str_results ='<pre>' + tabulate(vote_res, headers=['id', 'title', '#'],tablefmt='pretty',disable_numparse=True)+'</pre>'
        print(str_results)
        await bot.send_message(message.from_user.id, str_results, parse_mode=types.ParseMode.HTML, reply_markup=admin_kb.button_case_admin)
        if message.chat.type == 'supergroup':
            await message.delete()


async def user_menu(message: types.Message):
    if ADMINS is None:
        await bot.send_message(message.from_user.id, "I don't have ADMIN IDs\nPlease write '/moder' in group chat")
    else:
        if message.from_user.id in ADMINS:
            await bot.send_message(message.from_user.id, 'changing menu to user_menu, \nto get admin_menu send "/admin_menu" to me', reply_markup=client_kb.kb_client_main)            
        else:
            await bot.send_message(message.from_user.id, 'This is admins command, but you are not in Admin IDs list.\nConnect to admins of the group', reply_markup=client_kb.kb_client_main)
    if message.chat.type == 'supergroup':
        await message.delete()
        

async def admin_menu(message: types.Message):
    if ADMINS is None:
        await bot.send_message(message.from_user.id, "I don't have ADMIN IDs\nPlease write '/moder' in group chat")
    else:
        if message.from_user.id in ADMINS:
            await bot.send_message(message.from_user.id, 'changing menu to admin_menu, \nto get user_menu send "/user_menu" to me', reply_markup=admin_kb.button_case_admin)
        else:
            await bot.send_message(message.from_user.id, 'sorry you are not in Admin IDs list.\nConnect to admins of the group', reply_markup=client_kb.kb_client_main)
    if message.chat.type == 'supergroup':
        await message.delete()
        

# add new event to timetable
class FSMAdmin(StatesGroup):
    date = State()
    title = State()
    description = State()
    duration = State()
    

async def cm_start(message: types.Message):
    print(message.from_user)
    print(message.from_user.id)
    member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    for x in member:
        print(x) 
    if message.from_user.id in ADMINS:
        await FSMAdmin.date.set()
        await message.reply('Введите дату мероприятия')

async def cancel_handler(message: types.Message, state: FSMContext):    
    if message.from_user.id in ADMINS:
        current_state = await state.get_state()
        if current_state is None:
            return 
        await state.finish()
        await message.reply('OK')


async def load_date(message: types.Message, state: FSMContext):   
    if message.from_user.id in ADMINS:
        async with state.proxy() as data:
            data['date'] = message.text
        await FSMAdmin.next()
        await message.reply("Теперь введите название = title")
    

async def load_title(message: types.Message, state: FSMContext):    
    if message.from_user.id in ADMINS:
        async with state.proxy() as data:
            data['title'] = message.text
        await FSMAdmin.next()
        await message.reply("Введи описание description")
        

async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMINS:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdmin.next()
        await message.reply("Введи продолжительность duration")


#catch third answer     
async def load_duration(message: types.Message, state: FSMContext):    
    if message.from_user.id in ADMINS:
        async with state.proxy() as data:
            data['duration'] = message.text
        async with state.proxy() as data:
            print(tuple(data.values()))        
        await state.finish()
    

#Exit from states
# @dp.message_handler(state='*',commands='отмена')
# @dp.message_handler(Text(equals='отмена',ignore_case=True),state='*')

    
    
#register our handlers
def register_handlers_admin(dp: Dispatcher):        
    dp.register_message_handler(make_changes_command, commands=['moder'])
    # dp.register_message_handler(count_votes, commands=['Подсчёт_голосов'])
    dp.register_message_handler(count_votes, commands=['Count_votes'])    
    dp.register_message_handler(user_menu, commands=['user_menu'])
    dp.register_message_handler(user_menu, Text(equals=['user menu','user_menu'],ignore_case=True))
    dp.register_message_handler(admin_menu, commands=['admin_menu'])
    dp.register_message_handler(admin_menu, Text(equals=['admin menu','admin_menu'],ignore_case=True))
    
    # dp.register_message_handler(cm_start, commands=['Загрузить'], state=None)
    # dp.register_message_handler(cancel_handler, state='*', commands='отмена')
    # dp.register_message_handler(cancel_handler, Text(equals='отмена',ignore_case=True), state='*')
    # dp.register_message_handler(load_date, state=FSMAdmin.date)
    # dp.register_message_handler(load_title, state=FSMAdmin.title)
    # dp.register_message_handler(load_description, state=FSMAdmin.description)
    # dp.register_message_handler(load_duration, state=FSMAdmin.duration)
    # # dp.register_message_handler(make_changes_command, commands=['moderator'], is_chat_admin=True)
    

    