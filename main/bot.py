import os
import time
import requests
from bs4 import BeautifulSoup
import re
import telebot
# from dotenv import load_dotenv

# project_folder = os.path.expanduser('~\check_cars')
# load_dotenv('.env')

BOT_TOKEN = os.getenv('BOT_TOKEN')
urls = [
    'https://cars.av.by/filter?brands[0][brand]=6&year[min]=2000&price_usd[min]=4000&price_usd[max]=12000&engine_capacity[min]=1900&engine_capacity[max]=2700&transmission_type=2&engine_type[0]=5&engine_type[1]=1&place_region[0]=1003&place_region[1]=1006&place_region[2]=1005&sort=4'
]
# Initialize bot and dispatcher
bot = telebot.TeleBot(token=BOT_TOKEN)


def is_enabled():
    print('start_loop')
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
    bot.send_message(chat_id='-695378182', text='start work')
    while True:
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
                           '\nhttps://cars.av.by' + link
                try:
                    bot.send_message(chat_id='-695378182', text=msg_text)
                except Exception as e:
                    print(e)

        print('start_sleep')
        time.sleep(60 * 2)


if __name__ == "__main__":
    is_enabled()
