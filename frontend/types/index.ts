export interface ProcessResult {
  arquivo: string
  tipo: string
  valor: string | null
  data: string | null
  erro?: string;
}

export interface ProcessingResponse {
  status: string
  Total: number
  files: string[]
  results?: ProcessResult[]
}

export interface DirectoryItem {
  name: string
  path: string
  isDirectory: boolean
  size?: number
  modifiedDate?: string
}

export interface ProcessingStats {
  notas_fiscais: number
  recibos: number
  outros: number
  erros: number
  total_valor_notas?: number,
  total_valor_recebidos?: number
}