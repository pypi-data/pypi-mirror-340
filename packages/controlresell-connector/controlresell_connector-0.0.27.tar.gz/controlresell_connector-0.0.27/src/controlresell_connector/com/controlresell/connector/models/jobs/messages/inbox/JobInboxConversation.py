from pydantic import BaseModel
from datetime import datetime
from controlresell_connector.com.controlresell.connector.models.jobs.messages.inbox.JobConversationInboxOppositeUser import JobConversationInboxOppositeUser
from typing import Optional

class JobInboxConversation(BaseModel):
    id: str
    itemCount: int
    isDeletionRestricted: bool
    description: str
    unread: bool
    updatedAt: datetime
    oppositeUser: Optional[JobConversationInboxOppositeUser] = None
