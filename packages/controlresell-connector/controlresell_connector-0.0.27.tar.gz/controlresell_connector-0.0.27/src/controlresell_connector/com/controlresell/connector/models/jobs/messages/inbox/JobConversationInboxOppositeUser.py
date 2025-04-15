from pydantic import BaseModel
from typing import Optional

class JobConversationInboxOppositeUser(BaseModel):
    id: str
    login: str
    badge: Optional[str] = None
