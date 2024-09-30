from . import *


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
		type = '☀'
	elif q_type == 'middle':
		type = '👾'
	elif q_type == 'boss':
		type = '👹'

	await query.message.answer(
		text=f'''
📌 Quest: {getattr(quest, 'name')} 
Type: {type}

Benefits: {getattr(quest, 'benefits')}
'''
	)


##########################################################################

class AddingQuest(StatesGroup):
	"""
	Class for processing adding quest
	"""
	to_get_name = State()
	to_get_type = State()
	to_get_benefits = State()


# -------------------------------------------------------------------------
# Add quest
@router.callback_query(QuestAction.filter(F.action == 'add_quest'))
async def add_quest(query: types.CallbackQuery, callback_data: QuestAction, state: FSMContext):
	await state.clear()

	location_id = callback_data.location_id
	await state.update_data(location_id=location_id)

	await query.message.answer(
		text='''
Let`s go!

The first field is name.
Most popular: clean-up home, do homework, do exercise, clear desk, walk.

💡 By the way, it is not necessary to name the quest in simple words. 
You can also call it game words, let's say "Preparing for battle" 
(which, let's say, means breakfast)

So, type your quest name:
'''
	)
	await state.set_state(AddingQuest.to_get_name)


@router.message(F.text, AddingQuest.to_get_name)
async def get_name(message: types.Message, state: FSMContext):
	name = message.text
	await state.update_data(name=name)

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

☀️A simple type of task in real life is a habit. 
That is, if you don't do it, you won't get hurt, 
but the reward will be small. In the game: 
A Easy mob, the reward is small, but regular 
execution strengthens the character.
Example: 10 push-ups, clear-desk

👾 The Middle quest is the Middle mob in the game world. 
The damage will already be serious, but the reward will 
also be more valuable.
Example: learn 10 foreign words, 1 hr studying

👺 The Boss quest - maximum damage and maximum awards
In real life: A huge goal that requires long preparation 
and great willpower, but if you do it, it's a huge breakthrough.
Example: finish a project, win the marathon, complete 1-st chapter of course

So, select the type:
'''
	)
	await state.set_state(AddingQuest.to_get_type)


@router.callback_query(F.data.startswith('type_is_', AddingQuest.to_get_type))
async def get_type(query: types.CallbackQuery, callback_data: str, state: FSMContext):
	type = query.data.split('_')[-1]
	await state.update_data(type=type)

	await query.message.answer(
		text='''
The last field is the benefits.

💡Benefits are the results from the quest, 
i.e. what you get after completing it. 
For example, if the task “Project” - it is 
quite possible to add benefits as coins 
(that is, the game character will get coins, 
and you in real life - money)

So, type the benefits:
''',    reply_markup=await benefits_kb()
	)
	await state.set_state(AddingQuest.to_get_benefits)


@router.callback_query(F.data.startswith('benefits_', AddingQuest.to_get_benefits))
async def get_benefits(query: types.CallbackQuery, callback_data: str, state: FSMContext):
	benefits = callback_data.split('_')[-1]
	await state.update_data(benefits=benefits)

	data = await state.get_data()
	await QuestOrm().add(
		user_id=query.from_user.id,
		name=data['name'],
		location_id=data['location_id'],
		type=data['type'],
		benefits=data['benefits'],
	)

	await query.message.answer(
		text='✅ The quest successfully added!'
	)
	await state.clear()


