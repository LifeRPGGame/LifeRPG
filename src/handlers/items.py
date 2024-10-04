from . import *


router = Router()


@router.message(F.text.startswith('/info'))
async def see_info_about_item(message: types.Message):
	try:
		item_id = int(message.text.split('_')[1])
		in_inventory = await InventoryOrm().item_in_inventory(
			user_id=message.from_user.id,
			item_id=item_id
		)

	except:
		await message.answer(text='Item unknown…')
		return

	if not in_inventory:
		await message.answer(
			text="I can't see an item that isn't in my inventory…"
		)
		return

	item = await ItemOrm().get(item_id=item_id)
	match getattr(item, 'type'):
		case 'food':
			await message.answer(
				text=f'''
🥩 Food: {getattr(item, 'name')}
{getattr(item, 'description')}

<b>Heal:</b> +{getattr(item, 'heal')} ❤
<b>Price:</b> {getattr(item, 'price')} 💰
	''',           parse_mode=ParseMode.HTML
				)


@router.message(F.text.startswith('/use'))
async def use_item(message: types.Message):
	try:
		inventory_hash_id = int(message.text.split('_')[1])
		inventory_item = await InventoryOrm().get_inventory_item(hash_id=inventory_hash_id)
		item_id = getattr(inventory_item, 'item_id')
		in_inventory = await InventoryOrm().item_in_inventory(
			user_id=message.from_user.id,
			hash_id=inventory_hash_id
		)
	except:
		await message.answer(
			text='Item unknown…'
		)
		return
	print(f'inventory_hash_id {inventory_hash_id}')
	print(f'item_id {item_id}')
	print(f'in_inventory {in_inventory}')

	if not in_inventory:
		await message.answer(text="I can't use an item that isn't in my inventory…")
		return

	inventory_item = await ItemOrm().get(item_id=item_id)
	match getattr(inventory_item, 'type'):
		case 'food':
			await InventoryOrm().remove_from_inventory(
				user_id=message.from_user.id,
				hash_id=inventory_hash_id
			)
			await message.answer(
				text=f'''
Used: {getattr(inventory_item, 'name')}
Result: +{getattr(inventory_item, 'heal')}❤
''')