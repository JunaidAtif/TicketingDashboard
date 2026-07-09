from typing import List, Optional
from fastapi import APIRouter, Depends, status
from app.schemas.ticket.request import TicketCreate, TicketUpdate
from app.schemas.ticket.response import TicketResponse
from app.services.ticket_service import TicketService
from app.api.dependencies import get_ticket_service, get_current_user
from app.models.user import User
from app.enums.ticket import TicketStatus, TicketPriority

router = APIRouter(prefix="/tickets", tags=["tickets"], dependencies=[Depends(get_current_user)])

@router.get("/", response_model=List[TicketResponse])
def get_tickets(
    status: Optional[TicketStatus] = None, 
    priority: Optional[TicketPriority] = None, 
    search: Optional[str] = None,
    service: TicketService = Depends(get_ticket_service)
):
    return service.get_all_tickets(status=status, priority=priority, search=search)

@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(
    ticket_id: int, 
    service: TicketService = Depends(get_ticket_service)
):
    return service.get_ticket(ticket_id)

@router.post("/", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
def create_ticket(
    ticket: TicketCreate, 
    service: TicketService = Depends(get_ticket_service)
):
    return service.create_ticket(ticket)

@router.patch("/{ticket_id}", response_model=TicketResponse)
def update_ticket(
    ticket_id: int, 
    ticket_update: TicketUpdate, 
    service: TicketService = Depends(get_ticket_service)
):
    return service.update_ticket(ticket_id, ticket_update)
