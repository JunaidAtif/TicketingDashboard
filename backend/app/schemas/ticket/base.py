from pydantic import BaseModel, EmailStr, Field
from app.enums.ticket import TicketStatus, TicketPriority

class TicketBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1, max_length=5000)
    customerName: str = Field(..., min_length=1, max_length=100)
    customerEmail: EmailStr
    priority: TicketPriority
