import { useState, useCallback } from 'react';
import { ticketApi } from '../api/ticketApi';
import type { Ticket, TicketCreate, TicketUpdate } from '../types/ticket';

export const useTickets = () => {
    const [tickets, setTickets] = useState<Ticket[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const fetchTickets = useCallback(async (search?: string) => {
        setLoading(true);
        setError(null);
        try {
            const data = await ticketApi.getTickets(search);
            setTickets(data);
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to fetch tickets');
        } finally {
            setLoading(false);
        }
    }, []);

    const createTicket = async (ticket: TicketCreate) => {
        const newTicket = await ticketApi.createTicket(ticket);
        setTickets(prev => [...prev, newTicket]);
        return newTicket;
    };

    const updateTicket = async (id: number, updates: TicketUpdate) => {
        const updatedTicket = await ticketApi.updateTicket(id, updates);
        setTickets(prev => prev.map(t => (t.id === id ? updatedTicket : t)));
        return updatedTicket;
    };

    return { tickets, loading, error, fetchTickets, createTicket, updateTicket, setTickets };
};
