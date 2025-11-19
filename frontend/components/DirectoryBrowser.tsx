'use client';

import { useState } from 'react';
import { Folder, ChevronRight, HardDrive } from 'lucide-react';

interface DirectoryBrowserProps {
  selectedPath: string;
  onPathSelect: (path: string) => void;
  disabled?: boolean;
}

export default function DirectoryBrowser({ 
  selectedPath, 
  onPathSelect, 
  disabled = false 
}: DirectoryBrowserProps) {
  const [customPath, setCustomPath] = useState('');

  // Exemplos de diretórios comuns (você pode remover ou adaptar)
  const commonDirectories = [
    'C:/Users/matheus.recieri/Desktop/testes_pdf',
    'C:/Users/matheus.recieri/Desktop/Empresas',
    'C:/Documentos/Contabil',
  ];

  const handleSelectCommon = (path: string) => {
    if (!disabled) {
      onPathSelect(path);
      setCustomPath(path);
    }
  };

  const handleCustomPathSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (customPath.trim() && !disabled) {
      onPathSelect(customPath.trim());
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center gap-2">
        <Folder className="w-5 h-5" />
        Selecionar Diretório
      </h2>

      {/* Input de Caminho Personalizado */}
      <form onSubmit={handleCustomPathSubmit} className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Caminho do Diretório
        </label>
        <div className="flex gap-2">
          <input
            type="text"
            value={customPath}
            onChange={(e) => setCustomPath(e.target.value)}
            placeholder="Ex: C:/Users/seu-usuario/Desktop/pdfs"
            disabled={disabled}
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 
                     focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100
                     disabled:cursor-not-allowed"
          />
          <button
            type="submit"
            disabled={disabled || !customPath.trim()}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg font-medium
                     hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed
                     transition-colors duration-200"
          >
            Selecionar
          </button>
        </div>
        <p className="text-xs text-gray-500 mt-2">
          Digite o caminho completo do diretório que deseja processar
        </p>
      </form>

      {/* Diretórios Comuns */}
      <div>
        <h3 className="text-sm font-medium text-gray-700 mb-3 flex items-center gap-2">
          <HardDrive className="w-4 h-4" />
          Diretórios Recentes
        </h3>
        <div className="space-y-2">
          {commonDirectories.map((dir, index) => (
            <button
              key={index}
              onClick={() => handleSelectCommon(dir)}
              disabled={disabled}
              className={`w-full text-left px-4 py-3 rounded-lg border transition-all duration-200
                       ${selectedPath === dir
                         ? 'bg-blue-50 border-blue-300 text-blue-700'
                         : 'bg-gray-50 border-gray-200 text-gray-700 hover:bg-gray-100'
                       }
                       disabled:opacity-50 disabled:cursor-not-allowed
                       flex items-center gap-2 group`}
            >
              <Folder className={`w-4 h-4 flex-shrink-0 ${
                selectedPath === dir ? 'text-blue-500' : 'text-gray-400'
              }`} />
              <span className="flex-1 text-sm font-mono truncate">{dir}</span>
              <ChevronRight className={`w-4 h-4 flex-shrink-0 transition-transform
                ${selectedPath === dir ? 'text-blue-500 transform translate-x-1' : 'text-gray-400'}
                group-hover:translate-x-1`} />
            </button>
          ))}
        </div>
      </div>

      {/* Caminho Selecionado */}
      {selectedPath && (
        <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg">
          <p className="text-sm font-medium text-green-800 mb-1">✓ Diretório Selecionado</p>
          <p className="text-xs font-mono text-green-700 break-all">{selectedPath}</p>
        </div>
      )}
    </div>
  );
}