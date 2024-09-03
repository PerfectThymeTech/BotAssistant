from typing import List

from pydantic import BaseModel


class FileInfo(BaseModel):
    file_name: str
    file_path: str


class UserData:
    def __init__(self, thread_id: str = None, vector_store_ids: List[str] = []) -> None:
        self.thread_id = thread_id
        self.vector_store_ids = vector_store_ids


# class UserData(BaseModel):
#     thread_id: str | None = None
#     vector_store_ids: List[str] = []
