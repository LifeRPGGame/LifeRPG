import random
import asyncio

from utils.db.user import UserOrm


# Класс персонажа
class Character:
	def __init__(
			self,
			user_id: int,
			username: str = None
	):
		self.username = username
		self.hearts = (asyncio.run(UserOrm().get(user_id=user_id))).hearts
		self.attack = 0

	def is_alive(self):
		return self.hearts > 0

	def take_damage(self, damage):
		self.hearts -= damage

	def attack_mob(self, mob):
		damage = random.randint(1, self.attack)
		mob.take_damage(damage)
		return damage


# Класс моба
class Mob:
	def __init__(self, name, hp, attack):
		self.name = name
		self.hp = hp
		self.attack = attack

	def is_alive(self):
		return self.hp > 0

	def take_damage(self, damage):
		self.hp -= damage

	def attack_character(self, character):
		damage = random.randint(1, self.attack)
		character.take_damage(damage)
		return damage


# Класс боя
class Battle:
	def __init__(self, player, mob):
		self.player = player
		self.mob = mob

	def player_turn(self):
		damage = self.player.attack_mob(self.mob)
		return f"🧔‍ {self.player.username} 🔪 🧟 {self.mob.username} ({damage} 💥)"

	def mob_turn(self):
		damage = self.mob.attack_character(self.player)
		return f"🧟 {self.mob.username} 🔪 🧔 {self.player.username} ({damage} 💥)"

	def check_winner(self):
		if not self.player.is_alive():
			return f"💀 {self.player.username} вы были убиты!"
		elif not self.mob.is_alive():
			return f"🎉 {self.mob.username} враг побежден!"
		return None


# Хранение текущих сражений
active_battles = {}


# Функции для управления боями
def create_battle(player_name):
	player = Character(name=player_name, hp=100, attack=20)
	mob = Mob(name="Зомби", hp=50, attack=10)
	battle = Battle(player, mob)
	return battle


def start_battle(user_id, player_name):
	if user_id in active_battles:
		return "У тебя уже есть активный бой. Напиши /attack, чтобы ударить"
	else:
		battle = create_battle(player_name)
		active_battles[user_id] = battle
		return f"Начался бой! {player_name} против {battle.mob.username}! Ударь моба командой /attack."


def attack(user_id) -> str | None:
	if user_id not in active_battles:
		return "У тебя нет активного боя. Напиши /fight, чтобы начать."

	battle = active_battles[user_id]

	# Ход игрока
	player_message = battle.player_turn()

	# Проверка победителя после атаки игрока
	winner = battle.check_winner()
	if winner:
		del active_battles[user_id]
		return f"{player_message}\n{winner}"

	# Ход моба
	mob_message = battle.mob_turn()

	# Проверка победителя после атаки моба
	winner = battle.check_winner()
	if winner:
		del active_battles[user_id]
		return f"{player_message}\n{mob_message}\n{winner}"

	# Если бой продолжается
	return f"{player_message}\n{mob_message}"

