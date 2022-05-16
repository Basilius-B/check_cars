import os
import time
import requests
from bs4 import BeautifulSoup

from aiogram import Bot, Dispatcher, executor, types
import asyncio

API_TOKEN = os.getenv('BOT_TOKEN')
url_new = 'https://cars.av.by/filter?brands[0][brand]=1216&brands[0][model]=5912&brands[0][generation]=4750&transmission_type=2&engine_type[0]=5&place_region[0]=1003&sort=4'

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)

dp = Dispatcher(bot)


#
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nThis bot will be check new cars in av.by!")


async def send_message(user_id=None):
    if user_id:
        await bot.send_message(chat_id=user_id, text='Some content2')


async def is_enabled():
    while True:
        page = requests.get(url_new)
        soup = BeautifulSoup(page.content)
        div_cars = soup.find_all(class_='listing-item')
        for soup in div_cars:
            date_wr = soup.find('div', class_='listing-item__date').text
            date_list = date_wr.split(' ')
            print(date_list)
            if 'сек' in date_wr or 'только что' in date_wr:
                pass
            elif 'мин' not in date_wr:
                break
            elif 'минуту' in date_wr:
                pass
            elif int(date_list[0]) > 10:
                break

            link = 'https://cars.av.by' + soup.find('a', class_='listing-item__link').get('href')
            await bot.send_message(chat_id='-695378182', text=link)
        time.sleep(60 * 10)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(is_enabled())
    executor.start_polling(dp, skip_updates=True, )
