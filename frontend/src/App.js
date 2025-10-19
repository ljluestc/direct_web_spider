import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from 'react-router-dom';
import { HomeIcon, CogIcon, ChartBarIcon, UserIcon } from '@heroicons/react/24/outline';
import './App.css';

// Components
import Header from './components/Header';
import Footer from './components/Footer';
import Home from './pages/Home';
import Dashboard from './pages/Dashboard';
import Settings from './pages/Settings';
import Profile from './pages/Profile';
import Login from './pages/Login';
import Register from './pages/Register';
import NotFound from './pages/NotFound';
import LoadingSpinner from './components/LoadingSpinner';
import ErrorBoundary from './components/ErrorBoundary';

// Hooks
import { useAuth } from './hooks/useAuth';
import { useSpider } from './hooks/useSpider';

// Utils
import { formatDate, formatNumber, validateEmail, validateURL } from './utils/helpers';

// Services
import { spiderService } from './services/spiderService';
import { authService } from './services/authService';

function App() {
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const { user, login, logout, isAuthenticated } = useAuth();
  const { spiderData, startSpider, stopSpider, isRunning } = useSpider();

  useEffect(() => {
    // Initialize app
    const initializeApp = async () => {
      try {
        setIsLoading(true);
        setError(null);
        
        // Check if user is already logged in
        const token = localStorage.getItem('token');
        if (token) {
          await authService.validateToken(token);
        }
        
        // Initialize spider service
        await spiderService.initialize();
        
      } catch (err) {
        setError(err.message);
        console.error('App initialization error:', err);
      } finally {
        setIsLoading(false);
      }
    };

    initializeApp();
  }, []);

  const handleLogin = async (credentials) => {
    try {
      setError(null);
      await login(credentials);
    } catch (err) {
      setError(err.message);
    }
  };

  const handleLogout = () => {
    logout();
    setError(null);
  };

  const handleSpiderStart = async (config) => {
    try {
      setError(null);
      await startSpider(config);
    } catch (err) {
      setError(err.message);
    }
  };

  const handleSpiderStop = async () => {
    try {
      setError(null);
      await stopSpider();
    } catch (err) {
      setError(err.message);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="large" />
      </div>
    );
  }

  return (
    <ErrorBoundary>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <Header 
            user={user}
            isAuthenticated={isAuthenticated}
            onLogout={handleLogout}
            error={error}
            onClearError={() => setError(null)}
          />
          
          <main className="container mx-auto px-4 py-8">
            <Routes>
              <Route 
                path="/" 
                element={
                  <Home 
                    spiderData={spiderData}
                    isRunning={isRunning}
                    onStartSpider={handleSpiderStart}
                    onStopSpider={handleSpiderStop}
                    error={error}
                  />
                } 
              />
              <Route 
                path="/dashboard" 
                element={
                  <Dashboard 
                    spiderData={spiderData}
                    isRunning={isRunning}
                    onStartSpider={handleSpiderStart}
                    onStopSpider={handleSpiderStop}
                  />
                } 
              />
              <Route 
                path="/settings" 
                element={
                  <Settings 
                    user={user}
                    onUpdateSettings={(settings) => console.log('Update settings:', settings)}
                  />
                } 
              />
              <Route 
                path="/profile" 
                element={
                  <Profile 
                    user={user}
                    onUpdateProfile={(profile) => console.log('Update profile:', profile)}
                  />
                } 
              />
              <Route 
                path="/login" 
                element={
                  <Login 
                    onLogin={handleLogin}
                    error={error}
                  />
                } 
              />
              <Route 
                path="/register" 
                element={
                  <Register 
                    onRegister={(userData) => console.log('Register:', userData)}
                    error={error}
                  />
                } 
              />
              <Route path="*" element={<NotFound />} />
            </Routes>
          </main>
          
          <Footer />
        </div>
      </Router>
    </ErrorBoundary>
  );
}

export default App;
