from create_bot import bot
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from keyboards import client_kb

# @dp.message_handler()
async def echo_send(message: types.Message, state: FSMContext):
    # print(message.chat)
    # if message.text == "Привет от бота :-)":
    if message.text == "Hy from bot :-)":
        await bot.send_message(message.from_user.id, "Hello to you my friend )) ", reply_markup=client_kb.kb_client_main)
        if message.chat.type == 'supergroup':
            await message.delete()
    else:
        if message.chat.type == 'private':
            # await bot.send_message(message.from_user.id, f"Нет такой команды: {message.text}\nЧтобы получить список команд напишите: 'меню'")
            await bot.send_message(message.from_user.id, f"No such command: {message.text}\nThere are my commands:", reply_markup=client_kb.kb_client_main)
        
    # await message.reply(message.text)
    # await bot.send_message(message.from_user.id, message.text)
    await state.finish()

def register_handlers_other(dp : Dispatcher):
    dp.register_message_handler(echo_send, state='*')