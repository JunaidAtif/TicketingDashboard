from pydantic import ConfigDict, Field
from datetime import datetime
from app.enums.ticket import TicketStatus
from app.schemas.ticket.base import TicketBase

class TicketResponse(TicketBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: TicketStatus
    createdAt: datetime
