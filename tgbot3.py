import asyncio
import logging
import time

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils import exceptions

logging.basicConfig(level=logging.INFO)

TOKEN = "5456832876:AAG_oDE77miDIEtjG8jVWNCRZmqP76BTYAg"
MSG = "Ты делал что нибудь полезное сегодня, {}?"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)


async def send_periodic_message():
    while True:
        try:
            user_id = 1178506932
            user_name = "друг"
            await bot.send_message(user_id, MSG.format(user_name))
        except exceptions.BotBlocked:
            logging.warning(f"Bot is blocked by the user")
        except exceptions.ChatNotFound:
            logging.warning(f"Chat not found")
        except exceptions.RetryAfter as e:
            logging.warning(f"Telegram API limits: {e.timeout} seconds")
            await asyncio.sleep(e.timeout)
        except exceptions.TelegramAPIError:
            logging.exception("Exception occurred")
        await asyncio.sleep(30 * 60)


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id=} {user_full_name=} {time.asctime()}')
    await message.reply(f"Привет, {user_full_name}!")


if __name__ == '__main__':
    asyncio.ensure_future(send_periodic_message())
    executor.start_polling(dp, skip_updates=True)
