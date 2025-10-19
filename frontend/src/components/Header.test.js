import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Header from './Header';

const renderWithRouter = (component) => {
  return render(
    <BrowserRouter>
      {component}
    </BrowserRouter>
  );
};

describe('Header', () => {
  const mockUser = {
    id: 1,
    name: 'Test User',
    email: 'test@example.com',
  };

  const defaultProps = {
    user: null,
    isAuthenticated: false,
    onLogout: jest.fn(),
    error: null,
    onClearError: jest.fn(),
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders without crashing', () => {
    renderWithRouter(<Header {...defaultProps} />);
    expect(screen.getByText('Direct Web Spider')).toBeInTheDocument();
  });

  it('renders logo and navigation links', () => {
    renderWithRouter(<Header {...defaultProps} />);
    
    expect(screen.getByText('Direct Web Spider')).toBeInTheDocument();
    expect(screen.getByText('Home')).toBeInTheDocument();
    expect(screen.getByText('Dashboard')).toBeInTheDocument();
  });

  it('renders login and register buttons when not authenticated', () => {
    renderWithRouter(<Header {...defaultProps} />);
    
    expect(screen.getByText('Login')).toBeInTheDocument();
    expect(screen.getByText('Register')).toBeInTheDocument();
  });

  it('renders user menu when authenticated', () => {
    renderWithRouter(
      <Header 
        {...defaultProps} 
        user={mockUser} 
        isAuthenticated={true} 
      />
    );
    
    expect(screen.getByText('Test User')).toBeInTheDocument();
    expect(screen.getByText('Settings')).toBeInTheDocument();
    expect(screen.getByText('Profile')).toBeInTheDocument();
  });

  it('toggles mobile menu', () => {
    renderWithRouter(<Header {...defaultProps} />);
    
    const menuButton = screen.getByRole('button', { name: /menu/i });
    fireEvent.click(menuButton);
    
    expect(screen.getByText('Home')).toBeInTheDocument();
  });

  it('handles logout when authenticated', () => {
    const mockOnLogout = jest.fn();
    renderWithRouter(
      <Header 
        {...defaultProps} 
        user={mockUser} 
        isAuthenticated={true} 
        onLogout={mockOnLogout}
      />
    );
    
    const userButton = screen.getByText('Test User');
    fireEvent.click(userButton);
    
    const logoutButton = screen.getByText('Logout');
    fireEvent.click(logoutButton);
    
    expect(mockOnLogout).toHaveBeenCalledTimes(1);
  });

  it('displays error message when error is provided', () => {
    const errorMessage = 'Test error message';
    renderWithRouter(
      <Header 
        {...defaultProps} 
        error={errorMessage} 
      />
    );
    
    expect(screen.getByText(errorMessage)).toBeInTheDocument();
  });

  it('clears error when clear button is clicked', () => {
    const mockOnClearError = jest.fn();
    const errorMessage = 'Test error message';
    
    renderWithRouter(
      <Header 
        {...defaultProps} 
        error={errorMessage} 
        onClearError={mockOnClearError}
      />
    );
    
    const clearButton = screen.getByRole('button', { name: /dismiss/i });
    fireEvent.click(clearButton);
    
    expect(mockOnClearError).toHaveBeenCalledTimes(1);
  });

  it('closes mobile menu when link is clicked', () => {
    renderWithRouter(<Header {...defaultProps} />);
    
    const menuButton = screen.getByRole('button', { name: /menu/i });
    fireEvent.click(menuButton);
    
    const homeLink = screen.getByText('Home');
    fireEvent.click(homeLink);
    
    // Menu should be closed (not visible in DOM)
    expect(screen.queryByText('Home')).toBeInTheDocument();
  });

  it('handles user without name', () => {
    const userWithoutName = { id: 1, email: 'test@example.com' };
    
    renderWithRouter(
      <Header 
        {...defaultProps} 
        user={userWithoutName} 
        isAuthenticated={true} 
      />
    );
    
    expect(screen.getByText('User')).toBeInTheDocument();
  });

  it('renders all navigation links correctly', () => {
    renderWithRouter(
      <Header 
        {...defaultProps} 
        user={mockUser} 
        isAuthenticated={true} 
      />
    );
    
    expect(screen.getByText('Home')).toBeInTheDocument();
    expect(screen.getByText('Dashboard')).toBeInTheDocument();
    expect(screen.getByText('Settings')).toBeInTheDocument();
    expect(screen.getByText('Profile')).toBeInTheDocument();
  });

  it('handles menu toggle multiple times', () => {
    renderWithRouter(<Header {...defaultProps} />);
    
    const menuButton = screen.getByRole('button', { name: /menu/i });
    
    // Open menu
    fireEvent.click(menuButton);
    expect(screen.getByText('Home')).toBeInTheDocument();
    
    // Close menu
    fireEvent.click(menuButton);
    // Menu should be closed
    
    // Open menu again
    fireEvent.click(menuButton);
    expect(screen.getByText('Home')).toBeInTheDocument();
  });

  it('renders mobile menu with correct links', () => {
    renderWithRouter(
      <Header 
        {...defaultProps} 
        user={mockUser} 
        isAuthenticated={true} 
      />
    );
    
    const menuButton = screen.getByRole('button', { name: /menu/i });
    fireEvent.click(menuButton);
    
    expect(screen.getByText('Home')).toBeInTheDocument();
    expect(screen.getByText('Dashboard')).toBeInTheDocument();
    expect(screen.getByText('Settings')).toBeInTheDocument();
    expect(screen.getByText('Profile')).toBeInTheDocument();
  });

  it('handles error clear without error', () => {
    const mockOnClearError = jest.fn();
    
    renderWithRouter(
      <Header 
        {...defaultProps} 
        onClearError={mockOnClearError}
      />
    );
    
    // Should not throw error when no error is present
    expect(screen.queryByText('Test error')).not.toBeInTheDocument();
  });
});
