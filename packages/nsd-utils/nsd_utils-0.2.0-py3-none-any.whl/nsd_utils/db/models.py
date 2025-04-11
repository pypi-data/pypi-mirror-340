# nsd_utils/db/models.py

from pydantic import BaseModel
from nsd_utils.db.crud import TableModel

class UserModel(TableModel):
    user_id: int
    username: str
    balance: float = 0

    @classmethod
    def table_name(cls):
        return "users"

    @classmethod
    def primary_key(cls):
        return "user_id"
