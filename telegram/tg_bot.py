from datetime import datetime, timedelta

import settings

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton
import requests

bot = Bot(token=settings.TOKEN)

dp = Dispatcher(bot)

user_token = {}


# Keyboards
def get_default_kb():
    statistic = KeyboardButton("Dino statistics")
    work = KeyboardButton("Go to work")
    return ReplyKeyboardMarkup().add(statistic).add(work)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    if str(message.from_user.id) not in user_token.keys():
        data = {"telegram_id": str(message.from_user.id), "username": str(message.from_user.username),
                "status": "beginner",
                "experience": 0, "isAdmin": False}
        response = requests.post("http://localhost:8000/api/user", json=data)

        if response.status_code == 200:
            user_token[str(message.from_user.id)] = {"Authorization": response.json()["detail"]}
            await bot.send_message(message.from_user.id, "You are successfully registered\nYour experience = 0\nYour "
                                                         "role = beginner", reply_markup=get_default_kb())

        else:
            await bot.send_message(message.from_user.id, "Something went wrong")
    else:
        await bot.send_message(message.from_user.id, "You are already registered", reply_markup=get_default_kb())


@dp.message_handler(text=["Dino statistics"])
async def statistics_handler(message: types.Message):
    if str(message.from_user.id) in user_token.keys():
        response = requests.get("http://localhost:8000/api/user", headers=user_token[str(message.from_user.id)])

        if response.status_code == 200:
            username = response.json()["username"]
            status = response.json()["status"]
            experience = response.json()["experience"]

            await bot.send_message(message.from_user.id,
                                   f"Your username {username}\nExperience = {experience}\nRole = {status}",
                                   reply_markup=get_default_kb())
        else:
            await bot.send_message(message.from_user.id, "Something went wrong", reply_markup=get_default_kb())

    else:
        await bot.send_message(message.from_user.id, "You are not registered")


@dp.message_handler(text=["Go to work"])
async def go_to_work_handler(message: types.Message):
    if str(message.from_user.id) in user_token.keys():
        finish = datetime.now() + timedelta(minutes=30)
        data = {"telegram_id": str(message.from_user.id), "working_status": "removes garbage on the street",
                "finish": int(finish.timestamp())}
        response = requests.post("http://localhost:8000/api/user/work", json=data,
                                 headers=user_token[str(message.from_user.id)])

        if response.status_code == 200:
            response_status = response.json()["status"]
            if response_status == "OK":
                await bot.send_message(message.from_user.id,
                                       "Your dino is going to work. He will finish in 30 minutes!",
                                       reply_markup=get_default_kb())

            else:
                minutes_left = (datetime.fromtimestamp(
                    int(response.json()["detail"])) - datetime.now()).total_seconds() / 60
                await bot.send_message(message.from_user.id,
                                       f"Your dino already on the work. He will finish in {minutes_left} minutes!",
                                       reply_markup=get_default_kb())
        else:
            await bot.send_message(message.from_user.id, "Something went wrong", reply_markup=get_default_kb())

    else:
        await bot.send_message(message.from_user.id, "You are not registered")


if __name__ == '__main__':
    executor.start_polling(dp)
