from aiogram import types
from typing import Optional
from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup
)
from aiogram.filters.callback_data import CallbackData

from utils.db.location import LocationOrm
from utils.db.quest import QuestOrm


class QuestAction(CallbackData, prefix='quest'):
    action: str
    location_id: Optional[int] = None


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


async def locations_kb(user_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    locations = await LocationOrm().get_user_locations(user_id=user_id)
    print(f'user locations is {locations}')

    for l in locations:
        builder.row(
            types.InlineKeyboardButton(
                text=getattr(l, 'name'),
                callback_data=f'location_{getattr(l, 'id')}'
            )
        )
    return builder.as_markup()


async def benefits_kb() -> InlineKeyboardMarkup:
    benefits = {
        '🎓 Intelligence': 'intelligence',
        '🏋️‍♂️ Power': 'power',
        '💰 Coins': 'coins',
        '👁️‍🗨️ Observation': 'observation',
        '🧘‍♀️ Resting': 'resting',
        '👥 Socialite': 'socialite',
        '🧹 Comfort': 'comfort'
    }

    builder = InlineKeyboardBuilder()
    for n, c in benefits.items():
        builder.row(
            types.InlineKeyboardButton(
                text=n,
                callback_data=f'benefits_{c}'
            )
        )
    return builder.as_markup()


async def under_location_kb(location_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    quests = await QuestOrm().get_location_quests(location_id=location_id)
    print(f'quests is {quests}')
    for q in quests:
        if q.type == 'easy':
            type = '☀️ '
        elif q.type == 'middle':
            type = '👾'
        elif q.type == 'boss':
            type = '👹'

        builder.row(
            types.InlineKeyboardButton(
                text=f'{q.name} {type}',
                callback_data=QuestAction(action='see_quest', quest_id=q.id).pack()
            )
        )

    builder.row(
        types.InlineKeyboardButton(
            text='➕ Quest',
            callback_data=QuestAction(action='add_quest', location_id=location_id).pack()
        )
    )
    return builder.as_markup()
