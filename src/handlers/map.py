from . import *


router = Router()


@router.message(F.text == '🗺 Map')
async def map_handler(message: types.Message):
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
			text='Select location:',
			reply_markup=await locations_kb(user_id=message.from_user.id)
		)