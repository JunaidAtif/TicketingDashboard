export type TicketStatus = "Open" | "In Progress" | "Resolved";
export type TicketPriority = "Low" | "Medium" | "High";

export interface Ticket {
    id: number;
    title: string;
    description: string;
    customerName: string;
    customerEmail: string;
    status: TicketStatus;
    priority: TicketPriority;
    createdAt: string;
}

export interface TicketCreate {
    title: string;
    description: string;
    customerName: string;
    customerEmail: string;
    priority: TicketPriority;
}

export interface TicketUpdate {
    status?: TicketStatus;
    priority?: TicketPriority;
    description?: string;
}
