from pydantic import BaseModel
from typing import Optional
from controlresell_connector.com.controlresell.connector.models.jobs.posts.JobPostOptionals import JobPostOptionals

class JobPostListed(BaseModel):
    platformId: str
    platformUrl: str
    itemClosingAction: Optional[str] = None
    post: JobPostOptionals
    data: str
