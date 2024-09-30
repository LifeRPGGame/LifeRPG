from . import *


router = Router()


class AddLocation(StatesGroup):
	to_get_name = State()


@router.message(Command('add_location'))
async def add_location(msg: types.Message, state: FSMContext):
	await msg.answer(
		text='''
💡 A location is a projection of the 
real place of  your life into the game. 
For example, the game location "Home" is a 
reflection of your real-life home.

Popular: Home, Work, School, Gym, Park

So, if you want to do a real-life task - 
you can add it is in your game location. 
For example, if you wanted to clean the 
house in real life, you could make reflections 
of that task as a quest in the game

So, type a location name:
'''
	)
	await state.set_state(AddLocation.to_get_name)


@router.message(F.text, AddLocation.to_get_name)
async def get_name(msg: types.Message, state: FSMContext):
	await LocationOrm().add(
		user_id=msg.from_user.id,
		name=msg.text,
	)
	await msg.answer(
		text='✅ Successfully added'
	)
	await state.clear()


# ------------------------------
# View locations
@router.callback_query(F.data.startswith('location_'))
async def see_location(call: types.CallbackQuery, state: FSMContext):
	location_id = int(call.data.split('_')[1])
	location = await LocationOrm().get_by_id(location_id=location_id)

	await call.message.answer(
		text=f'''
🧭 Location: {getattr(location, 'name')}

⭐ Level: 1
🔹 Experience: 0 points
✴ Boosters: None

'''
	)