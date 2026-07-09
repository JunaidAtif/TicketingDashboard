from typing import List, Optional
from app.repositories.ticket_repository import TicketRepository
from app.schemas.ticket.request import TicketCreate, TicketUpdate
from app.models.ticket import Ticket
from app.core.exceptions import NotFoundException

class TicketService:
    def __init__(self, repository: TicketRepository):
        self.repository = repository

    def get_all_tickets(self, status: Optional[str] = None, priority: Optional[str] = None, search: Optional[str] = None) -> List[Ticket]:
        return self.repository.get_all(status, priority, search)

    def get_ticket(self, ticket_id: int) -> Ticket:
        ticket = self.repository.get_by_id(ticket_id)
        if not ticket:
            raise NotFoundException(detail="Ticket not found")
        return ticket

    def create_ticket(self, ticket: TicketCreate) -> Ticket:
        return self.repository.create(ticket)

    def update_ticket(self, ticket_id: int, ticket_update: TicketUpdate) -> Ticket:
        db_ticket = self.get_ticket(ticket_id)
        return self.repository.update(db_ticket, ticket_update)
