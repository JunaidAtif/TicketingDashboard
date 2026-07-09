from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from app.models.ticket import Ticket
from app.schemas.ticket.request import TicketCreate, TicketUpdate

class TicketRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, status: Optional[str] = None, priority: Optional[str] = None, search: Optional[str] = None) -> List[Ticket]:
        query = self.db.query(Ticket)
        if status:
            query = query.filter(Ticket.status == status)
        if priority:
            query = query.filter(Ticket.priority == priority)
        if search:
            query = query.filter(
                or_(
                    Ticket.title.ilike(f"%{search}%"),
                    Ticket.customerName.ilike(f"%{search}%")
                )
            )
        return query.all()

    def get_by_id(self, ticket_id: int) -> Optional[Ticket]:
        return self.db.query(Ticket).filter(Ticket.id == ticket_id).first()

    def create(self, ticket: TicketCreate) -> Ticket:
        db_ticket = Ticket(**ticket.model_dump())
        self.db.add(db_ticket)
        self.db.commit()
        self.db.refresh(db_ticket)
        return db_ticket

    def update(self, db_ticket: Ticket, update_data: TicketUpdate) -> Ticket:
        update_dict = update_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(db_ticket, key, value)
        self.db.commit()
        self.db.refresh(db_ticket)
        return db_ticket
