from pydantic import BaseModel

class JobConversationOppositeUser(BaseModel):
    id: str
    login: str
    lastLoggedInAt: str
    isSystem: bool
    reviewCount: int
    feedbackReputation: float
    isHated: bool
    profileUrl: str
    locationDescription: str
    isOnHoliday: bool
    isModerator: bool
    isUserUnblockable: bool
