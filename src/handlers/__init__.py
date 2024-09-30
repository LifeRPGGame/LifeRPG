from aiogram import types
from typing import Optional
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters.callback_data import CallbackData

from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardMarkup
from aiogram.types import URLInputFile, FSInputFile

from kb.kb import *
from kb.inline import *

from utils.other.emoji import send_emoji
from utils.db.user import UserOrm
from utils.db.location import LocationOrm
from utils.db.quest import QuestOrm
from utils.db.item import ItemOrm
from utils.db.inventory import InventoryOrm