TOKEN = '1305342821:AAHUh-gq8ospT7vKvHIsnxiKrNKnSwcyFe0'
PROJECT_NAME = 'valery-bot'
#
#6074124143:AAHcv54FEPMV6d1sFYi4tev3ueaxnwm9lco
import datetime
from collections import defaultdict
from dataclasses import dataclass


from aiogram import executor, types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, InputFile
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types.inline_query_result import InlineQueryResultPhoto
from aiogram.utils.callback_data import CallbackData
import logging

#1. start doesnt work
#2. menu doesnt work
#3. product price doesnt do anything
#4. better fix menu then the buttons below



'''
def a(x, y, a = 0, b = 2): x + y

args = [1, 2]
kwargs = {'a': 1, 'b': 2}
a(*args, **kwargs)


def dbrows_to_dataclass(rows, klass):
    return [klass(*row) for row in rows]


#with this classes i can create one handler for all of the classes
@dataclass
class Product():
    pid: int = 0
    price: float = 0.0
    name: str = ''
    image: str = ''
    category_id: int = 0
    


@dataclass
class Order():
    oid: int
    uid: int
    pid: int
    created: datetime.datetime
    updated: datetime.datetime
    paid: bool
    processed: bool
    delivered: bool

'''
user_products = defaultdict(list)

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
cb = CallbackData('ikb','action')


#product = Product(id=1, price=11.0, name='p11', image='')


from typing import List

p_by_cats = {'c1': {
    1: ('p1', 1.0, 'p1.img'),
}}

products_by_category = {'category1': {'product11': (11, 'product11.jpeg'),
                                      'product12': (12, 'product12.jpeg'),
                                      'product13': (13, 'product13.jpeg')},
                        'category2': {'product21': (21, 'product21.jpeg'),
                                      'product22': (22, 'product22.jpeg'),
                                      'product23': (23, 'product23.jpeg')},
                        'category3': {'product31': (31, 'product31.jpeg'),
                                      'product32': (32, 'product32.jpeg'),
                                      'product33': (33, 'product33.jpeg')}}

shopping_cart = []

welcome_msg = "Welcome to our airsoft shop. Use the buttons below to browse the shop!"
photo_filename1 = 'https://www.sheknows.com/wp-content/uploads/2018/08/fajkx3pdvvt9ax6btssg.jpeg'
photo_filename = 'brownie.jpeg'


#1. callback that adds products to cart(dict) - finished
#2. cart page that displays all products in cart, and sums the price - 
#3. function that removes the clicked product
#4. display a photo on every product clicked
#5. 
'''
async def product_callback_handler(query: CallbackQuery):
    product_info = query.data.split("_")
    product_name = product_info[0]
    product_price = product_info[1]
    photo_filename = product_info[2]
    
    user_id = query.from_user.id
    user_products[user_id].append((product_name, product_price))

    message_text = f"You have selected {product_name} for {product_price}."
    print(user_products)
    await query.message.answer(message_text)
    
    photo = InputFile(photo_filename)
    caption = f"{product_name} very very - {product_price}"
    message = await bot.send_photo(chat_id=query.from_user.id, photo=photo, caption=caption)
    message_link = f"https://t.me/{PROJECT_NAME}/{message.message_id}"
    await bot.answer_callback_query(query.id, text="Going to the selected product.", show_alert=True, url=message_link)
   
'''

def create_product_keyboard(products):
    keyboard = InlineKeyboardMarkup()
    for product in products:
        product_name = product
        product_price, photo_filename = products[product]
        callback_data = f"{product_name}_{product_price}_{photo_filename}"
        button_text = f"{product_name} - {product_price}"
        button = InlineKeyboardButton(button_text, callback_data=callback_data)
        keyboard.add(button)
    return keyboard

def get_products_for_category(category):
    dict_of_products = products_by_category[category]
    return dict_of_products

async def category_button_handler(query: CallbackQuery, state: FSMContext):
    category = query.data
    products = get_products_for_category(category)
    print(products)
    keyboard = create_product_keyboard(products)
    message_text = f"Please select a product from the {category} category:"
    await query.message.answer(message_text, reply_markup=keyboard, disable_notification=False)

@dp.callback_query_handler(lambda query: query.data.startswith('product'))
async def handle_product_callback_query(query: CallbackQuery):
    
    product_info = query.data.split("_")
    product_name = product_info[0]
    product_price = product_info[1]
    photo_filename = product_info[2]
    user_id = query.from_user.id
    user_products[user_id].append((product_name, product_price))
    photo = InputFile(photo_filename)
    caption = "Add to cart price according to plan. Add discription according to needs"
    # Create the inline keyboard
    
    keyboard = InlineKeyboardMarkup()
    button_regular = InlineKeyboardButton(f'Regular Price - {product_price}₪', callback_data=f'price_{product_price}')
    button_vip = InlineKeyboardButton(f'VIP Price - {product_price}₪', callback_data=f'price_{product_price}')
    keyboard.add(button_regular, button_vip)
    
    await query.message.answer_photo(photo, caption=caption, reply_markup=keyboard, disable_notification=False)

@dp.callback_query_handler(lambda query: query.data in ['category1', 'category2', 'category3'])
async def handle_category_button(query: CallbackQuery, state: FSMContext):
    await category_button_handler(query, state)



@dp.message_handler(text="catalog")
async def catalog(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    categories = ['category1', 'category2', 'category3']
    for category in categories:
        callback_data = category
        button = InlineKeyboardButton(category, callback_data=callback_data)
        keyboard.add(button)

    message_text = "Please select a category to start shopping:"
    await message.answer(message_text, reply_markup=keyboard, disable_notification=False)

@dp.message_handler(text="catalog")
async def process_category(callback_query: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup()
    categories = ['category1', 'category2', 'category3']
    for category in categories:
        callback_data = category
        button = InlineKeyboardButton(category, callback_data=callback_data)
        keyboard.add(button)

    message_text = "Please select a category to start shopping:"
    await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text=message_text, reply_markup=keyboard, scroll_offset=len(subcategories))


@dp.message_handler(text="shopping cart")
async def shopping_cart(message: types.Message):
    uid = message.from_user.id
    if uid in user_products:
        msg = "You chose the following products:\n"
        total_price = 0
        for order_tuple in user_products[uid]:
            product_name = order_tuple[0]
            product_price = order_tuple[1]
            msg += f"{product_name} for {product_price}₪\n"
            total_price += int(product_price)
        msg += f"\nTotal price: {total_price}₪"
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("Check out", "Go back")
        await message.answer(msg, reply_markup=markup)
    else:
        await message.answer("Your shopping cart is empty")



@dp.message_handler(text="membership")
async def membership(message: types.Message):
    msg = "We have plans and promotions for you\n you can join our vip club or renew your membership here"
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("Renew", "Join", "Go back")
    await message.answer(msg, reply_markup=markup)
# Function to generate the menu

async def generate_menu(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("catalog", "shopping cart", "membership")
    await message.answer(welcome_msg, reply_markup=markup)

# Handler for the start command
@dp.message_handler(commands=['start','catalog','cart'])
async def cmd_start(message: types.Message):
    await generate_menu(message)

# Handler for the "Go back" button
@dp.message_handler(text='Go back')
async def go_back(message: types.Message):
    await generate_menu(message)
    
    




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
