import React from 'react';
import { Login } from '../components/Auth/Login';
import { useAuth } from '../hooks/useAuth';

export const LoginPage: React.FC = () => {
    const { login } = useAuth();
    
    return (
        <Login onLogin={login} />
    );
};

export default LoginPage;
