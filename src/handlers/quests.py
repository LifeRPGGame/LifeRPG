import aiogram

from . import *
from utils.exceptions import *


router = Router()


# -------------------------------------------------------------------------
# See quest
@router.callback_query(QuestAction.filter(F.action == 'see_quest'))
async def see_one_quest(query: types.CallbackQuery, callback_data: QuestAction):
	quest_id = callback_data.quest_id

	under_quest_kb = InlineKeyboardBuilder()
	under_quest_kb.row(
		types.InlineKeyboardButton(
			text='✅ Finish',
			callback_data=QuestAction(action='finish_quest', quest_id=quest_id).pack(),
		)
	)
	under_quest_kb.row(
		types.InlineKeyboardButton(
			text='🗑️ Delete',
			callback_data=QuestAction(action='delete_quest', quest_id=quest_id).pack()
		)
	)

	quest = await QuestOrm().get_quest(quest_id=quest_id)
	q_type = getattr(quest, 'type')

	if q_type == 'easy':
		type_emoji = '☀'
		type_name = 'Easy'
	elif q_type == 'middle':
		type_emoji = '👾'
		type_name = 'Middle'
	elif q_type == 'boss':
		type_emoji = '👹'
		type_name = 'Boss'

	await query.message.answer(
		text=f'''
<b>📌 Quest</b>
Name: {getattr(quest, 'name')} {type_emoji}
Type: {type_name}

Benefits: {getattr(quest, 'benefits')}
''',    reply_markup=under_quest_kb.as_markup(),
		parse_mode=ParseMode.HTML,
	)


#########################################################################
# Delete a quest
@router.callback_query(QuestAction.filter(F.action == 'delete_quest'))
async def delete_quest(query: types.CallbackQuery, callback_data: QuestAction):
	await QuestOrm().delete(quest_id=callback_data.quest_id)
	await query.answer('✅ Successfully deleted')
	await query.message.delete()


##########################################################################
# Adding a quest
class AddingQuest(StatesGroup):
	"""
	Class for processing adding quest
	"""
	start = State()
	to_get_name = State()
	to_get_type = State()
	to_get_benefits = State()


# -------------------------------------------------------------------------
# Add quest
@router.callback_query(QuestAction.filter(F.action == 'add_quest'))
async def add_quest(
		query: types.CallbackQuery,
		callback_data: QuestAction,
		state: FSMContext,
	):
	await state.clear()
	await state.set_state(AddingQuest.start)
	text = '''
Let`s go!

The first field is name.
Most popular: clean-up home, do homework, do exercise, clear desk, walk.

💡 By the way, it is not necessary to name the quest in simple words. 
You can also call it game words, let's say "Preparing for battle" 
(which, let's say, means breakfast)

So, type your quest name:
'''
	location_id = callback_data.location_id
	await state.update_data(location_id=location_id)
	await query.message.answer(
		text=text
	)
	await state.set_state(AddingQuest.to_get_name)


@router.message(F.text, AddingQuest.to_get_name)
async def get_name(message: types.Message, state: FSMContext):
	try:
		name = message.text
		await state.update_data(name=name)

		if len(name) >= 50:
			raise QuestNameIsLong

	except QuestNameIsLong:
		await message.answer(
			text='Sorry, the name is too long. Try again with Map button'
		)
		return

	types_kb = InlineKeyboardBuilder()
	types_kb.row(
		types.InlineKeyboardButton(
			text='☀ Easy',
			callback_data=f'type_is_easy'
		)
	)
	types_kb.row(
		types.InlineKeyboardButton(
			text='👾 Middle',
			callback_data=f'type_is_middle'
		)
	)
	types_kb.row(
		types.InlineKeyboardButton(
			text='👺 Boss',
			callback_data=f'type_is_boss'
		)
	)

	await message.answer(
		text='''
The second field is the type.
The type is the degree of difficulty of the quest.

☀ The easy quest in the game: a Easy mob, 
the reward is small, but regular execution 
strengthens the character. That is, if you don't do 
it, you won't get hurt, but the reward will be small. 
Example: <code>10 push-ups</code>, <code>clear desk</code>

👾 The Middle quest is the Middle mob in the game world. 
The damage will already be serious, but the reward will 
also be more valuable.
Example: <code>learn 10 foreign words</code>, <code>1 hr studying</code>

👺 The Boss quest - maximum damage and maximum awards
In real life: A huge goal that requires long preparation 
and great willpower, but if you do it, it's a huge breakthrough.
Example: <code>finish a project</code>, <code>win the marathon</code>, <code>complete 1-st chapter of course</code>

So, select the type:
''',    reply_markup=types_kb.as_markup(),
		parse_mode=ParseMode.HTML
		)
	await state.set_state(AddingQuest.to_get_type)


@router.callback_query(F.data.startswith('type_is_'), AddingQuest.to_get_type)
async def get_type(query: types.CallbackQuery, state: FSMContext):
	type = query.data.split('_')[-1]
	await state.update_data(type=type)

	await query.message.answer(
		text='''
The last field is the benefits.

💡 Benefits are the results from the quest, 
i.e. what you get after completing it. 

For example, if the task “Project” - it is 
quite possible to add benefits as coins 
(that is, the game character will get coins, 
and you in real life - money)

So, type the benefits:
''',    reply_markup=await benefits_kb()
	)
	await state.set_state(AddingQuest.to_get_benefits)


@router.callback_query(F.data.startswith('benefits_'), AddingQuest.to_get_benefits)
async def get_benefits(query: types.CallbackQuery, state: FSMContext, bot: aiogram.Bot):
	async def test_display_quest(query: types.CallbackQuery, q_name: str) -> dict:
		"""
		Test to display the task.

		The user can write a long name and telegram will not be able to send the keyboard
		"""
		test_kb = InlineKeyboardBuilder()
		test_kb.row(
			types.InlineKeyboardButton(
				text=f'{q_name} 👾',
				callback_data=f'test_{q_name}'
			)
		)
		try:
			test_msg = await query.message.answer(
				text=f'Quest test {q_name} 👾',
				reply_markup=test_kb.as_markup()
			)
			await test_msg.delete()
			return {
				'result': True,
				'error': None
			}
		except Exception as e:
			return {
				'result': True,
				'error': str(e)
			}

	benefits = query.data.split('_')[-1]
	await state.update_data(benefits=benefits)
	data = await state.get_data()

	res = await test_display_quest(query, data['name'])
	if res:
		await QuestOrm().add(
			user_id=query.from_user.id,
			name=data['name'],
			location_id=data['location_id'],
			type=data['type'],
			benefits=data['benefits'],
		)
		await bot.delete_messages(
			chat_id=query.message.chat.id,
			message_ids=[
				query.message.message_id,
				query.message.message_id - 1,
				query.message.message_id - 2,
				query.message.message_id - 3,
			]
		)
		await query.message.answer(
			text='✅ The quest successfully added!'
		)
		await state.clear()
	else:
		await query.message.answer(
			text=f'😥 Sorry, the quest not added.\nError: {res['error']}'
		)
		await state.clear()
