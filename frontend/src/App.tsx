import { useAuth } from './hooks/useAuth';
import Dashboard from './pages/Dashboard';
import LoginPage from './pages/LoginPage';

function App() {
  const { isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return <LoginPage />;
  }

  return <Dashboard />;
}

export default App;
