# nsd_utils/db/crud.py

import asyncpg
from typing import Optional, Any, TypeVar, Type, Union
from pydantic import BaseModel
from nsd_utils.db.session_manager import get_pool

class TableModel(BaseModel):
    class Config:
        orm_mode = True
    @classmethod
    def table_name(cls):
        raise NotImplementedError()
    @classmethod
    def primary_key(cls):
        return "id"

ModelType = TypeVar("ModelType", bound=TableModel)

class CRUD:
    @staticmethod
    async def create(model_cls: Type[ModelType], **kwargs):
        pool = await get_pool()
        name = model_cls.table_name()
        fields = list(kwargs.keys())
        values = list(kwargs.values())
        placeholders = ", ".join(f"${i+1}" for i in range(len(fields)))
        sql = f"INSERT INTO {name} ({', '.join(fields)}) VALUES ({placeholders}) RETURNING *"
        async with pool.acquire() as conn:
            try:
                row = await conn.fetchrow(sql, *values)
                if row:
                    return model_cls.parse_obj(dict(row))
            except asyncpg.UniqueViolationError:
                return None

    @staticmethod
    async def get(model_cls: Type[ModelType], pk_value: Any, pk_field: Optional[str] = None):
        pool = await get_pool()
        name = model_cls.table_name()
        pk = pk_field or model_cls.primary_key()
        sql = f"SELECT * FROM {name} WHERE {pk}=$1 LIMIT 1"
        async with pool.acquire() as conn:
            row = await conn.fetchrow(sql, pk_value)
            if row:
                return model_cls.parse_obj(dict(row))

    @staticmethod
    async def update(model_cls: Type[ModelType], pk_value: Any, data: dict, pk_field: Optional[str] = None):
        pool = await get_pool()
        name = model_cls.table_name()
        pk = pk_field or model_cls.primary_key()
        fields = list(data.keys())
        values = list(data.values())
        set_expr = ", ".join(f"{field}=${i+1}" for i, field in enumerate(fields))
        sql = f"UPDATE {name} SET {set_expr} WHERE {pk}=${len(values)+1} RETURNING *"
        async with pool.acquire() as conn:
            row = await conn.fetchrow(sql, *values, pk_value)
            if row:
                return model_cls.parse_obj(dict(row))

    @staticmethod
    async def delete(model_cls: Type[ModelType], pk_value: Any, pk_field: Optional[str] = None):
        pool = await get_pool()
        name = model_cls.table_name()
        pk = pk_field or model_cls.primary_key()
        sql = f"DELETE FROM {name} WHERE {pk}=$1"
        async with pool.acquire() as conn:
            result = await conn.execute(sql, pk_value)
            if result.startswith("DELETE"):
                return True
