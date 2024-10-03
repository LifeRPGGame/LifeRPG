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
<b>YOUR LIFE IS A GAME 🎭 = 🕹</b>.

You can easily turn real life 
into 📍 RPG quests.
 
By doing which you can finish 
the real thing, but also get 
object reward for your game 
Character: gold, experience points, swords, etc.

Also call your 👥 friends in the team
and play life more fun! 
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
<i>Emptiness... 
But this is only the beginning of something great....

It's time to create your first location with /add_location</i>''',
            parse_mode=ParseMode.HTML
        )
    else:
        await message.answer(
            text='Select a location below or create a new one with /add_location',
            reply_markup=await locations_kb(user_id=message.from_user.id)
        )


@router.message(F.text == '⚙️ Settings')
async def settings_handler(message: types.Message, state: FSMContext):
    await state.clear()

    await message.answer(
        text='There are the settings!'
    )
