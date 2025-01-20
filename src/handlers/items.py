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
		await message.answer(
			text='Item unknown…',
			reply_markup=profile_kb)
		return

	if not in_inventory:
		await message.answer(
			text="I can't see an item that isn't in my inventory…",
			reply_markup=profile_kb
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
''',            parse_mode=ParseMode.HTML,
				reply_markup=profile_kb
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
			text='Item unknown…',
			reply_markup=profile_kb
		)
		return

	if not in_inventory:
		await message.answer(
			text="I can't use an item that isn't in my inventory…",
			reply_markup=profile_kb)
		return

	inventory_item = await ItemOrm().get(item_id=item_id)
	user = await UserOrm().get(user_id=message.from_user.id)
	match getattr(inventory_item, 'type'):
		case 'food':
			if user.hearts + inventory_item.heal <= user.max_hearts:
				await InventoryOrm().remove_from_inventory(
					user_id=message.from_user.id,
					hash_id=inventory_hash_id
				)
				await UserOrm().plus_value(user_id=message.from_user.id,  hearts=user.hearts)
				await message.answer(
					text=f'''
Used: {getattr(inventory_item, 'name')}
Result: +{getattr(inventory_item, 'heal')}❤
	''',    reply_markup=profile_kb
				)
			else:
				await message.answer(
					text='You have full hearts!',
					reply_markup=profile_kb
				)


@router.message(F.text.startswith('/del_'))
async def delete_item(message: types.Message):
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
			text='Item unknown…',
			reply_markup=profile_kb
		)
		return

	if not in_inventory:
		await message.answer(
			text="I can't use an item that isn't in my inventory…",
			reply_markup=profile_kb)
		return

	inventory_item = await ItemOrm().get(item_id=item_id)
	await InventoryOrm().remove_from_inventory(
		user_id=message.from_user.id,
		hash_id=inventory_hash_id
	)
	await message.answer(
		text=f'''
Item deleted: {getattr(inventory_item, 'name')}
	''', reply_markup=profile_kb
	)
