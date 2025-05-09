import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

interface LoginResponse {
  token: string;
  user: {
    id: number;
    email: string;
    full_name: string;
  };
}

interface User {
  id: number;
  email: string;
  full_name: string;
  is_active: boolean;
  is_superuser: boolean;
  created_at: string;
  updated_at: string;
}

interface AuthError {
  message: string;
  field?: string;
}

class AuthService {
  private token: string | null = null;

  async login(email: string, password: string): Promise<LoginResponse> {
    try {
      const response = await axios.post(`${API_URL}/api/auth/login`, {
        email,
        password,
      });
      
      if (response.data.token) {
        this.setToken(response.data.token);
      }
      
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        if (error.response) {
          const errorData = error.response.data;
          throw {
            message: errorData.message || 'Erreur lors de la connexion',
            field: errorData.field
          } as AuthError;
        }
      }
      throw {
        message: 'Une erreur est survenue lors de la connexion'
      } as AuthError;
    }
  }

  async register(userData: Omit<User, 'id' | 'is_active' | 'is_superuser' | 'created_at' | 'updated_at'>): Promise<User> {
    try {
      const response = await axios.post(`${API_URL}/api/auth/register`, userData);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        if (error.response) {
          const errorData = error.response.data;
          throw {
            message: errorData.message || 'Erreur lors de l\'inscription',
            field: errorData.field
          } as AuthError;
        }
      }
      throw {
        message: 'Une erreur est survenue lors de l\'inscription'
      } as AuthError;
    }
  }

  setToken(token: string) {
    this.token = token;
    localStorage.setItem('token', token);
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  }

  getToken(): string | null {
    if (!this.token) {
      this.token = localStorage.getItem('token');
    }
    return this.token;
  }

  isAuthenticated(): boolean {
    return !!this.getToken();
  }

  logout() {
    this.token = null;
    localStorage.removeItem('token');
    delete axios.defaults.headers.common['Authorization'];
  }
}

export const authService = new AuthService(); 