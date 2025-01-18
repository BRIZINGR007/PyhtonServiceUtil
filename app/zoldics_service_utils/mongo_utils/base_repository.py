from pymongo.collection import Collection
from typing import Optional, Type
from mongoengine import Document
from pymongo.client_session import ClientSession

from ..mongo_utils.transactions import mongo_session_context


class BaseRepository:
    @staticmethod
    def _get_session() -> Optional[ClientSession]:
        return mongo_session_context.get()

    @staticmethod
    def _get_collection(model_class: Type[Document]) -> Collection:
        return model_class._get_collection()
