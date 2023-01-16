import os
import time
import requests
from aiogram.types import InputMediaPhoto
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.common.by import By

from aiogram import Bot, Dispatcher, executor, types
import asyncio

API_TOKEN = os.getenv('BOT_TOKEN')
urls = [
    'https://cars.av.by/filter?brands[0][brand]=6&year[min]=2000&price_usd[min]=4000&price_usd[max]=12000&engine_capacity[min]=1900&engine_capacity[max]=2700&transmission_type=2&engine_type[0]=5&engine_type[1]=1&place_region[0]=1003&place_region[1]=1006&place_region[2]=1005&sort=4'
]

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)

dp = Dispatcher(bot)


#
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nThis bot will be check new cars in av.by!")





async def is_enabled():
    print('tut')
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
    driver = webdriver.Chrome()
    while True:
        sleep_time = 60 * 5
        for url in urls:
            page = requests.get(url, headers=headers)
            soup = BeautifulSoup(page.content, 'lxml')
            div_cars = soup.find_all(class_='listing-item')
            for soup in div_cars:
                date_wr = soup.find('div', class_='listing-item__date').text
                date_list = date_wr.split(' ')
                if 'сек' in date_wr or 'только что' in date_wr:
                    pass
                elif 'мин' not in date_wr:
                    break
                elif 'минут' in date_list[0]:
                    pass
                elif int(date_list[0]) > 5:
                    break
                price_usd = soup.find('div', class_='listing-item__priceusd').text
                city = soup.find('div', class_='listing-item__location').text
                params = soup.find('div', class_='listing-item__params').text
                year = params[:7]
                p: str = params[7:]
                km = re.search(r'(\d+ \d+ км)', p).group(0)
                p = p.replace(km, '')
                params = [year, *p.split(','), km]
                link = soup.find('a', class_='listing-item__link').get('href')
                msg_text = 'цена ' + price_usd + \
                           '\nгород -' + city + '\n' + \
                           '\n'.join(params) + \
                           '\nhttps://cars.av.by' + soup.find('a', class_='listing-item__link').get('href')
                try:
                    driver.get('https://cars.av.by' + link)
                    driver.find_element(By.CLASS_NAME, "gallery__fullscreen-button").click()
                    list_link = driver.find_elements(By.CLASS_NAME, 'fullscreen-gallery__item')
                    photos = [i.find_element(By.TAG_NAME, 'img').get_attribute('data-src') for i in list_link]
                    # driver.close()
                    # driver.quit()
                    photos_links = [InputMediaPhoto(photo, caption=msg_text) if i == 0 else InputMediaPhoto(photo) for
                                    i, photo in enumerate(photos[::len(photos) // 10])]
                    await bot.send_media_group(chat_id='-695378182', media=photos_links[:9])
                    time.sleep(20)
                    sleep_time += 20
                except Exception as e:
                    print(e)
                    e = str(e)
                    if 'Flood control' in e:
                        try:
                            time.sleep(int(e.split(' ')[-2]) + 5)
                            sleep_time = int(e.split(' ')[-2]) + 6
                            await bot.send_media_group(chat_id='-695378182', media=photos_links[:9])
                        except Exception as e2:
                            print(e2)
        print('start_sleep')
        time.sleep(60 * sleep_time)


async def task1():
    await dp.start_polling()


async def main():
    await asyncio.gather(
        is_enabled(),
        task1()
    )


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())

# if __name__ == '__main__':
#     executor.start_polling(dp, skip_updates=True)
#     loop = asyncio.get_event_loop()
#     loop.create_task(is_enabled())
