import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export interface Model {
  id: number;
  name: string;
  description: string;
  file_path: string;
  thumbnail_path: string;
  owner_id: number;
  created_at: string;
  updated_at: string;
}

export const modelService = {
  async getModels(): Promise<Model[]> {
    const response = await axios.get(`${API_URL}/models`);
    return response.data;
  },

  async getModel(id: number): Promise<Model> {
    const response = await axios.get(`${API_URL}/models/${id}`);
    return response.data;
  },

  async createModel(data: FormData): Promise<Model> {
    const response = await axios.post(`${API_URL}/models`, data, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  async updateModel(id: number, data: Partial<Model>): Promise<Model> {
    const response = await axios.put(`${API_URL}/models/${id}`, data);
    return response.data;
  },

  async deleteModel(id: number): Promise<void> {
    await axios.delete(`${API_URL}/models/${id}`);
  },

  async getModelFileUrl(filePath: string): Promise<string> {
    return `${API_URL}${filePath}`;
  },

  async getModelFileContent(filePath: string): Promise<string | null> {
    const response = await axios.get(`${API_URL}${filePath}`, {
      responseType: 'arraybuffer',
    });
    const content = response.data;
    return content ? Buffer.from(content).toString('base64') : null;
  },

  async getThumbnailUrl(thumbnailPath: string | null): Promise<string | null> {
    if (!thumbnailPath) return null;
    return `${API_URL}${thumbnailPath}`;
  },
}; 