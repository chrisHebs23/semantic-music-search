from pydantic import BaseModel
from uuid import UUID

class TrackCreate(BaseModel):

    title: str
    artist: str
    description: str
    
class TrackResponse(BaseModel):
    id: UUID | None = None
    title: str
    artist: str
    description: str