from typing import List
from pydantic import BaseModel


class AttachmentResult(BaseModel):
    success: bool = False
    vector_store_ids: List[str] = []
