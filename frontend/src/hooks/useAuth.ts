import { useState, useEffect } from 'react';
import { authApi } from '../api/authApi';

export const useAuth = () => {
    const [isAuthenticated, setIsAuthenticated] = useState<boolean>(!!localStorage.getItem('token'));

    useEffect(() => {
        const handleAuthChange = () => {
            setIsAuthenticated(!!localStorage.getItem('token'));
        };
        window.addEventListener('auth-change', handleAuthChange);
        return () => window.removeEventListener('auth-change', handleAuthChange);
    }, []);

    const login = async (username: string, password: string) => {
        const data = await authApi.login(username, password);
        localStorage.setItem('token', data.access_token);
        setIsAuthenticated(true);
        window.dispatchEvent(new Event('auth-change'));
    };

    const logout = () => {
        localStorage.removeItem('token');
        setIsAuthenticated(false);
        window.dispatchEvent(new Event('auth-change'));
    };

    return { isAuthenticated, login, logout };
};
