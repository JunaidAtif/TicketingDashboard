import React, { useState, useEffect } from 'react';
import type { Ticket, TicketUpdate } from '../../types/ticket';
import { StatusDropdown } from '../Common/StatusDropdown';

interface Props {
  ticket: Ticket;
  onClose: () => void;
  onUpdate: (updatedFields: TicketUpdate) => Promise<void>;
}

export const TicketDetails: React.FC<Props> = ({ ticket, onClose, onUpdate }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editDescription, setEditDescription] = useState(ticket.description);
  const [savingDesc, setSavingDesc] = useState(false);

  useEffect(() => {
    setEditDescription(ticket.description);
  }, [ticket.description]);

  const handleStatusChange = async (newStatus: 'Open' | 'In Progress' | 'Resolved') => {
    try {
      await onUpdate({ status: newStatus });
    } catch (err) {
      alert('Failed to update status');
    }
  };

  const handleSaveDescription = async () => {
    setSavingDesc(true);
    try {
      await onUpdate({ description: editDescription });
      setIsEditing(false);
    } catch (err) {
      alert('Failed to update description');
    } finally {
      setSavingDesc(false);
    }
  };

  return (
    <div className="animate-fade-in glass-panel" style={{ padding: '2rem' }}>
      <button className="btn btn-secondary" onClick={onClose} style={{ marginBottom: '1.5rem' }}>
        ← Back to List
      </button>
      
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '2rem' }}>
        <div>
          <h2 style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>{ticket.title}</h2>
          <div style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
            Ticket #{ticket.id} • Created on {new Date(ticket.createdAt).toLocaleString()}
          </div>
        </div>
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <span className={`badge badge-priority-${ticket.priority.toLowerCase()}`}>
            {ticket.priority} Priority
          </span>
          <StatusDropdown status={ticket.status} onChange={handleStatusChange} />
        </div>
      </div>

      <div style={{ background: 'rgba(0,0,0,0.2)', padding: '1.5rem', borderRadius: '0.5rem', marginBottom: '2rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
          <h3 style={{ fontSize: '1rem', color: 'var(--text-secondary)' }}>Description</h3>
          {!isEditing && (
            <button className="btn btn-secondary" style={{ padding: '0.25rem 0.5rem', fontSize: '0.75rem' }} onClick={() => setIsEditing(true)}>
              Edit
            </button>
          )}
        </div>
        
        {isEditing ? (
          <div>
            <textarea 
              value={editDescription}
              onChange={e => setEditDescription(e.target.value)}
              style={{ minHeight: '150px', marginBottom: '1rem' }}
            />
            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <button 
                className="btn btn-primary" 
                onClick={handleSaveDescription}
                disabled={savingDesc}
              >
                {savingDesc ? 'Saving...' : 'Save'}
              </button>
              <button 
                className="btn btn-secondary" 
                onClick={() => {
                  setIsEditing(false);
                  setEditDescription(ticket.description);
                }}
                disabled={savingDesc}
              >
                Cancel
              </button>
            </div>
          </div>
        ) : (
          <p style={{ whiteSpace: 'pre-wrap' }}>{ticket.description}</p>
        )}
      </div>

      <div style={{ borderTop: '1px solid var(--surface-border)', paddingTop: '1.5rem' }}>
        <h3 style={{ marginBottom: '1rem', fontSize: '1rem', color: 'var(--text-secondary)' }}>Customer Details</h3>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
          <div>
            <strong>Name:</strong> {ticket.customerName}
          </div>
          <div>
            <strong>Email:</strong> <a href={`mailto:${ticket.customerEmail}`}>{ticket.customerEmail}</a>
          </div>
        </div>
      </div>
    </div>
  );
};
