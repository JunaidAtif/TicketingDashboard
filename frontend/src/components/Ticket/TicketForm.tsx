import React, { useState } from 'react';
import type { TicketCreate } from '../../types/ticket';

interface Props {
  onSubmit: (data: TicketCreate) => Promise<void>;
  onCancel: () => void;
}

export const TicketForm: React.FC<Props> = ({ onSubmit, onCancel }) => {
  const [formData, setFormData] = useState<TicketCreate>({
    title: '',
    description: '',
    customerName: '',
    customerEmail: '',
    priority: 'Low',
  });
  const [errors, setErrors] = useState<Partial<Record<keyof TicketCreate, string>>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const validate = () => {
    const newErrors: Partial<Record<keyof TicketCreate, string>> = {};
    if (!formData.title) newErrors.title = 'Title is required';
    if (!formData.description) newErrors.description = 'Description is required';
    if (!formData.customerName) newErrors.customerName = 'Customer name is required';
    if (!formData.customerEmail) {
      newErrors.customerEmail = 'Email is required';
    } else if (!/^\S+@\S+\.\S+$/.test(formData.customerEmail)) {
      newErrors.customerEmail = 'Invalid email format';
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validate()) return;
    
    setIsSubmitting(true);
    try {
      await onSubmit(formData);
    } catch (err) {
      console.error(err);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="animate-fade-in">
      <h2 style={{ marginBottom: '1.5rem' }}>Create New Ticket</h2>
      
      <div className="form-group">
        <label>Title</label>
        <input 
          value={formData.title} 
          onChange={e => setFormData({...formData, title: e.target.value})} 
          placeholder="Brief issue summary"
        />
        {errors.title && <div className="form-error">{errors.title}</div>}
      </div>

      <div className="form-group">
        <label>Description</label>
        <textarea 
          rows={4}
          value={formData.description} 
          onChange={e => setFormData({...formData, description: e.target.value})} 
          placeholder="Detailed description of the issue"
        />
        {errors.description && <div className="form-error">{errors.description}</div>}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
        <div className="form-group">
          <label>Customer Name</label>
          <input 
            value={formData.customerName} 
            onChange={e => setFormData({...formData, customerName: e.target.value})} 
          />
          {errors.customerName && <div className="form-error">{errors.customerName}</div>}
        </div>
        
        <div className="form-group">
          <label>Customer Email</label>
          <input 
            type="email"
            value={formData.customerEmail} 
            onChange={e => setFormData({...formData, customerEmail: e.target.value})} 
          />
          {errors.customerEmail && <div className="form-error">{errors.customerEmail}</div>}
        </div>
      </div>

      <div className="form-group">
        <label>Priority</label>
        <select 
          value={formData.priority} 
          onChange={e => setFormData({...formData, priority: e.target.value as any})}
        >
          <option value="Low">Low</option>
          <option value="Medium">Medium</option>
          <option value="High">High</option>
        </select>
      </div>

      <div style={{ display: 'flex', gap: '1rem', justifyContent: 'flex-end', marginTop: '2rem' }}>
        <button type="button" className="btn btn-secondary" onClick={onCancel}>Cancel</button>
        <button type="submit" className="btn btn-primary" disabled={isSubmitting}>
          {isSubmitting ? 'Creating...' : 'Create Ticket'}
        </button>
      </div>
    </form>
  );
};
