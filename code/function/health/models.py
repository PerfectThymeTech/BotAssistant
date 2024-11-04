from pydantic import BaseModel


class HeartbeatResponse(BaseModel):
    is_alive: bool = True
