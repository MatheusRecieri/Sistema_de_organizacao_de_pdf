"""
Sistema de Testes Completo - Organizador Contábil
Testa todas as funcionalidades do projeto
"""
import os
import json
from services.splitter_pdf import split_pdf_by_page, split_pdf_by_type
from services.file_scanner import (
    scan_directory, 
    scan_and_split, 
    scan_and_split_by_type,
    create_output_folders
)
from services.extractor_pdf import extract_pdf_data


def print_header(title):
    """Imprime um cabeçalho bonito para os testes"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_results(items, max_items=10):
    """Imprime resultados de forma organizada"""
    if not items:
        print("  ❌ Nenhum resultado encontrado")
        return
    
    print(f"  ✅ Total: {len(items)} item(s)")
    print(f"\n  Mostrando {min(len(items), max_items)} primeiros:")
    
    for i, item in enumerate(items[:max_items], 1):
        if isinstance(item, dict):
            print(f"\n  {i}. Arquivo: {item.get('arquivo', 'N/A')}")
            print(f"     Tipo: {item.get('tipo', 'N/A')}")
            print(f"     Valor: {item.get('valor', 'N/A')}")
            print(f"     Data: {item.get('data', 'N/A')}")
            if 'erro' in item:
                print(f"     ⚠️ Erro: {item['erro']}")
        else:
            print(f"  {i}. {item}")
    
    if len(items) > max_items:
        print(f"\n  ... e mais {len(items) - max_items} item(s)")


def test_1_scan_directory():
    """TESTE 1: Escanear diretório e listar PDFs"""
    print_header("TESTE 1: Escanear Diretório")
    
    # CONFIGURE ESTE CAMINHO
    base_path = "C:/Users/matheus.recieri/Desktop/testes_pdf - 05"
    
    print(f"\n  📁 Diretório: {base_path}")
    
    if not os.path.exists(base_path):
        print(f"  ❌ ERRO: Diretório não encontrado!")
        return []
    
    try:
        files = scan_directory(base_path)
        print_results(files)
        return files
    except Exception as e:
        print(f"  ❌ ERRO: {str(e)}")
        return []


def test_2_split_single_pdf():
    """TESTE 2: Separar um PDF específico página por página"""
    print_header("TESTE 2: Separar PDF por Páginas")
    
    # CONFIGURE ESTE CAMINHO
    pdf_path = "C:/Users/matheus.recieri/Desktop/testes_pdf - 05/BIOAGRI - 60193.pdf"
    
    print(f"\n  📄 Arquivo: {pdf_path}")
    
    if not os.path.exists(pdf_path):
        print(f"  ❌ ERRO: Arquivo não encontrado!")
        return []
    
    try:
        result = split_pdf_by_page(pdf_path)
        print_results(result)
        return result
    except Exception as e:
        print(f"  ❌ ERRO: {str(e)}")
        return []


def test_3_split_by_type():
    """TESTE 3: Separar PDF por tipo de documento"""
    print_header("TESTE 3: Separar PDF por Tipo")
    
    # CONFIGURE ESTE CAMINHO (PDF com múltiplos documentos)
    pdf_path = "C:/Users/matheus.recieri/Desktop/testes_pdf - 05/BIOAGRI - 60193.pdf"
    
    print(f"\n  📄 Arquivo: {pdf_path}")
    
    if not os.path.exists(pdf_path):
        print(f"  ❌ ERRO: Arquivo não encontrado!")
        return []
    
    try:
        result = split_pdf_by_type(pdf_path)
        print_results(result)
        return result
    except Exception as e:
        print(f"  ❌ ERRO: {str(e)}")
        return []


def test_4_extract_data():
    """TESTE 4: Extrair dados de um PDF"""
    print_header("TESTE 4: Extrair Dados do PDF")
    
    # CONFIGURE ESTE CAMINHO
    pdf_path = "C:/Users/matheus.recieri/Desktop/testes_pdf - 05/Elias de Alencar - Guia GFD.pdf"
    
    print(f"\n  📄 Arquivo: {pdf_path}")
    
    if not os.path.exists(pdf_path):
        print(f"  ❌ ERRO: Arquivo não encontrado!")
        return {}
    
    try:
        data = extract_pdf_data(pdf_path)
        print_results([data])
        return data
    except Exception as e:
        print(f"  ❌ ERRO: {str(e)}")
        return {}


def test_5_create_folders():
    """TESTE 5: Criar estrutura de pastas"""
    print_header("TESTE 5: Criar Estrutura de Pastas")
    
    # CONFIGURE ESTE CAMINHO
    base_path = "C:/Users/matheus.recieri/Desktop/testes_pdf - 05"
    
    print(f"\n  📁 Diretório base: {base_path}")
    
    try:
        folders = create_output_folders(base_path)
        
        print("\n  📂 Estrutura de pastas:")
        for name, path in folders.items():
            exists = "✅" if os.path.exists(path) else "⚠️ (não existe ainda)"
            print(f"    • {name}: {path} {exists}")
        
        return folders
    except Exception as e:
        print(f"  ❌ ERRO: {str(e)}")
        return {}


def test_6_scan_and_split_pages():
    """TESTE 6: Escanear e separar todo o diretório por páginas"""
    print_header("TESTE 6: Processar Diretório Completo (por páginas)")
    
    # CONFIGURE ESTE CAMINHO
    base_path = "C:/Users/matheus.recieri/Desktop/testes_pdf - 05/Elias de Alencar - Guia GFD.pdf"
    
    print(f"\n  📁 Diretório: {base_path}")
    print("  ⚠️  ATENÇÃO: Isso pode demorar e criar muitos arquivos!")
    print("  💡 Descomente esta função no main() para executar")
    
    return []
    
    # Descomente abaixo para executar de verdade:
    # if not os.path.exists(base_path):
    #     print(f"  ❌ ERRO: Diretório não encontrado!")
    #     return []
    
    # try:
    #     result = scan_and_split(base_path, split_pages=True)
    #     print_results(result, max_items=20)
    #     return result
    # except Exception as e:
    #     print(f"  ❌ ERRO: {str(e)}")
    #     return []


def test_7_scan_and_split_by_type():
    """TESTE 7: Escanear e separar todo o diretório por tipo"""
    print_header("TESTE 7: Processar Diretório Completo (por tipo)")
    
    # CONFIGURE ESTE CAMINHO
    base_path = "C:/Users/matheus.recieri/Desktop/testes_pdf - 05"
    
    print(f"\n  📁 Diretório: {base_path}")
    print("  ⚠️  ATENÇÃO: Isso pode demorar!")
    print("  💡 Descomente esta função no main() para executar")
    
    return []
    
    # Descomente abaixo para executar de verdade:
    # if not os.path.exists(base_path):
    #     print(f"  ❌ ERRO: Diretório não encontrado!")
    #     return []
    
    # try:
    #     result = scan_and_split_by_type(base_path)
    #     print_results(result, max_items=20)
    #     return result
    # except Exception as e:
    #     print(f"  ❌ ERRO: {str(e)}")
    #     return []


def test_8_full_workflow():
    """TESTE 8: Fluxo completo - Escanear, Separar e Extrair"""
    print_header("TESTE 8: Fluxo Completo do Sistema")
    
    # CONFIGURE ESTE CAMINHO
    base_path = "C:/Users/matheus.recieri/Desktop/testes_pdf - 05"
    
    print(f"\n  📁 Diretório: {base_path}")
    
    if not os.path.exists(base_path):
        print(f"  ❌ ERRO: Diretório não encontrado!")
        return
    
    try:
        # Passo 1: Escanear
        print("\n  🔍 Passo 1: Escaneando diretório...")
        files = scan_directory(base_path)
        print(f"     Encontrados: {len(files)} PDF(s)")
        
        # Passo 2: Processar apenas os primeiros 3 PDFs (para não demorar muito)
        print("\n  📄 Passo 2: Processando primeiros 3 PDFs...")
        
        results = []
        for i, pdf_file in enumerate(files[:3], 1):
            print(f"\n     Processando {i}/3: {os.path.basename(pdf_file)}")
            
            # Extrair dados
            data = extract_pdf_data(pdf_file)
            results.append(data)
            
            print(f"       Tipo: {data.get('tipo', 'N/A')}")
            print(f"       Valor: {data.get('valor', 'N/A')}")
            print(f"       Data: {data.get('data', 'N/A')}")
        
        # Passo 3: Resumo
        print("\n  📊 Passo 3: Resumo Final")
        notas = sum(1 for r in results if 'Nota Fiscal' in r.get('tipo', ''))
        recibos = sum(1 for r in results if 'Recibo' in r.get('tipo', ''))
        desconhecidos = sum(1 for r in results if 'Desconhecido' in r.get('tipo', ''))
        
        print(f"     📋 Notas Fiscais: {notas}")
        print(f"     📋 Recibos: {recibos}")
        print(f"     ❓ Desconhecidos: {desconhecidos}")
        
    except Exception as e:
        print(f"  ❌ ERRO: {str(e)}")


def main():
    """Executa todos os testes"""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "SISTEMA DE TESTES - ORGANIZADOR CONTÁBIL" + " " * 18 + "║")
    print("╚" + "=" * 78 + "╝")
    
    # ============================================
    # CONFIGURE AQUI QUAIS TESTES EXECUTAR
    # ============================================
    
    # Testes básicos (rápidos)
    test_1_scan_directory()
    test_2_split_single_pdf()
    test_3_split_by_type()
    test_4_extract_data()
    test_5_create_folders()
    
    # Teste de fluxo completo
    test_8_full_workflow()
    
    # Testes pesados (descomente para executar)
    # test_6_scan_and_split_pages()
    # test_7_scan_and_split_by_type()
    
    print("\n")
    print("=" * 80)
    print("  ✅ TESTES CONCLUÍDOS!")
    print("=" * 80)
    print()


if __name__ == "__main__":
    main()