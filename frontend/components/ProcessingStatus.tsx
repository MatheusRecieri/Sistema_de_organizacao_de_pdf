'use client';

import { FileText, Loader2 } from 'lucide-react';

export default function ProcessingStatus() {
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex items-center gap-3 mb-4">
        <Loader2 className="w-6 h-6 text-blue-600 animate-spin" />
        <h2 className="text-xl font-semibold text-gray-800">
          Processando Documentos
        </h2>
      </div>

      <div className="space-y-4">
        <div className="flex items-center gap-3 p-3 bg-blue-50 rounded-lg animate-pulse">
          <div className="w-2 h-2 bg-blue-600 rounded-full animate-ping" />
          <p className="text-sm text-gray-700">Escaneando diretório...</p>
        </div>

        <div className="flex items-center gap-3 p-3 bg-blue-50 rounded-lg animate-pulse delay-100">
          <div className="w-2 h-2 bg-blue-600 rounded-full animate-ping" />
          <p className="text-sm text-gray-700">Separando páginas dos PDFs...</p>
        </div>

        <div className="flex items-center gap-3 p-3 bg-blue-50 rounded-lg animate-pulse delay-200">
          <div className="w-2 h-2 bg-blue-600 rounded-full animate-ping" />
          <p className="text-sm text-gray-700">Extraindo informações...</p>
        </div>

        <div className="mt-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
          <p className="text-sm text-yellow-800">
            ⏱️ Este processo pode levar alguns minutos dependendo da quantidade de arquivos
          </p>
        </div>
      </div>
    </div>
  );
}