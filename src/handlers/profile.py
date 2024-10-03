from . import * 


router = Router()


@router.message(F.text == '👤 Profile')
async def profile(message: types.Message, state: FSMContext):

    user = await UserOrm().get(user_id=message.from_user.id)
    await message.answer_photo(
        photo=FSInputFile(
            'images/hero.png'
        ),
        caption=f'''
Username: @{message.from_user.username}
ID: <code>{message.from_user.id}</code>     
   
<b>PROFILE</b>
🌟 Level: {getattr(user, 'level')}
🌀 Experience: {getattr(user, 'experience')}

❤ ️Health: {getattr(user, 'hearts')}/{getattr(user, 'max_hearts')} points
⚡ Power: {getattr(user, 'power')}/{getattr(user, 'max_power')} points
💰 Money: {getattr(user, 'money')}
''',    parse_mode=ParseMode.HTML,
        reply_markup=profile_kb
    )


@router.message(F.text == '🎽 Equipment')
async def see_equipment(message: types.Message, state: FSMContext):

    await message.answer(
        text='''
<b>EQUIPMENT</b>
🗡️ Weapon: <code>None</code>
🪖 Helmet: <code>None</code>
👕 Armor: <code>None</code>
🩳 Pants: <code>None</code>
🥾 Boots: <code>None</code>
🗡️ Weapon: <code>None</code>
<i>Unwear all clothes:</i> /unwear
<i>Sell all clothes:</i> /s_wear''',
        parse_mode=ParseMode.HTML,
        reply_markup=equipment_kb
    )


@router.message(F.text == '🍎 Food')
async def see_food(message: types.Message, state: FSMContext):
    inventory_foods = await InventoryOrm().get_inventory_of_type(user_id=message.from_user.id, type='food')
    print(inventory_foods)
    foods_display = ''

    for f in inventory_foods:
        name = getattr(await ItemOrm().get(item_id=f.item_id), 'name')
        item_id = getattr(await ItemOrm().get(item_id=f.item_id), 'id')

        foods_display += f'''
{name} <i>🍴: /use_{f.hash_id}</i> <i>ℹ: /info_{item_id}</i>'''

    await message.answer(
        text=f'''
🍎 Food({len(inventory_foods)}/10):
{foods_display if foods_display != '' else '<i>No food...</i>'}
''',
        parse_mode=ParseMode.HTML,
        reply_markup=food_kb
)