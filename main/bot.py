import os
import time
import requests
from bs4 import BeautifulSoup
import re
import telebot


def check_new(urls, bot):

    print('start_loop')

    # bot.send_message(chat_id='-695378182', text='start work')
    # while True:
    for url in urls:
        page = requests.get(url)
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
            print(msg_text)
            try:
                bot.send_message(chat_id='-695378182', text=msg_text)
            except Exception as e:
                print(e)
    print('start_sleep')

if __name__ == "__main__":
    check_new()
