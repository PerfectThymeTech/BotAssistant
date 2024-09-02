from pydantic import BaseModel


class FileInfo(BaseModel):
    file_name: str
    file_path: str
