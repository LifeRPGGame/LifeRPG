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


