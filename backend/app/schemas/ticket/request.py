from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional
from app.enums.ticket import TicketStatus, TicketPriority
from app.schemas.ticket.base import TicketBase
from app.validators.string_validators import strip_and_validate_not_blank, reject_empty_strings

class TicketCreate(TicketBase):
    _strip_whitespace = field_validator("title", "description", "customerName", mode="before")(strip_and_validate_not_blank)

class TicketUpdate(BaseModel):
    status: Optional[TicketStatus] = None
    priority: Optional[TicketPriority] = None
    description: Optional[str] = Field(None, min_length=1, max_length=5000)

    _reject_empty = field_validator("status", "priority", "description", mode="before")(reject_empty_strings)

    @model_validator(mode='after')
    def check_at_least_one_field(self):
        if not any(v is not None for v in [self.status, self.priority, self.description]):
            raise ValueError("At least one field must be provided for update")
        return self
