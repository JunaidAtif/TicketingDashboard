import { DragDropContext, Droppable, Draggable } from '@hello-pangea/dnd';
import type { DropResult } from '@hello-pangea/dnd';
import type { Ticket } from '../../types/ticket';

interface KanbanBoardProps {
  tickets: Ticket[];
  onTicketClick: (id: number) => void;
  onStatusChange: (id: number, status: 'Open' | 'In Progress' | 'Resolved') => void;
}

const COLUMNS: { id: 'Open' | 'In Progress' | 'Resolved'; title: string }[] = [
  { id: 'Open', title: 'Open' },
  { id: 'In Progress', title: 'In Progress' },
  { id: 'Resolved', title: 'Resolved' },
];

export function KanbanBoard({ tickets, onTicketClick, onStatusChange }: KanbanBoardProps) {
  const handleDragEnd = (result: DropResult) => {
    const { destination, source, draggableId } = result;

    if (!destination) return;

    if (
      destination.droppableId === source.droppableId &&
      destination.index === source.index
    ) {
      return;
    }

    const ticketId = parseInt(draggableId, 10);
    const newStatus = destination.droppableId as 'Open' | 'In Progress' | 'Resolved';

    onStatusChange(ticketId, newStatus);
  };

  return (
    <DragDropContext onDragEnd={handleDragEnd}>
      <div className="kanban-board">
        {COLUMNS.map((column) => {
          const columnTickets = tickets.filter(t => t.status === column.id);
          
          return (
            <div key={column.id} className="kanban-column glass-panel">
              <h3 className="column-title">{column.title} <span className="column-count">{columnTickets.length}</span></h3>
              
              <Droppable droppableId={column.id}>
                {(provided, snapshot) => (
                  <div
                    ref={provided.innerRef}
                    {...provided.droppableProps}
                    className={`kanban-droppable ${snapshot.isDraggingOver ? 'dragging-over' : ''}`}
                  >
                    {columnTickets.map((ticket, index) => (
                      <Draggable key={ticket.id} draggableId={ticket.id.toString()} index={index}>
                        {(provided, snapshot) => (
                          <div
                            ref={provided.innerRef}
                            {...provided.draggableProps}
                            {...provided.dragHandleProps}
                            className={`ticket-card glass-panel kanban-card ${snapshot.isDragging ? 'is-dragging' : ''}`}
                            onClick={() => onTicketClick(ticket.id)}
                            style={{ ...provided.draggableProps.style }}
                          >
                            <div className="ticket-card-header">
                              <span className={`badge badge-priority-${ticket.priority.toLowerCase()}`}>
                                {ticket.priority}
                              </span>
                            </div>
                            <h4 className="ticket-title">{ticket.title}</h4>
                            <div className="ticket-meta">
                              <span>#{ticket.id}</span>
                              <span>•</span>
                              <span>{ticket.customerName}</span>
                            </div>
                          </div>
                        )}
                      </Draggable>
                    ))}
                    {provided.placeholder}
                  </div>
                )}
              </Droppable>
            </div>
          );
        })}
      </div>
    </DragDropContext>
  );
}
