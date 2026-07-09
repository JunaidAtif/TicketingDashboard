import api from './axios';
import type { Ticket, TicketCreate, TicketUpdate } from '../types/ticket';

export const ticketApi = {
    getTickets: async (search?: string) => {
        const params = new URLSearchParams();
        if (search) params.append('search', search);
        const response = await api.get<Ticket[]>(`/tickets/?${params.toString()}`);
        return response.data;
    },
    
    getTicket: async (id: number) => {
        const response = await api.get<Ticket>(`/tickets/${id}`);
        return response.data;
    },
    
    createTicket: async (ticket: TicketCreate) => {
        const response = await api.post<Ticket>('/tickets/', ticket);
        return response.data;
    },
    
    updateTicket: async (id: number, ticket: TicketUpdate) => {
        const response = await api.patch<Ticket>(`/tickets/${id}`, ticket);
        return response.data;
    }
};
