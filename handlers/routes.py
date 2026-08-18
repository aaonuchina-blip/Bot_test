import aiohttp
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    BufferedInputFile,
    FSInputFile
)
from sqlalchemy import lambda_stmt
from forms.user import Form
from aiogram.fsm.context import FSMContext
import aiosqlite
import asyncio


router = Router()

subscribers = set()
async def notifier(bot: Bot):
    while True:
        if subscribers:
            for user_id in list(subscribers):
                try:
                    await bot.send_message(user_id, 'Пробуем рассылку')
                except Exception:
                    pass

        await asyncio.sleep(10)


@router.message(Command('start'))
async def start(message: Message):
    await message.answer(
        "Привет!\n"
        "Я могу помочь с рассылкой\n"
        "Команды:\n"
        "/subscribe - подписаться на уведомления\n\n"
        "/unsubscrube - отписка\n\n"
        "/subscribers - список подписчиков\n\n"
    )

@router.message(Command('subscribe'))
async def subscribe(message: Message):
    user_id = message.from_user.id

    subscribers.add(user_id)

    await message.answer("Вы подписаны!")

@router.message(Command('unsubscribe'))
async def unsubscribe(message: Message):
    user_id = message.from_user.id

    subscribers.discard(user_id)

    await message.answer("Вы отписаны от подписки!")

@router.message(Command('subscribers'))
async def subscribers_cmd(message: Message):
    if not subscribers:
        await message.answer('Пока никого нет')
        return
    text = "Подписчики: \n"
    for us_id in subscribers:
        text += f'{us_id}\n'
    await message.answer(text)

#Работа с MYsql
# DB_NAME = 'bot1.sql'
#
# async def init_db():
#     async with aiosqlite.connect(DB_NAME) as db:
#         await db.execute("""
#             CREATE TABLE IF NOT EXISTS users (
#                             id INTEGER PRIMARY KEY,
#                             full_name TEXT,
#                             age INTEGER
#         )
#         """)
#         await db.commit()
#
# async def add_user(full_name, age):
#     async with aiosqlite.connect(DB_NAME) as db:
#         await db.execute("INSERT INTO users (full_name, age) VALUES(?, ?)", (full_name, age))
#         await db.commit()
#
# async def get_users():
#     async with aiosqlite.connect(DB_NAME) as db:
#         cursor = await db.execute("SELECT full_name, age FROM users")
#         result = await cursor.fetchall()
#         return result
#
# @router.message(Command('start'))
# async def start(message: Message):
#     await init_db()
#     await message.answer('Добрый день\nПропишите команду: /reg AGE')
#
# @router.message(Command('reg'))
# async def reg(message: Message):
#     parts = message.text.strip().split()
#
#     if len(parts) != 2 or not parts[1].isdigit():
#         await message.answer('Введите команду верно')
#         return
#     await add_user(message.from_user.full_name, int(parts[1]))
#     await message.answer('Все готово!')
#
# @router.message(Command('users'))
# async def users(message: Message):
#     users = await get_users()
#
#     if not users:
#         await message.answer('В базе нет пользователей')
#         return
#     text = 'Пользователи в базе\n\n'
#     for full_name, age in users:
#         text += f'- {full_name} - <code>{age}</code>\n'
#     await message.answer(text, parse_mode='HTML')

# Работаем с АПИ
# async def get_product(product_id):
#     url = f'http://fakestoreapi.com/products/{product_id}'
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as resp:
#             if resp.status == 404:
#                 return None
#             data = await resp.json()
#             return data
#
# async def download_image(url):
#     """Скачивает изображение по ссылке и возвращает байты"""
#     async with aiohttp.ClientSession() as session:
#         try:
#             async with session.get(url, timeout=10) as resp:
#                 if resp.status == 200:
#                     return await resp.read()
#         except Exception:
#             return None
#     return None
#
# @router.message(Command("start"))
# async def start(message: Message):
#     await message.answer(
#         "Привет! Я простой бот магазин\n"
#         "Введите команду: /product ID\n\n"
#         "Пример: <b>/product 1</b>",
#         parse_mode='HTML'
#     )
#
# @router.message(Command("product"))
# async def get_product_cmd(message: Message):
#     parts = message.text.strip().split()
#
#     if len(parts) != 2:
#         await message.answer("Используйте: /product 1")
#         return
#
#     product_id = parts[1]
#     if not product_id.isdigit():
#         await message.answer("ID товара должен быть числом")
#         return
#
#     await message.answer(f'Ищу товар с id: {product_id}')
#
#     try:
#         product = await get_product(int(product_id))
#     except Exception:
#         await message.answer('Не удалось обратиться к серверу')
#         return
#
#     if product is None:
#         await message.answer('Такого товара нет')
#         return
#
#     title = product.get('title', 'Без названия')
#     price = product.get('price', '-')
#     desc = product.get('description', 'Без описания')
#     category = product.get('category', 'Без категории')
#     image = product.get('image')
#
#     text = (
#         f'<b>{title}</b>\n\n'
#         f'Категория: <i>{category}</i>\n'
#         f'Цена: <b>{price}$</b>\n\n'
#         f'{desc}'
#     )
#
#     if image:
#         # Пробуем отправить по прямой ссылке
#         try:
#             await message.answer_photo(photo=image, caption=text, parse_mode='HTML')
#         except Exception as e:
#             # Если ссылка не работает — скачиваем и отправляем как файл
#             image_data = await download_image(image)
#             if image_data:
#                 # 🔥 КЛЮЧЕВОЙ МОМЕНТ: оборачиваем байты в BufferedInputFile
#                 photo_file = BufferedInputFile(image_data, filename="product.jpg")
#                 await message.answer_photo(photo=photo_file, caption=text, parse_mode='HTML')
#             else:
#                 await message.answer(text, parse_mode='HTML')
#     else:
#         await message.answer(text, parse_mode='HTML')




    # Заполнение и сохранение от пользователя анкеты

# @router.message(Command("start"))
# async def start(message: Message, state: FSMContext):
#     await message.answer("Давайте знакомиться!\nСперва введите ваше имя:")
#     await state.set_state(Form.name)
#
# @router.message(Command('cansel'))
# async def cancel_form(message: Message, state: FSMContext):
#     await state.clear()
#     await message.answer('Анкета отклонена')
#
# @router.message(Form.name, F.text)
# async def proccess_name(message: Message, state: FSMContext):
#     await state.update_data(name=message.text)
#
#     await message.answer("Хорошо!\nА теперь введите ваш возраст:")
#     await state.set_state(Form.age)
#
# @router.message(Form.age, F.text)
# async def proccess_age(message: Message, state: FSMContext):
#     if not message.text.isdigit():
#         await message.answer('Возраст должен быть числлом')
#         return
#     if int(message.text) < 1 or int(message.text) > 100:
#         await message.answer('Возраст должен быть от 1 до 100')
#         return
#
#     await state.update_data(age=int(message.text))
#
#     await message.answer("Хорошо!\nА теперь введите ваш e-mail:")
#     await state.set_state(Form.email)
#
#
# @router.message(Form.email, F.text)
# async def proccess_email(message: Message, state: FSMContext):
#     email_text = message.text
#     if "@" not in email_text or "." not in email_text:
#         await message.answer('Email не корректный')
#         return
#
#     await state.update_data(email=email_text)
#
#     data = await state.get_data()
#     name = data['name']
#     age = data['age']
#     email = data['email']
#
#     await message.answer(f'Анкета готова!\nИмя: {name}\nВозраст: {age}\nПочта: {email} ')
#     await state.clear()

#Сохранение от пользователя фото

# @router.message(F.photo)
# async def proccess_photo(message: Message):
#     photo = message.photo[-1]
#     file_id = photo.file_id
#
#     await message.answer(
#         f'вы отправили фото!\nID photo: <code>{file_id}</code>',
#         parse_mode='HTML'
#     )
#
#     await message.answer_photo(file_id, caption='Вот ваше фото')
#  Сохранение от пользователя документов

# @router.message(F.document)
# async def proccess_document(message: Message, bot: Bot):
#     document = message.document
#     file_id = document.file_id
#
#     file = await bot.get_file(file_id)
#     file_path = file.file_path
#
#     local_path = f'downloads/{document.file_name}'
#
#     await bot.download_file(file_path=file_path, destination=local_path)
#
#     await message.answer('Файл сохранен!')

#  Отправка пользователю файлов
# @router.message(Command('file'))
# async def send_file(message: Message):
#     file = FSInputFile('files/example.txt')
#
#     await message.answer_document(file)

# Работа с книпоками

# def get_main_reply_keyboard():
#     keyboard = ReplyKeyboardMarkup(
#         keyboard=[
#             [KeyboardButton(text='/about')],
#             [KeyboardButton(text="/start"), KeyboardButton(text='/help')]
#         ],
#         resize_keyboard=True
#     )
#     return keyboard
#
# def get_main_inline_keyboard():
#     keyboard = InlineKeyboardMarkup(
#         inline_keyboard=[
#             [InlineKeyboardButton(text='Открыть сайт', url="https://github.com/aaonuchina-blip")],
#             [InlineKeyboardButton(text='Подробнее', callback_data='info_more')]
#     ])
#     return keyboard
#
# @router.callback_query(lambda c: c.data=='info_more')
# async def proccess_more_info(callback: CallbackQuery):
#     await callback.message.answer('Вот более подробная информация')
#     await callback.answer()
#
# @router.message(Command('start'))
# @router.message(F.text.lower() == 'старт')
# async def start(message: Message):
#     await message.answer(
#         'Привет, давай начнем *работу*!\n\nНапиши /help для помощи',
#         parse_mode='Markdown',
#     reply_markup=get_main_reply_keyboard())
#
# @router.message(Command('help'))
# async def help(message: Message):
#     await message.answer(
#         'Команды:\n<b>/start</b> - запустить бот\n<b>/help</b> - список команд\n<b>/about</b> - про нас',
#     parse_mode='HTML')
#
# @router.message(Command('about'))
# async def about(message: Message):
#     await message.answer(f'Это команда про бота. Твое имя: {message.from_user.first_name}',
#                          reply_markup=get_main_inline_keyboard()
#                          )
#
# @router.message()
# async def mess(message: Message):
#     await message.answer('Text message')


