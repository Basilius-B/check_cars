import time

from flask import Flask, render_template, Response
from main.bot import check_new
import random
import os
import telebot

app = Flask(__name__)
BOT_TOKEN = os.getenv('BOT_TOKEN')
urls = [
    'https://cars.av.by/filter?brands[0][brand]=6&year[min]=2000&price_usd[min]=4000&price_usd[max]=12000&engine_capacity[min]=1900&engine_capacity[max]=2700&transmission_type=2&engine_type[0]=5&engine_type[1]=1&place_region[0]=1003&place_region[1]=1006&place_region[2]=1005&sort=4'
]
bot = telebot.TeleBot(token=BOT_TOKEN)



@app.route('/fps')
def fps():
    print('we are calling')
    the_answer = random.randint(25, 60)
    return (str(the_answer))


@app.route('/get_data')
def index():
    print('get_data')
    start_time = time.gmtime()
    check_new(urls, bot)
    return 'TIME - '+time.strftime("%Y-%m-%d %H:%M:%S", start_time)


@app.route('/')
def main():
    return render_template('page.html')


if __name__ == '__main__':
    app.run(debug=True)
