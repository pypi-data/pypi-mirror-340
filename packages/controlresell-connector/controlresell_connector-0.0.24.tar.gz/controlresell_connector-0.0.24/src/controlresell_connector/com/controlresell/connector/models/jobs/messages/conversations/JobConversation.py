from pydantic import BaseModel
from typing import Optional
from controlresell_connector.com.controlresell.connector.models.jobs.messages.JobConversationOppositeUser import JobConversationOppositeUser
from controlresell_connector.com.controlresell.connector.models.jobs.messages.JobConversationTransaction import JobConversationTransaction
from controlresell_connector.com.controlresell.connector.models.jobs.messages.JobConversationMessage import JobConversationMessage

class JobConversation(BaseModel):
    id: str
    url: str
    subtitle: str
    readByCurrentUser: bool
    readByOppositeUser: bool
    localization: Optional[str] = None
    translated: bool
    allowReply: bool
    isSuspicious: bool
    isDeletionRestricted: bool
    userHasSupportRole: bool
    safetyEducation: bool
    oppositeUser: JobConversationOppositeUser
    transaction: Optional[JobConversationTransaction] = None
    messages: list[JobConversationMessage]
