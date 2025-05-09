import axios from 'axios';
import { ModelAnalysis } from '../types';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const analysisService = {
  async createAnalysis(analysisData: Omit<ModelAnalysis, 'id' | 'created_at' | 'results'>): Promise<ModelAnalysis> {
    const response = await axios.post(`${API_URL}/analyses`, analysisData);
    return response.data;
  },

  async getAnalyses(skip: number = 0, limit: number = 100): Promise<ModelAnalysis[]> {
    const response = await axios.get(`${API_URL}/analyses`, {
      params: { skip, limit },
    });
    return response.data;
  },

  async getAnalysis(id: number): Promise<ModelAnalysis> {
    const response = await axios.get(`${API_URL}/analyses/${id}`);
    return response.data;
  },

  async getAnalysisResults(id: number): Promise<any> {
    const analysis = await this.getAnalysis(id);
    return analysis.results ? JSON.parse(analysis.results) : null;
  },
}; 