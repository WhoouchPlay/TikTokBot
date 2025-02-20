import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, InputFile
import requests

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
proxy_url = "http://proxy.server:3128"
logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN, proxy=proxy_url)
dp = Dispatcher(bot, storage=MemoryStorage())



@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.answer(text='Привіт! Я - бот-завантажувач🎲\nНадішли мені посилання на TikTok-відео, і я відправлю його тобі без водяного знаку!')

@dp.message_handler()
async def start(message: types.Message):
    link = message.text

    msg = await message.answer("Будь ласка зачекайте, оброблюємо ваш запит.")
    url = "https://tiktok-video-no-watermark2.p.rapidapi.com/"

    print(link)

    querystring = {"url": link, "hd": "1"}
    headers = {
        "x-rapidapi-key": os.getenv("APITOKEN"),
        "x-rapidapi-host": "tiktok-video-no-watermark2.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers, params=querystring)
        print(response.json())
        video_link = response.json()['data']['play']
        await msg.edit_text("Надсилаємо відео. \nЗачекайте...")
        await msg.delete()
        await bot.send_video(message.chat.id, video_link)
    except BaseException:
        await msg.edit_text("Вибачте я не розумію вас \nВведіть чітке питання, або ж надішліть вірне посилання.")



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)