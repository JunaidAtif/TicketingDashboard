import React from 'react';
import type { Ticket } from '../../types/ticket';
import { StatusDropdown } from '../Common/StatusDropdown';

interface Props {
  tickets: Ticket[];
  onTicketClick: (id: number) => void;
  onStatusChange: (id: number, status: 'Open' | 'In Progress' | 'Resolved') => void;
}

export const TicketList: React.FC<Props> = ({ tickets, onTicketClick, onStatusChange }) => {
  if (tickets.length === 0) {
    return (
      <div style={{ textAlign: 'center', padding: '4rem 2rem', color: 'var(--text-secondary)' }} className="glass-panel">
        <h3 style={{ marginBottom: '0.5rem', color: 'var(--text-primary)' }}>No tickets found</h3>
        <p>There are currently no tickets matching your criteria.</p>
      </div>
    );
  }

  return (
    <div className="ticket-grid">
      {tickets.map((ticket, i) => (
        <div 
          key={ticket.id} 
          className={`ticket-card glass-panel delay-${(i % 3) + 1} animate-fade-in`}
          onClick={() => onTicketClick(ticket.id)}
        >
          <div className="ticket-card-header">
            <span className={`badge badge-status-${ticket.status.toLowerCase().replace(' ', '-')}`}>
              {ticket.status}
            </span>
            <span className={`badge badge-priority-${ticket.priority.toLowerCase()}`}>
              {ticket.priority}
            </span>
          </div>
          
          <h3 className="ticket-title">{ticket.title}</h3>
          
          <div className="ticket-meta">
            <span>{ticket.customerName}</span>
            <span style={{ marginLeft: 'auto' }}>
              {new Date(ticket.createdAt).toLocaleDateString()}
            </span>
          </div>
          
          <div style={{ marginTop: '1rem' }}>
            <StatusDropdown 
              status={ticket.status} 
              onChange={(newStatus) => onStatusChange(ticket.id, newStatus)} 
            />
          </div>
        </div>
      ))}
    </div>
  );
};
