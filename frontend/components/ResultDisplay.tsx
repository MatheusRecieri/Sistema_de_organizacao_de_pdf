'use client';

import { CheckCircle, FileText, Receipt, FolderOpen, AlertTriangle } from 'lucide-react';
import { ProcessingResponse, ResultsDisplayProps } from '@/types';


export default function ResultsDisplay({ results }: ResultsDisplayProps) {

  const files = results.files || [];
  const resultsData = results.results || [];
  const total = results.Total || 0;
  const status = results.status || 'unknown'
  ;
 return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex items-center gap-3 mb-6">
        <CheckCircle className="w-6 h-6 text-green-600" />
        <h2 className="text-xl font-semibold text-gray-800">
          Processamento Concluído
        </h2>
      </div>

      {/* Estatísticas */}
      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
          <div className="flex items-center gap-2 mb-1">
            <FileText className="w-4 h-4 text-blue-600" />
            <span className="text-sm text-gray-600">Total de Arquivos</span>
          </div>
          <p className="text-2xl font-bold text-blue-700">{total}</p>
        </div>

        <div className="p-4 bg-green-50 rounded-lg border border-green-200">
          <div className="flex items-center gap-2 mb-1">
            <CheckCircle className="w-4 h-4 text-green-600" />
            <span className="text-sm text-gray-600">Status</span>
          </div>
          <p className="text-lg font-semibold text-green-700 capitalize">{status}</p>
        </div>
      </div>

      {/* Lista de Arquivos Processados */}
      <div>
        <h3 className="text-sm font-medium text-gray-700 mb-3 flex items-center gap-2">
          <FolderOpen className="w-4 h-4" />
          Arquivos Processados ({files.length}) {/* ← USAR A VARIÁVEL LOCAL */}
        </h3>

        <div className="max-h-96 overflow-y-auto space-y-2 pr-2">
          {files.length > 0 ? (
            files.map((file, index) => {
              // Extrair apenas o nome do arquivo do caminho completo
              const fileName = file.split(/[/\\]/).pop() || file;
              
              return (
                <div
                  key={index}
                  className="p-3 bg-gray-50 rounded-lg border border-gray-200 hover:bg-gray-100
                           transition-colors duration-150"
                >
                  <div className="flex items-start gap-2">
                    <FileText className="w-4 h-4 text-gray-500 mt-0.5 flex-shrink-0" />
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-700 truncate" title={fileName}>
                        {fileName}
                      </p>
                      <p className="text-xs text-gray-500 font-mono truncate mt-1" title={file}>
                        {file}
                      </p>
                    </div>
                  </div>
                </div>
              );
            })
          ) : (
            <div className="p-8 text-center">
              <AlertTriangle className="w-12 h-12 text-yellow-500 mx-auto mb-2" />
              <p className="text-gray-600">Nenhum arquivo foi processado</p>
            </div>
          )}
        </div>
      </div>

      {/* Informações Adicionais */}
      {files.length > 0 && resultsData.length > 0 && (
        <div className="mt-6 pt-6 border-t border-gray-200">
          <h3 className="text-sm font-medium text-gray-700 mb-3">
            Detalhes da Extração
          </h3>
          
          <div className="space-y-3 max-h-64 overflow-y-auto">
            {resultsData.map((result, index) => {
              // Extrair apenas o nome do arquivo
              const fileName = result.arquivo?.split(/[/\\]/).pop() || result.arquivo || 'Arquivo desconhecido';
              
              return (
                <div key={index} className="p-3 bg-gray-50 rounded-lg border border-gray-200">
                  <p className="text-xs text-gray-600 mb-2 truncate" title={fileName}>
                    {fileName}
                  </p>
                  <div className="grid grid-cols-2 gap-2 text-xs">
                    <div>
                      <span className="text-gray-500">Tipo:</span>{' '}
                      <span className="font-medium text-gray-700">{result.tipo || 'N/A'}</span>
                    </div>
                    <div>
                      <span className="text-gray-500">Valor:</span>{' '}
                      <span className="font-medium text-gray-700">
                        {result.valor ? `R$ ${result.valor}` : 'N/A'}
                      </span>
                    </div>
                    <div className="col-span-2">
                      <span className="text-gray-500">Data:</span>{' '}
                      <span className="font-medium text-gray-700">{result.data || 'N/A'}</span>
                    </div>
                  </div>
                  {result.erro && (
                    <p className="text-xs text-red-600 mt-2 flex items-start gap-1">
                      <AlertTriangle className="w-3 h-3 flex-shrink-0 mt-0.5" />
                      <span>{result.erro}</span>
                    </p>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Mensagem se não houver dados */}
      {files.length === 0 && resultsData.length === 0 && (
        <div className="mt-6 p-6 bg-yellow-50 border border-yellow-200 rounded-lg text-center">
          <AlertTriangle className="w-10 h-10 text-yellow-500 mx-auto mb-2" />
          <p className="text-sm text-yellow-800 font-medium">
            O processamento foi concluído, mas nenhum arquivo foi encontrado ou processado.
          </p>
          <p className="text-xs text-yellow-700 mt-1">
            Verifique se o diretório contém arquivos PDF válidos.
          </p>
        </div>
      )}
    </div>
  );
}