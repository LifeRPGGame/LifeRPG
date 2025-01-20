from .. import *
from utils.battle import *
from utils.db.user import User

router = Router()


@router.message(F.text == '🪓 PvP')
async def pvp_main_handler(message: types.Message):
    await message.answer(
        text='''
Welcome to the PvP! 

Here you can fight with other players or mobs!
Use /start_pvp to fight!
'''
    )


@router.message(Command('start_pvp'))
async def start_pvp(message: types.Message):
    pvp_accept_kb = InlineKeyboardBuilder()
    pvp_accept_kb.row(
        types.InlineKeyboardButton(
            text='⚔ Accept',
            callback_data='pvp_accept'
        ),
        types.InlineKeyboardButton(
            text='❌ Cancel',
            callback_data='pvp_cancel'
        )
    )

    await message.answer(
        text='Finding your opponent...'
    )
    await send_emoji(
        message=message,
        emoji='⏳',
        time=3.5,
        times=5
    )

    opponent = User(
        user_id=3333333,
        username='Pashka',
        level=2,
        power=20,
        hearts=50
    )
    await message.answer(
        text=f'''
Found an opponent:
👤 {opponent.username}
🌟 {opponent.level} | 💪 {opponent.power} | ❤ {opponent.hearts}

Accept the battle? 
''',    reply_markup=pvp_accept_kb.as_markup()
    )


# Команда для начала боя
@router.message(Command('fight'))
async def start_fight(message: types.Message):
    user_id = message.from_user.id
    player_name = message.from_user.first_name

    response = start_battle(user_id, player_name)
    await message.answer(response)


# Команда для атаки
@router.message(Command('attack'))
async def attack_mob(message: types.Message):
    user_id = message.from_user.id
    response = attack(user_id)

    if response:
        messages = response.split('\n')
        msg_1 = messages[0]

        if len(messages) > 1:
            if messages[1].startswith('🎉'):
                await message.answer(messages[1])
            else:
                # print(f'Сообщение 1: {msg_1}')
                await message.answer(messages[0])
                # print(f'Сообщение 2: {messages[1]}')
                await message.answer(messages[1])
        else:
            # print(f'Сообщение 1: {msg_1}')
            await message.answer(messages[0])
