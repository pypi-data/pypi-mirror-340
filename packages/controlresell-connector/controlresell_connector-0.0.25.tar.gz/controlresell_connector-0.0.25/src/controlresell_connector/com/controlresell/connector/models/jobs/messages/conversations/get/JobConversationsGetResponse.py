from pydantic import BaseModel
from controlresell_connector.com.controlresell.connector.models.jobs.messages.conversations.JobConversation import JobConversation
from controlresell_connector.com.controlresell.connector.models.jobs.orders.JobOrder import JobOrder
from typing import Optional

class JobConversationsGetResponse(BaseModel):
    conversation: JobConversation
    order: Optional[JobOrder] = None
