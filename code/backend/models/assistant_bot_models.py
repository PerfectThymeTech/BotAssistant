from typing import List

from pydantic import BaseModel


class FileInfo(BaseModel):
    file_name: str
    file_path: str


class UserData(BaseModel):
    thread_id: str
    vector_store_id: List[str]
