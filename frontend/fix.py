import os

replacements = {
    "src/api/ticketApi.ts": [
        ("import { Ticket, TicketCreate, TicketUpdate }", "import type { Ticket, TicketCreate, TicketUpdate }")
    ],
    "src/components/Auth/Login.tsx": [
        ("import api from '../api'", "import { authApi } from '../../api/authApi'"),
        ("const response = await api.post('/auth/token', formData, {", "const response = await authApi.login(username, password);"),
        ("headers: { 'Content-Type': 'application/x-www-form-urlencoded' }", ""),
        ("});", ""),
        ("localStorage.setItem('token', response.data.access_token);", "localStorage.setItem('token', response.access_token);")
    ],
    "src/components/Ticket/KanbanBoard.tsx": [
        ("import { Ticket, TicketStatus } from '../types'", "import type { Ticket, TicketStatus } from '../../types/ticket'"),
        ("import api from '../api'", "import { ticketApi } from '../../api/ticketApi'"),
        ("await api.patch(`/tickets/${ticketId}`, { status: newStatus })", "await ticketApi.updateTicket(ticketId, { status: newStatus })"),
        ("const response = await api.get<Ticket[]>('/tickets/')", "const response = await ticketApi.getTickets()"),
        ("setTickets(response.data)", "setTickets(response)")
    ],
    "src/components/Ticket/TicketDetails.tsx": [
        ("import { Ticket, TicketStatus } from '../types'", "import type { Ticket, TicketStatus } from '../../types/ticket'"),
        ("import api from '../api'", "import { ticketApi } from '../../api/ticketApi'"),
        ("import { StatusDropdown } from './StatusDropdown'", "import { StatusDropdown } from '../Common/StatusDropdown'"),
        ("await api.patch(`/tickets/${ticket.id}`, { description: editedDescription })", "await ticketApi.updateTicket(ticket.id, { description: editedDescription })")
    ],
    "src/components/Ticket/TicketForm.tsx": [
        ("import { TicketCreate } from '../types'", "import type { TicketCreate } from '../../types/ticket'")
    ],
    "src/components/Ticket/TicketList.tsx": [
        ("import { Ticket, TicketStatus } from '../types'", "import type { Ticket, TicketStatus } from '../../types/ticket'"),
        ("import { StatusDropdown } from './StatusDropdown'", "import { StatusDropdown } from '../Common/StatusDropdown'"),
        ("newStatus: any", "newStatus: TicketStatus")
    ],
    "src/hooks/useTickets.ts": [
        ("import { Ticket, TicketCreate, TicketUpdate }", "import type { Ticket, TicketCreate, TicketUpdate }"),
        ("import { useState, useEffect, useCallback }", "import { useState, useCallback }")
    ],
    "src/pages/Dashboard.tsx": [
        ("import KanbanBoard from '../components/Ticket/KanbanBoard'", "import { KanbanBoard } from '../components/Ticket/KanbanBoard'"),
        ("import TicketList from '../components/Ticket/TicketList'", "import { TicketList } from '../components/Ticket/TicketList'")
    ],
    "src/pages/LoginPage.tsx": [
        ("import Login from '../components/Auth/Login'", "import { Login } from '../components/Auth/Login'")
    ]
}

for filepath, reps in replacements.items():
    with open(filepath, 'r') as f:
        content = f.read()
    for old, new in reps:
        content = content.replace(old, new)
    with open(filepath, 'w') as f:
        f.write(content)
print("Done")
