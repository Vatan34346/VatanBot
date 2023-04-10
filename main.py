import os
from dotenv import load_dotenv
from gpt import ChatGptHandler
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


load_dotenv()

gpt_answer = ChatGptHandler(os.getenv('OPEN_AI_API_KEY'))

bot = Bot(os.getenv('TELEGRAM_BOT_KEY'))
dp = Dispatcher(bot)
conversation_history = {}


@dp.message_handler()
async def send(message: types.Message):
    bot_info = await bot.get_me()

    if message.reply_to_message and message.reply_to_message.from_user.id == bot_info.id:
        user_id = message.from_user.id

        history = conversation_history.get(user_id, [])
        history.append(message.text)

        response = gpt_answer.generate_answer("".join(history))
        history.append(response)
        conversation_history[user_id] = history

        await message.answer(response, reply=True)

    if message.text.startswith('@'+bot_info.username):
        user_id = message.from_user.id

        history = conversation_history.get(user_id, [])
        history.append(message.text)

        response = gpt_answer.generate_answer("".join(history))
        history.append(response)
        conversation_history[user_id] = history

        await message.answer(response, reply=True)
    else:
        return

executor.start_polling(dp, skip_updates=True)

