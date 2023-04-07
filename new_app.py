
TOKEN = '6074124143:AAHcv54FEPMV6d1sFYi4tev3ueaxnwm9lco'
PROJECT_NAME = 'valery-bot'

from aiogram import executor, types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.callback_data import CallbackData
import logging


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
cb = CallbackData('ikb','action')

shopping_cart = []

welcome_msg = "Welcome to our airsoft shop. to start shopping press /start!"
photo_filename = 'https://www.sheknows.com/wp-content/uploads/2018/08/fajkx3pdvvt9ax6btssg.jpeg'


#@dp.message_handler(IsUser(), commands='menu')
# the decorator above uses `filters` API
# `filters` API allows you to receive the same message
# but run a different handler
#
#

@dp.message_handler(commands='user_menu')
async def user_menu(message: types.Message):
    print(dict(message))
    markup = ReplyKeyboardMarkup(selective=True)
    markup.add("show catalog")
    markup.add("balance", "orders")
    markup.add("show all current orders")
    await message.answer("", reply_markup=markup)


@dp.message_handler(commands='test_photo')
async def test_photo(message: types.Message):
    print(dict(message))
    price = 2
    idx = ''
    product_cb = CallbackData('product', 'id', 'action')
    markup_cb = InlineKeyboardMarkup(2)
    btn_1 = InlineKeyboardButton(f'להוסיף לסל - {price}₽', callback_data=product_cb.new(id='', action='add'))
    btn_2 = InlineKeyboardButton(f'להוריד מהסל - {price}₽', callback_data=product_cb.new(id='', action='add'))
    markup_cb.add(btn_1, btn_2)
    markup = ReplyKeyboardMarkup(selective=True)
    markup.add("show catalog")
    markup.add("balance", "orders")
    markup.add("show all current orders")
    await message.answer_photo(photo_filename, reply_markup=markup_cb)

@dp.message_handler(text="sub 1")
async def sub_product(message: types.Message):
    product_cb = CallbackData('product', 'id', 'action') 
    btn_1 = InlineKeyboardButton(f'להוסיף לסל - {price}₽', callback_data=product_cb.new(id='', action='add'))
    btn_2 = InlineKeyboardButton(f'להוריד מהסל - {price}₽', callback_data=product_cb.new(id='', action='add'))
    markup = InlineKeyboardMarkup()
    markup.add(btn_1, btn_2)
    await message.answer(photo_filename, reply_markup=markup)
#set for each product 2 price button, separate each with if. 
@dp.callback_query_handler(text = ["pic 1", "pic 2"])
async def sub_product(call: types.CallbackQuery):
    print(dp.callback_query)
    price = 2
    price_vip = 1
    product_cb = CallbackData('product', 'id', 'action') 
    btn_1 = InlineKeyboardButton(f'להוסיף לסל רגיל - {price}₪', callback_data=cb.new('sub1'))
    btn_2 = InlineKeyboardButton(f'להוסיף לסל VIP - {price_vip}₪', callback_data=cb.new('sub2'))
    ikb = InlineKeyboardMarkup()
    ikb.add(btn_1, btn_2)
    
    await call.message.answer(photo_filename, reply_markup=ikb)
#this function processing actions into shopping cart    
@dp.callback_query_handler(cb.filter())
async def add_to_cart(callback: types.CallbackQuery, callback_data: dict):
    if callback_data['action'] == 'sub1':
        shopping_cart.append('sub1')
        print("adddddded")
    if callback_data['action'] == 'sub2':
        print("VIPPPPP")

#another function should remove products from shopping cart
@dp.message_handler(text="קטגוריה 1")
async def first_category(message: types.Message):
    sub_cb = CallbackData('product','id','action')
    sub_product1 = InlineKeyboardButton(f'sub 1', callback_data="pic 1")
    sub_product2 = InlineKeyboardButton(f'sub 2', callback_data="pic 2")
    sub_product3 = InlineKeyboardButton(f'sub 3', callback_data=sub_cb.new(id='', action='add'))
    sub_product4 = InlineKeyboardButton(f'sub 4', callback_data=sub_cb.new(id='', action='add'))
    sub_product5 = InlineKeyboardButton(f'sub 5', callback_data=sub_cb.new(id='', action='add'))
    sub_product6 = InlineKeyboardButton(f'sub 6', callback_data=sub_cb.new(id='', action='add'))
    ikb = InlineKeyboardMarkup()
    ikb.add(sub_product1)
    ikb.add(sub_product2)
    ikb.add(sub_product3)
    ikb.add(sub_product4)
    ikb.add(sub_product5)
    ikb.add(sub_product6)
    await message.answer('category 1', reply_markup=ikb)
@dp.message_handler(text="catalog")
async def user_mode(message: types.Message):
    """תחבר בבקשה בקטגוריה הרצויה"""
    product_list = ['קטגוריה 1','קטגוריה 2','קטגוריה 3','קטגוריה 4', 'קטגוריה 5', 'קטגוריה 6', 'קטגוריה 7', 'קטגוריה 8']

    markup = ReplyKeyboardMarkup(selective=True)
    for product in product_list:
        markup.add(product)
    await message.answer('בחרו בקטגוריה הרצויה', reply_markup=markup)
   

#in here we should accumulate all the button togles that were made



#fist command start - displays 2 buttons - user, admin
'''
i would like to do only one button, but first i would like to send a message to the customer
'''
@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("catalog", "shopping cart", "membership")
    await message.answer(welcome_msg, reply_markup=markup)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
