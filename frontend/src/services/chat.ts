import { ChatSession, ChatMessage } from '../types';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
const WS_URL = process.env.REACT_APP_WS_URL || 'ws://localhost:8000';

export const chatService = {
  async createSession(modelId: number): Promise<ChatSession> {
    const response = await fetch(`${API_URL}/chat/sessions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ model_id: modelId }),
    });
    return response.json();
  },

  async getSessions(skip: number = 0, limit: number = 100): Promise<ChatSession[]> {
    const response = await fetch(`${API_URL}/chat/sessions?skip=${skip}&limit=${limit}`);
    return response.json();
  },

  async getMessages(sessionId: number, skip: number = 0, limit: number = 100): Promise<ChatMessage[]> {
    const response = await fetch(
      `${API_URL}/chat/sessions/${sessionId}/messages?skip=${skip}&limit=${limit}`
    );
    return response.json();
  },

  connectToSession(sessionId: number, onMessage: (message: ChatMessage) => void): WebSocket {
    const ws = new WebSocket(`${WS_URL}/chat/ws/${sessionId}`);

    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      onMessage(message);
    };

    return ws;
  },

  sendMessage(ws: WebSocket, content: string): void {
    ws.send(JSON.stringify({ content, is_user: true }));
  },
}; 