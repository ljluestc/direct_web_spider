import React from 'react';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import { useAuth } from './hooks/useAuth';
import { useSpider } from './hooks/useSpider';

// Mock the hooks
jest.mock('./hooks/useAuth');
jest.mock('./hooks/useSpider');

// Mock the services
jest.mock('./services/spiderService', () => ({
  spiderService: {
    initialize: jest.fn().mockResolvedValue(),
  },
}));

jest.mock('./services/authService', () => ({
  authService: {
    validateToken: jest.fn().mockResolvedValue(),
  },
}));

// Mock localStorage
const localStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
};
Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
});

describe('App', () => {
  const mockUser = {
    id: 1,
    name: 'Test User',
    email: 'test@example.com',
  };

  const mockSpiderData = {
    totalPages: 100,
    crawledPages: 50,
    errors: 2,
    startTime: new Date().toISOString(),
  };

  beforeEach(() => {
    jest.clearAllMocks();
    localStorageMock.getItem.mockReturnValue(null);
  });

  it('renders loading spinner initially', () => {
    useAuth.mockReturnValue({
      user: null,
      login: jest.fn(),
      logout: jest.fn(),
      isAuthenticated: false,
    });
    useSpider.mockReturnValue({
      spiderData: null,
      startSpider: jest.fn(),
      stopSpider: jest.fn(),
      isRunning: false,
    });

    render(<App />);
    expect(screen.getByTestId('loading-spinner')).toBeInTheDocument();
  });

  it('renders app after loading', async () => {
    useAuth.mockReturnValue({
      user: null,
      login: jest.fn(),
      logout: jest.fn(),
      isAuthenticated: false,
    });
    useSpider.mockReturnValue({
      spiderData: null,
      startSpider: jest.fn(),
      stopSpider: jest.fn(),
      isRunning: false,
    });

    render(<App />);
    
    await waitFor(() => {
      expect(screen.queryByTestId('loading-spinner')).not.toBeInTheDocument();
    });
    
    expect(screen.getByText('Direct Web Spider')).toBeInTheDocument();
  });

  it('handles authentication state', async () => {
    const mockLogin = jest.fn();
    const mockLogout = jest.fn();
    
    useAuth.mockReturnValue({
      user: mockUser,
      login: mockLogin,
      logout: mockLogout,
      isAuthenticated: true,
    });
    useSpider.mockReturnValue({
      spiderData: mockSpiderData,
      startSpider: jest.fn(),
      stopSpider: jest.fn(),
      isRunning: false,
    });

    render(<App />);
    
    await waitFor(() => {
      expect(screen.getByText('Test User')).toBeInTheDocument();
    });
  });

  it('handles spider operations', async () => {
    const mockStartSpider = jest.fn();
    const mockStopSpider = jest.fn();
    
    useAuth.mockReturnValue({
      user: null,
      login: jest.fn(),
      logout: jest.fn(),
      isAuthenticated: false,
    });
    useSpider.mockReturnValue({
      spiderData: mockSpiderData,
      startSpider: mockStartSpider,
      stopSpider: mockStopSpider,
      isRunning: true,
    });

    render(<App />);
    
    await waitFor(() => {
      expect(screen.getByText('Crawling in progress...')).toBeInTheDocument();
    });
  });

  it('handles errors during initialization', async () => {
    const { spiderService } = require('./services/spiderService');
    spiderService.initialize.mockRejectedValue(new Error('Initialization failed'));

    useAuth.mockReturnValue({
      user: null,
      login: jest.fn(),
      logout: jest.fn(),
      isAuthenticated: false,
    });
    useSpider.mockReturnValue({
      spiderData: null,
      startSpider: jest.fn(),
      stopSpider: jest.fn(),
      isRunning: false,
    });

    render(<App />);
    
    await waitFor(() => {
      expect(screen.getByText('Initialization failed')).toBeInTheDocument();
    });
  });

  it('handles login with valid token', async () => {
    localStorageMock.getItem.mockReturnValue('valid-token');
    
    useAuth.mockReturnValue({
      user: mockUser,
      login: jest.fn(),
      logout: jest.fn(),
      isAuthenticated: true,
    });
    useSpider.mockReturnValue({
      spiderData: null,
      startSpider: jest.fn(),
      stopSpider: jest.fn(),
      isRunning: false,
    });

    render(<App />);
    
    await waitFor(() => {
      expect(screen.getByText('Test User')).toBeInTheDocument();
    });
  });

  it('handles login errors', async () => {
    const mockLogin = jest.fn().mockRejectedValue(new Error('Login failed'));
    
    useAuth.mockReturnValue({
      user: null,
      login: mockLogin,
      logout: jest.fn(),
      isAuthenticated: false,
    });
    useSpider.mockReturnValue({
      spiderData: null,
      startSpider: jest.fn(),
      stopSpider: jest.fn(),
      isRunning: false,
    });

    render(<App />);
    
    // Simulate login attempt
    const loginButton = screen.getByText('Login');
    fireEvent.click(loginButton);
    
    await waitFor(() => {
      expect(screen.getByText('Login failed')).toBeInTheDocument();
    });
  });

  it('handles spider start errors', async () => {
    const mockStartSpider = jest.fn().mockRejectedValue(new Error('Spider start failed'));
    
    useAuth.mockReturnValue({
      user: null,
      login: jest.fn(),
      logout: jest.fn(),
      isAuthenticated: false,
    });
    useSpider.mockReturnValue({
      spiderData: null,
      startSpider: mockStartSpider,
      stopSpider: jest.fn(),
      isRunning: false,
    });

    render(<App />);
    
    // Simulate spider start
    const startButton = screen.getByText('Start Spider');
    fireEvent.click(startButton);
    
    await waitFor(() => {
      expect(screen.getByText('Spider start failed')).toBeInTheDocument();
    });
  });

  it('handles spider stop errors', async () => {
    const mockStopSpider = jest.fn().mockRejectedValue(new Error('Spider stop failed'));
    
    useAuth.mockReturnValue({
      user: null,
      login: jest.fn(),
      logout: jest.fn(),
      isAuthenticated: false,
    });
    useSpider.mockReturnValue({
      spiderData: mockSpiderData,
      startSpider: jest.fn(),
      stopSpider: mockStopSpider,
      isRunning: true,
    });

    render(<App />);
    
    // Simulate spider stop
    const stopButton = screen.getByText('Stop Spider');
    fireEvent.click(stopButton);
    
    await waitFor(() => {
      expect(screen.getByText('Spider stop failed')).toBeInTheDocument();
    });
  });

  it('clears errors when requested', async () => {
    useAuth.mockReturnValue({
      user: null,
      login: jest.fn(),
      logout: jest.fn(),
      isAuthenticated: false,
    });
    useSpider.mockReturnValue({
      spiderData: null,
      startSpider: jest.fn(),
      stopSpider: jest.fn(),
      isRunning: false,
    });

    render(<App />);
    
    // Simulate error
    const errorButton = screen.getByText('Simulate Error');
    fireEvent.click(errorButton);
    
    await waitFor(() => {
      expect(screen.getByText('Test error')).toBeInTheDocument();
    });
    
    // Clear error
    const clearButton = screen.getByText('Clear Error');
    fireEvent.click(clearButton);
    
    await waitFor(() => {
      expect(screen.queryByText('Test error')).not.toBeInTheDocument();
    });
  });

  it('renders all routes correctly', async () => {
    useAuth.mockReturnValue({
      user: mockUser,
      login: jest.fn(),
      logout: jest.fn(),
      isAuthenticated: true,
    });
    useSpider.mockReturnValue({
      spiderData: mockSpiderData,
      startSpider: jest.fn(),
      stopSpider: jest.fn(),
      isRunning: false,
    });

    render(<App />);
    
    await waitFor(() => {
      expect(screen.getByText('Welcome to Direct Web Spider')).toBeInTheDocument();
    });
  });

  it('handles component unmounting', async () => {
    const { unmount } = render(<App />);
    
    useAuth.mockReturnValue({
      user: null,
      login: jest.fn(),
      logout: jest.fn(),
      isAuthenticated: false,
    });
    useSpider.mockReturnValue({
      spiderData: null,
      startSpider: jest.fn(),
      stopSpider: jest.fn(),
      isRunning: false,
    });
    
    unmount();
    // Should not throw any errors
  });
});
