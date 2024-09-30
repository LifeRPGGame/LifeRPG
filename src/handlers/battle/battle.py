from .. import *
from utils.battle import *

router = Router()


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


