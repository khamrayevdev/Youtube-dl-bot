import logging
from aiogram import Bot, Dispatcher, executor
from aiogram.types import *
from pytube import *
import os
import config


# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

video = None

def create_keyboard(yt):
    buttons = []
    keyboard = InlineKeyboardMarkup(row_width=1)
    i = 0
    for stream in yt.streams.filter(progressive="True"):
        typ = str(stream).split(" ")[2].split("=")[1][1:-1]
        quality = str(stream).split(" ")[3].split("=")[1][1:-1]

        text_button = "Tip: {}, Sifati: {}".format(typ, quality)
        buttons.append(InlineKeyboardButton(text=text_button, callback_data=str(i)))
        i += 1
    keyboard.add(*buttons)
    return keyboard

@dp.message_handler(commands=['start'])
async def lalu(message: Message):
    await message.answer_photo('AgACAgIAAxkBAANiYmllFQLrSPGU4a_q5w1pnqJN0fIAAk-9MRuj5ElL1ubZjyuSr4kBAAMCAAN5AAMkBA', caption="Assalomu aleykum!\nBu bot orqali youtubedan video yuklab olishingiz mumkin")


@dp.message_handler(content_types='text')
async def asdf(message: Message):
    yt = None
    try:
        yt = YouTube(message.text)
    except:
        await bot.send_message(message.chat.id, "Menga YouTube video linkini jo'nating.")
    if yt is not None:
        keyboard = create_keyboard(yt)
        global video
        video = yt
        await bot.send_message(message.chat.id, "Yuklab olish uchun formatni tanlang", reply_markup=keyboard)


@dp.callback_query_handler(func=lambda x: True)
async def query_hand(call: CallbackQuery):
    global video
    await call.message.answer('yuklanmoqda...')
    this = video.streams.filter(progressive='True')[int(call.data)].download(filename="{}".format(call.from_user.id))
    video = open(this, rb)
    await bot.send_video(call.from_user.id, video)
    video.close()
    name = f"rm -f {call.from_user.id}"
    os.system(name)
    os.remove("{}.mp4".format(call.from_user.id))

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
