from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database.base import Base
import app.enums.ticket as ticket_enums

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    customerName = Column(String, index=True)
    customerEmail = Column(String)
    status = Column(String, default=ticket_enums.TicketStatus.OPEN)
    priority = Column(String, default=ticket_enums.TicketPriority.LOW)
    createdAt = Column(DateTime, default=datetime.utcnow)
