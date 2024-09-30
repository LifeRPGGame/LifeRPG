from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.keyboard import InlineKeyboardMarkup

from kb import *
from utils.db.location import LocationOrm


async def locations_kb(user_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    locations = await LocationOrm().get_user_locations(user_id=user_id)

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
