from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardMarkup

# ------------------------
# Главное меню
main_kb = [
        [ 
            types.KeyboardButton(text='👤 Profile'),
            types.KeyboardButton(text='🗺 Map'),
            types.KeyboardButton(text='⚙️ Settings')
        ]
    ]
menu_kb = ReplyKeyboardMarkup(
    keyboard=main_kb,
    resize_keyboard=True,
    input_field_placeholder='Select move'
)

# ------------------------
# Меню профиля
profile_buttons = [
    [
        types.KeyboardButton(text='🎽 Equipment'),
        types.KeyboardButton(text='🍎 Food')
    ],
    [
        types.KeyboardButton(text='🔙 Menu')
    ]
]
profile_kb = ReplyKeyboardMarkup(
    keyboard=profile_buttons,
    resize_keyboard=True,
    input_field_placeholder='Select move'
)

# ------------------------
# Меню экипировки
equipment_buttons = [
    [
        types.KeyboardButton(text='👤 Profile')
    ]
]
equipment_kb = ReplyKeyboardMarkup(
    keyboard=equipment_buttons,
    resize_keyboard=True,
    input_field_placeholder='Select move'
)

# ------------------------
# Меню пищи
food_buttons = [[
    types.KeyboardButton(text='👤 Profile')

]]
food_kb = ReplyKeyboardMarkup(
    keyboard=food_buttons,
    resize_keyboard=True,
    input_field_placeholder='Select move'
)