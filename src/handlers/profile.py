from . import *
from utils.config import get_inventory_count_for_level


router = Router()


@router.message(F.text == '👤 Profile')
async def profile(message: types.Message, state: FSMContext):

    user = await UserOrm().get(user_id=message.from_user.id)
    await message.answer_photo(
        photo=FSInputFile(
            'images/hero.jpg'
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
🔫 Weapon: <code>None</code>

🪖 Helmet: <code>None</code>
👕 Armor: <code>None</code>
🩳 Pants: <code>None</code>
🥾 Boots: <code>None</code>
<i>Unwear all clothes:</i> /unwear
<i>Sell all clothes:</i> /s_wear''',
        parse_mode=ParseMode.HTML,
        reply_markup=equipment_kb
    )


@router.message(F.text == '📦 Inventory')
async def see_all_inventory(message: types.Message, state: FSMContext):
    user = await UserOrm().get(user_id=message.from_user.id)
    max_inventory_count = await get_inventory_count_for_level(user.level)
    print('max_inventory_count', max_inventory_count)
    inventory = await InventoryOrm().get_inventory(user_id=message.from_user.id)
    result = ''

    for item in inventory:
        name = getattr(await ItemOrm().get(item_id=item.item_id), 'name')
        item_id = getattr(await ItemOrm().get(item_id=item.item_id), 'id')
        type = getattr(await ItemOrm().get(item_id=item.item_id), 'type')

        if type == 'food':
            result += f'''
{name} 
<i>🍽 /use_{item.hash_id}</i> 
<i>🗑 /del_{item.hash_id}</i>
<i>ℹ /info_{item_id}</i>
'''

    await message.answer(
        text=f'''
Your inventory({len(inventory)}/{max_inventory_count}):
{result if result != '' else '<i>No items...</i>'}
''',
        parse_mode=ParseMode.HTML,
        reply_markup=food_kb
    )