"""
Sistema de Testes Completo - Organizador Contábil
Testa todas as funcionalidades do projeto
"""
import os
import json
import shutil
from services.splitter_pdf import split_pdf_by_page, batch_split_pdfs
from services.organizer import create_output_folders, organize_files_parallel
from services.file_scanner import scan_directory
from services.extractor_pdf import extract_pdf_data
import time

base_path = "C:/Users/matheus.recieri/Desktop/testes_pdf - otimizated"
pdf_path = "C:/Users/matheus.recieri/Desktop/testes_pdf - 06/BIOAGRI - 60193.pdf"
    

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


# def test_1_scan_directory(base_path):
#     """TESTE 1: Escanear diretório e listar PDFs"""
#     print_header("TESTE 1: Escanear Diretório")
    
#     # CONFIGURE ESTE CAMINHO
#     #base_path = "C:/Users/matheus.recieri/Desktop/Empresas/EmpresaABC/Contabil/2025"
    
#     print(f"\n  📁 Diretório: {base_path}")
    
#     if not os.path.exists(base_path):
#         print(f"  ❌ ERRO: Diretório não encontrado!")
#         return []
    
#     try:
#         files = scan_directory(base_path)
#         print_results(files)
#         return files
#     except Exception as e:
#         print(f"  ❌ ERRO: {str(e)}")
#         return []


# def test_2_split_all_pdfs(base_path):
#     """TESTE 2: Escanear e separar TODOS os PDFs do diretório página por página"""
#     print_header("TESTE 2: Separar TODOS os PDFs por Páginas")
    
#     # CONFIGURE ESTE CAMINHO
#     # base_path = "C:/Users/matheus.recieri/Desktop/testes_pdf - 05"
    
#     print(f"\n  📁 Diretório: {base_path}")
    
#     if not os.path.exists(base_path):
#         print(f"  ❌ ERRO: Diretório não encontrado!")
#         return []
    
#     try:
#         # Passo 1: Escanear PDFs
#         print("\n  🔍 Escaneando diretório...")
#         pdf_files = scan_directory(base_path)
#         print(f"  ✅ Encontrados: {len(pdf_files)} PDF(s)\n")
        
#         if len(pdf_files) == 0:
#             print("  ⚠️  Nenhum PDF encontrado no diretório!")
#             return []
        
#         # Passo 2: Separar cada PDF
#         all_results = []
#         print("  📄 Separando PDFs página por página...\n")
        
#         for i, pdf_file in enumerate(pdf_files, 1):
#             print(f"  [{i}/{len(pdf_files)}] Processando: {os.path.basename(pdf_file)}")
            
#             try:
#                 result = split_pdf_by_page(pdf_file)
                
#                 if result:
#                     all_results.extend(result)
#                     print(f"       ✅ Separado em {len(result)} página(s)")
#                 else:
#                     print(f"       ⚠️  Nenhuma página separada")
                    
#             except Exception as e:
#                 print(f"       ❌ Erro: {str(e)}")
        
#         # Resumo final
#         print("\n" + "  " + "-" * 60)
#         print(f"  📊 RESUMO:")
#         print(f"     • PDFs processados: {len(pdf_files)}")
#         print(f"     • Total de páginas separadas: {len(all_results)}")
#         print("  " + "-" * 60)
        
#         return all_results
        
#     except Exception as e:
#         print(f"  ❌ ERRO GERAL: {str(e)}")
#         return []


# def test_3_split_by_type(pdf_path):
#     """TESTE 3: Separar PDF por tipo de documento"""
#     print_header("TESTE 3: Separar PDF por Tipo")
    
#     # CONFIGURE ESTE CAMINHO (PDF com múltiplos documentos)
#     # pdf_path = "C:/Users/matheus.recieri/Desktop/Empresas/EmpresaABC/Contabil/2025/OK-259,90 - NF 11958 AMPARO HOTEL 2542C - P 824.pdf"
    
#     # print(f"\n  📄 Arquivo: {pdf_path}")
    
#     # if not os.path.exists(pdf_path):
#     #     print(f"  ❌ ERRO: Arquivo não encontrado!")
#     #     return []
    
#     # try:
#     #     # result = split_pdf_by_type(pdf_path)
#     #     print_results(result)
#     #     return result
#     # except Exception as e:
#     #     print(f"  ❌ ERRO: {str(e)}")
#     #     return []


# def test_4_extract_data(pdf_path):
#     """TESTE 4: Extrair dados de um PDF"""
#     print_header("TESTE 4: Extrair Dados do PDF")
    
#     # CONFIGURE ESTE CAMINHO
#     #  pdf_path = "C:/Users/matheus.recieri/Desktop/Empresas/EmpresaABC/Contabil/2025/OK-259,90 - NF 11958 AMPARO HOTEL 2542C - P 824.pdf"
    
#     print(f"\n  📄 Arquivo: {pdf_path}")
    
#     if not os.path.exists(pdf_path):
#         print(f"  ❌ ERRO: Arquivo não encontrado!")
#         return {}
    
#     try:
#         data = extract_pdf_data(pdf_path)
#         print_results([data])
#         return data
#     except Exception as e:
#         print(f"  ❌ ERRO: {str(e)}")
#         return {}


# def test_5_create_folders(base_path):
#     """TESTE 5: Criar estrutura de pastas"""
#     print_header("TESTE 5: Criar Estrutura de Pastas")
    
#     # CONFIGURE ESTE CAMINHO
#     # base_path = "C:/Users/matheus.recieri/Desktop/Empresas/EmpresaABC/Contabil/2025"
    
#     print(f"\n  📁 Diretório base: {base_path}")
    
#     try:
#         folders = create_output_folders(base_path)
        
#         print("\n  📂 Estrutura de pastas:")
#         for name, path in folders.items():
#             exists = "✅" if os.path.exists(path) else "⚠️ (não existe ainda)"
#             print(f"    • {name}: {path} {exists}")
        
#         return folders
#     except Exception as e:
#         print(f"  ❌ ERRO: {str(e)}")
#         return {}


# def test_6_scan_and_split_pages(base_path):
#     """TESTE 6: Escanear e separar todo o diretório por páginas"""
#     print_header("TESTE 6: Processar Diretório Completo (por páginas)")
    
#     # CONFIGURE ESTE CAMINHO
#     # base_path = "C:/Users/matheus.recieri/Desktop/Empresas/EmpresaABC/Contabil/2025"
    
#     print(f"\n  📁 Diretório: {base_path}")
#     print("  ⚠️  ATENÇÃO: Isso pode demorar e criar muitos arquivos!")
#     print("  💡 Descomente esta função no main() para executar")
    
#     return []
    
#     # Descomente abaixo para executar de verdade:
#     # if not os.path.exists(base_path):
#     #     print(f"  ❌ ERRO: Diretório não encontrado!")
#     #     return []
    
#     # try:
#     #     result = scan_and_split(base_path, split_pages=True)
#     #     print_results(result, max_items=20)
#     #     return result
#     # except Exception as e:
#     #     print(f"  ❌ ERRO: {str(e)}")
#     #     return []


# def test_7_scan_and_split_by_type(base_path):
#     """TESTE 7: Escanear e separar todo o diretório por tipo"""
#     print_header("TESTE 7: Processar Diretório Completo (por tipo)")
    
#     # CONFIGURE ESTE CAMINHO
#     # base_path = "C:/Users/matheus.recieri/Desktop/Empresas/EmpresaABC/Contabil/2025"
    
#     print(f"\n  📁 Diretório: {base_path}")
#     print("  ⚠️  ATENÇÃO: Isso pode demorar!")
#     print("  💡 Descomente esta função no main() para executar")
    
#     return []
    
#     # Descomente abaixo para executar de verdade:
#     # if not os.path.exists(base_path):
#     #     print(f"  ❌ ERRO: Diretório não encontrado!")
#     #     return []
    
#     # try:
#     #     result = scan_and_split_by_type(base_path)
#     #     print_results(result, max_items=20)
#     #     return result
#     # except Exception as e:
#     #     print(f"  ❌ ERRO: {str(e)}")
#     #     return []


def test_optimized_workflow(base_path: str):
    """TESTE OTIMIZADO: Fluxo completo com paralelização"""
    print_header("🚀 FLUXO OTIMIZADO - PROCESSAMENTO PARALELO")
    
    start_time = time.time()
    
    # 1. Scan diretório (única vez)
    pdf_files = scan_directory(base_path)
    print(f"📁 PDFs encontrados: {len(pdf_files)}")
    
    # 2. Split paralelo apenas se necessário
    print("⚡ Separando PDFs multi-páginas...")
    all_files = batch_split_pdfs(pdf_files)
    print(f"📄 Total de documentos: {len(all_files)}")
    
    # 3. Organização paralela
    print("🏗️ Organizando arquivos...")
    stats = organize_files_parallel(base_path, max_workers=16)
    
    total_time = time.time() - start_time
    files_per_second = len(all_files) / total_time
    
    print(f"\n🎉 PROCESSAMENTO CONCLUÍDO!")
    print(f"⏰ Tempo total: {total_time:.2f} segundos ({total_time/60:.2f} minutos)")
    print(f"📊 Velocidade: {files_per_second:.2f} arquivos/segundo")
    print(f"📈 Estatísticas: {stats}")
    
    # Meta de performance
    target_time = 15 * 60  # 15 minutos em segundos
    if total_time <= target_time:
        print(f"✅ META ATINGIDA: {total_time/60:.2f}min <= 15min")
    else:
        print(f"⚠️  FORA DA META: {total_time/60:.2f}min > 15min")


def test_9_organize_files(base_path):
    """TESTE 9: Organizar arquivos em pastas por tipo"""
    print_header("TESTE 9: Organizar Arquivos por Tipo")
    
    # CONFIGURE ESTE CAMINHO
    # base_path = "C:/Users/matheus.recieri/Desktop/Empresas/EmpresaABC/Contabil/2025"
    
    print(f"\n  📁 Diretório: {base_path}")
    print("  ⚠️  ATENÇÃO: Isso vai criar pastas e copiar arquivos!")
    print("  💡 Descomente esta função no main() para executar")
    
    # return {}
    
    # Descomente abaixo para executar de verdade:
    if not os.path.exists(base_path):
        print(f"  ❌ ERRO: Diretório não encontrado!")
        return {}
    
    try:
        # copy_mode=True: COPIA (mantém originais)
        # copy_mode=False: MOVE (remove originais)
        stats = organize_files(base_path, copy_mode=True)
        return stats
    except Exception as e:
        print(f"  ❌ ERRO: {str(e)}")
        return {}


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
    # test_1_scan_directory()
    # test_2_split_all_pdfs()  # MODIFICADO: Agora processa todos os PDFs
    # test_3_split_by_type()
    # test_4_extract_data()
    # test_5_create_folders()
    
    # Teste de fluxo completo
    test_optimized_workflow(base_path)
    
    
    # Teste de organização (descomente para usar)
    # test_9_organize_files(base_path)
    
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