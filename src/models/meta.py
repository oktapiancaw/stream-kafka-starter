from typing import Optional

from pydantic import BaseModel, Field


# ? Change this
class MessageDTO(BaseModel):
    data: Optional[str] = Field(None)
