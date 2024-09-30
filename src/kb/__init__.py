from typing import Optional
from aiogram.filters.callback_data import CallbackData

from utils.db.user import UserOrm
from utils.db.location import LocationOrm
from utils.db.quest import QuestOrm


class QuestAction(CallbackData, prefix='quest'):
    action: str
    location_id: Optional[int] = None
