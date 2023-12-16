import logging
import asyncio
import datetime
import listings as list
from aiogram import Bot, Dispatcher, executor, types
from words import WORDS
from exceptions import EXCEPTIONS
from config import CHAT_ID, TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(TOKEN)
dp = Dispatcher(bot)

def chech_sub_channel(chat_member):
    return chat_member['status'] != 'left'

# Приветствие нового участника
@dp.message_handler(content_types=["new_chat_members"])
async def handler_new_member(message: types.Message):
    user_name = message.new_chat_members[0].first_name
    msg = await message.answer(f'Привет, {user_name}!\nМы тебе рады!\n✔️Представься, пожалуйста, в чате.\n❗️Если ты первый раз в группе Анонимных Алкоголиков — напиши, что ты «новичок»💙')
    await asyncio.sleep(60)
    await msg.delete()

# Фильтр запрещённых слов
@dp.message_handler()
async def filter_messages(message: types.Message):
    text = message.text.lower()
    for word in WORDS:
        if word in text.split(' '):
            await message.delete()
            nik_name = message.from_user.username
            user_name = message.from_user.first_name
            msg = await message.answer(f"{user_name} — @{nik_name}, твоё сообщение было удалено.\n\nНапоминаю правила группы Китти Хок:\n✔️мы не выясняем отношения;\n✔️мы не используем нецензурные слова и выражения.\n\n💔За неоднократное нарушение правил чата участник может быть удален без предупреждения!")
            await asyncio.sleep(30)
            await msg.delete()
        for word in EXCEPTIONS:
            if word in text:
                await message.delete()
                nik_name = message.from_user.username
                user_name = message.from_user.first_name
                msg = await message.answer(f"{user_name} — @{nik_name}, твоё сообщение было удалено.\n\nНапоминаю правила группы Китти Хок:\n✔️мы не выясняем отношения;\n✔️мы не используем нецензурные слова и выражения.\n\n💔За неоднократное нарушение правил чата участник может быть удален без предупреждения!")
                await asyncio.sleep(30)
                await msg.delete()
                return

# Отправка сообщения по расписанию
async def send_message():
    chat_id = CHAT_ID
    now = datetime.datetime.now()
    if now.hour == 9 and now.minute >= 0 and now.minute < 1:
        message_text = list.RULES
    elif now.hour == 20 and now.minute >= 0 and now.minute < 1:
        message_text = list.TABLE
    else:
        return
    await bot.send_message(chat_id=chat_id, text=message_text, parse_mode=types.ParseMode.HTML)

# Установка времени отправки сообщения по расписанию
async def schedule_message():
    while True:
        now = datetime.datetime.now()
        if now.hour == 9 and now.minute == 0:
            await send_message()
        elif now.hour == 20 and now.minute == 0:
            await send_message()
        await asyncio.sleep(60)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(schedule_message())
    executor.start_polling(dp, skip_updates=True)