from typing import List

from pydantic import BaseModel


class FileInfo(BaseModel):
    file_name: str
    file_path: str


class UserData(BaseModel):
    login_succeeded: bool = False
    thread_id: str | None = None
    vector_store_ids: List[str] = []


class ConversationData(BaseModel):
    timestamp: str
    channel_id: str
