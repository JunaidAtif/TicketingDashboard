import React, { useEffect, useState } from 'react';
import { KanbanBoard } from '../components/Ticket/KanbanBoard';
import { TicketList } from '../components/Ticket/TicketList';
import { useAuth } from '../hooks/useAuth';
import { useTickets } from '../hooks/useTickets';
import type { Ticket, TicketStatus } from '../types/ticket';
import { TicketDetails } from '../components/Ticket/TicketDetails';
import { TicketForm } from '../components/Ticket/TicketForm';

export const Dashboard: React.FC = () => {
    const { logout } = useAuth();
    const { tickets, loading, fetchTickets, updateTicket, createTicket } = useTickets();
    const [view, setView] = useState<'kanban' | 'list'>('kanban');
    const [selectedTicket, setSelectedTicket] = useState<Ticket | null>(null);
    const [showForm, setShowForm] = useState(false);

    useEffect(() => {
        fetchTickets();
    }, [fetchTickets]);

    const handleStatusChange = async (ticketId: number, status: TicketStatus) => {
        await updateTicket(ticketId, { status });
    };

    return (
        <div className="app-container">
            <header>
                <div>
                    <h1>Support Dashboard</h1>
                    <div style={{ marginTop: '0.5rem' }}>
                        <span className="badge" style={{ background: 'rgba(255, 255, 255, 0.1)' }}>Admin</span>
                    </div>
                </div>
                <div>
                    <button 
                        onClick={logout}
                        className="btn btn-secondary"
                    >
                        Sign Out
                    </button>
                </div>
            </header>
            
            <main>
                <div className="dashboard-controls">
                    <div className="filters">
                        <button 
                            className={`btn ${view === 'kanban' ? 'btn-primary' : 'btn-secondary'}`}
                            onClick={() => setView('kanban')}
                        >
                            Board
                        </button>
                        <button 
                            className={`btn ${view === 'list' ? 'btn-primary' : 'btn-secondary'}`}
                            onClick={() => setView('list')}
                        >
                            List
                        </button>
                    </div>
                    <button className="btn btn-primary" onClick={() => setShowForm(true)}>+ New Ticket</button>
                </div>

                {loading && tickets.length === 0 ? (
                    <div className="loading-spinner"></div>
                ) : (
                    view === 'kanban' 
                        ? <KanbanBoard tickets={tickets} onTicketClick={(id) => setSelectedTicket(tickets.find(t => t.id === id) || null)} onStatusChange={handleStatusChange} /> 
                        : <TicketList tickets={tickets} onTicketClick={(id) => setSelectedTicket(tickets.find(t => t.id === id) || null)} onStatusChange={handleStatusChange} />
                )}
            </main>
            
            {showForm && (
                <div className="modal-overlay" onClick={() => setShowForm(false)}>
                    <div className="modal-content glass-panel" onClick={e => e.stopPropagation()}>
                        <TicketForm 
                            onSubmit={async (data) => {
                                await createTicket(data);
                                setShowForm(false);
                            }} 
                            onCancel={() => setShowForm(false)} 
                        />
                    </div>
                </div>
            )}

            {selectedTicket && (
                <div className="modal-overlay" onClick={() => setSelectedTicket(null)}>
                    <div className="modal-content" onClick={e => e.stopPropagation()} style={{ padding: 0, background: 'transparent', border: 'none', boxShadow: 'none' }}>
                        <TicketDetails 
                            ticket={selectedTicket} 
                            onClose={() => setSelectedTicket(null)} 
                            onUpdate={async (updatedTicket) => {
                                await updateTicket(selectedTicket.id, updatedTicket);
                                setSelectedTicket({ ...selectedTicket, ...updatedTicket });
                            }}
                        />
                    </div>
                </div>
            )}
        </div>
    );
};

export default Dashboard;
