from pydantic import BaseModel
from uuid import UUID
from controlresell_connector.com.controlresell.connector.models.jobs.orders.JobOrder import JobOrder
from typing import Optional

class JobConversationsGetPayload(BaseModel):
    accountId: UUID
    conversationId: str
    order: Optional[JobOrder] = None
