from . import * 

router = Router()


@router.message(Command('start'))
@router.message(F.text == '🔙 Menu')
async def _start(message: types.Message, state: FSMContext):
    await state.clear()

    await UserOrm().add(
        user_id=message.from_user.id,
        username=message.from_user.username,
        full_name=message.from_user.full_name,
    )

    text = '''
<b>YOUR LIFE IS A GAME 🎭 = 🕹</b>

🧟 The world has plunged into chaos, and every day — 
It's a struggle for survival. 

📕 Turn your daily tasks into
exciting RPG quests! And in case of not
completing the real task, feel the taste of defeat,
losing valuable things and reputation!

💣 Create your own locations from the real world,
complete missions, destroy zombies, find
rare items and tune weapons!

🪓 Fight with other survivors in PvP battles
or team up with friends for a joint
passage. In the post-apocalypse, your every action is important!
'''
    await message.answer(
        text=text, 
        parse_mode=ParseMode.HTML, 
        reply_markup=menu_kb
    )


@router.message(F.text == '🗺 Map')
async def map_handler(message: types.Message, state: FSMContext):
    await state.clear()

    locations = await LocationOrm().get_user_locations(user_id=message.from_user.id)
    if not locations:
        await message.answer(
            text='''
<i>There is emptiness all around...</i>

Moreover, I do not know any location,
add it using /add_location''',
            parse_mode=ParseMode.HTML
        )
    else:
        await message.answer(
            text='Where to this time?\nTo add a location - /add_location',
            reply_markup=await locations_kb(user_id=message.from_user.id)
        )


@router.message(F.text == '⚙️ Settings')
async def settings_handler(message: types.Message, state: FSMContext):
    await state.clear()

    await message.answer(
        text='There are the settings!'
    )
