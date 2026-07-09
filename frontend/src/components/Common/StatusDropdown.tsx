import React from 'react';

interface Props {
  status: 'Open' | 'In Progress' | 'Resolved';
  onChange: (newStatus: 'Open' | 'In Progress' | 'Resolved') => void;
  disabled?: boolean;
}

export const StatusDropdown: React.FC<Props> = ({ status, onChange, disabled }) => {
  return (
    <select
      value={status}
      onChange={(e) => onChange(e.target.value as any)}
      disabled={disabled}
      onClick={(e) => e.stopPropagation()}
      style={{ 
        width: 'auto', 
        padding: '0.25rem 0.5rem', 
        fontSize: '0.75rem',
        background: 'rgba(15, 23, 42, 0.8)',
        borderColor: 'rgba(255,255,255,0.1)'
      }}
    >
      <option value="Open">Open</option>
      <option value="In Progress">In Progress</option>
      <option value="Resolved">Resolved</option>
    </select>
  );
};
