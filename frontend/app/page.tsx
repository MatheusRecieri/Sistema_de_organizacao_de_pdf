'use client';

import { useState, useEffect } from 'react';
import { FileText, Folder, Server, AlertCircle } from 'lucide-react';
import DirectoryBrowser from '@/components/DirectoryBrowser';
import ProcessingStatus from '@/components/ProcessingStatus';
import ResultsDisplay from '@/components/ResultDisplay';
import { apiService } from '@/lib/api';
import { ProcessingResponse } from '@/types';

export default function Home() {
  const [selectedPath, setSelectedPath] = useState<string>('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [processingResults, setProcessingResults] = useState<ProcessingResponse | null>(null);
  const [error, setError] = useState<string>('');
  const [serverStatus, setServerStatus] = useState<'checking' | 'online' | 'offline'>('checking');

  // Verificar status do servidor ao carregar
  useEffect(() => {
    checkServerStatus();
  }, []);

  const checkServerStatus = async () => {
    try {
      await apiService.checkHealth();
      setServerStatus('online');
    } catch (error) {
      setServerStatus('offline');
    }
  };

  const handleProcessDirectory = async () => {
    if (!selectedPath) {
      setError('Por favor, selecione um diretório');
      return;
    }

    setIsProcessing(true);
    setError('');
    setProcessingResults(null);

    try {
      const results = await apiService.processDirectory(selectedPath);
      setProcessingResults(results);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao processar diretório');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8 max-w-7xl">
      {/* Header */}
      <header className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-4xl font-bold text-gray-800 mb-2">
              📊 Organizador Contábil
            </h1>
            <p className="text-gray-600">
              Sistema de organização e processamento de documentos contábeis
            </p>
          </div>

          {/* Status do Servidor */}
          <div className="flex items-center gap-2 px-4 py-2 rounded-lg bg-white shadow-sm">
            <Server className={`w-5 h-5 ${
              serverStatus === 'online' ? 'text-green-500' :
              serverStatus === 'offline' ? 'text-red-500' :
              'text-yellow-500'
            }`} />
            <span className={`text-sm font-medium ${
              serverStatus === 'online' ? 'text-green-700' :
              serverStatus === 'offline' ? 'text-red-700' :
              'text-yellow-700'
            }`}>
              {serverStatus === 'online' ? 'Servidor Online' :
               serverStatus === 'offline' ? 'Servidor Offline' :
               'Verificando...'}
            </span>
          </div>
        </div>
      </header>

      {/* Erro de Conexão */}
      {serverStatus === 'offline' && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3">
          <AlertCircle className="w-5 h-5 text-red-500 mt-0.5 flex-shrink-0" />
          <div>
            <h3 className="font-semibold text-red-800">Servidor Backend Offline</h3>
            <p className="text-sm text-red-600 mt-1">
              Não foi possível conectar ao servidor. Certifique-se de que o FastAPI está rodando em{' '}
              <code className="bg-red-100 px-1 rounded">http://localhost:8000</code>
            </p>
            <button
              onClick={checkServerStatus}
              className="mt-2 text-sm text-red-700 underline hover:text-red-800"
            >
              Tentar novamente
            </button>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Painel Esquerdo - Seleção de Diretório */}
        <div className="space-y-6">
          <DirectoryBrowser
            selectedPath={selectedPath}
            onPathSelect={setSelectedPath}
            disabled={isProcessing || serverStatus === 'offline'}
          />

          {/* Botão de Processar */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center gap-2">
              <FileText className="w-5 h-5" />
              Processar Documentos
            </h2>

            {selectedPath && (
              <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                <p className="text-sm text-gray-600 mb-1">Diretório selecionado:</p>
                <p className="text-sm font-mono text-blue-700 break-all">{selectedPath}</p>
              </div>
            )}

            <button
              onClick={handleProcessDirectory}
              disabled={!selectedPath || isProcessing || serverStatus === 'offline'}
              className="w-full py-3 px-4 bg-blue-600 text-white rounded-lg font-medium
                       hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed
                       transition-colors duration-200 flex items-center justify-center gap-2"
            >
              {isProcessing ? (
                <>
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  Processando...
                </>
              ) : (
                <>
                  <FileText className="w-5 h-5" />
                  Processar Diretório
                </>
              )}
            </button>

            {error && (
              <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
                <p className="text-sm text-red-700">{error}</p>
              </div>
            )}
          </div>
        </div>

        {/* Painel Direito - Status e Resultados */}
        <div className="space-y-6">
          {isProcessing && <ProcessingStatus />}
          
          {processingResults && !isProcessing && (
            <ResultsDisplay results={processingResults} />
          )}

          {!isProcessing && !processingResults && (
            <div className="bg-white rounded-lg shadow-md p-12 text-center">
              <Folder className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <p className="text-gray-500">
                Selecione um diretório e clique em processar para ver os resultados
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}