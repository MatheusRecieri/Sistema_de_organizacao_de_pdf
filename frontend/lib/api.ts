import { ProcessingResponse } from '@/types';
import axios from 'axios';
import { error } from 'console';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  }
})

export const apiService = {
  checkHealth: async () => {
    try {
      const response = await api.get('/')
      return response.data
    } catch (error) {
      throw new Error('Servidor backend não está respondendo')
    }
  },

  processDirectory: async (path: string): Promise<ProcessingResponse> => {
    try {
      const response = await api.post('/processar', { caminho: path});
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(error.response?.data?.erro || 'Erro ao processar diretório')
      }
      throw error;
    }
  },

  listDirectory: async (path: string) => {
    try {
      const response = await api.post('/listar-diretorios', { caminho: path});
      return response.data;
    } catch (error) {
      if(axios.isAxiosError(error)) {
        throw new Error(error.response?.data?.erro || 'Erro ao listar diretorio');
      }
      throw error;
    }
  }
}

export default api;