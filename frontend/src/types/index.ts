export interface User {
  id: number;
  email: string;
  full_name: string;
  is_active: boolean;
  is_superuser: boolean;
  created_at: string;
  updated_at: string;
}

export interface Model3D {
  id: number;
  name: string;
  description: string | null;
  is_public: boolean;
  metadata: string | null;
  owner_id: number;
  file_path: string;
  thumbnail_path: string | null;
  created_at: string;
  updated_at: string;
}

export interface ModelAnalysis {
  id: number;
  model_id: number;
  analysis_type: string;
  parameters: string;
  status: string;
  results: string | null;
  created_at: string;
}

export interface ChatSession {
  id: number;
  user_id: number;
  model_id: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface ChatMessage {
  id: number;
  session_id: number;
  content: string;
  is_user: boolean;
  created_at: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
} 