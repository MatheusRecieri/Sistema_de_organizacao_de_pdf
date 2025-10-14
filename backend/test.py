"""
Sistema de Testes Completo - Organizador Contábil
Testa todas as funcionalidades do projeto
"""
import os
import json
import shutil
from services.splitter_pdf import split_pdf_by_page, split_pdf_by_type
from services.organizer import create_output_folders, organize_files
from services.file_scanner import (
    scan_directory, 
    scan_and_split, 
    scan_and_split_by_type
)
from services.extractor_pdf import extract_pdf_data

base_path = "C:/Users/matheus.recieri/Desktop/testes_pdf - 06"
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


def test_1_scan_directory(base_path):
    """TESTE 1: Escanear diretório e listar PDFs"""
    print_header("TESTE 1: Escanear Diretório")
    
    # CONFIGURE ESTE CAMINHO
    #base_path = "C:/Users/matheus.recieri/Desktop/Empresas/EmpresaABC/Contabil/2025"
    
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


def test_2_split_all_pdfs(base_path):
    """TESTE 2: Escanear e separar TODOS os PDFs do diretório página por página"""
    print_header("TESTE 2: Separar TODOS os PDFs por Páginas")
    
    # CONFIGURE ESTE CAMINHO
    # base_path = "C:/Users/matheus.recieri/Desktop/testes_pdf - 05"
    
    print(f"\n  📁 Diretório: {base_path}")
    
    if not os.path.exists(base_path):
        print(f"  ❌ ERRO: Diretório não encontrado!")
        return []
    
    try:
        # Passo 1: Escanear PDFs
        print("\n  🔍 Escaneando diretório...")
        pdf_files = scan_directory(base_path)
        print(f"  ✅ Encontrados: {len(pdf_files)} PDF(s)\n")
        
        if len(pdf_files) == 0:
            print("  ⚠️  Nenhum PDF encontrado no diretório!")
            return []
        
        # Passo 2: Separar cada PDF
        all_results = []
        print("  📄 Separando PDFs página por página...\n")
        
        for i, pdf_file in enumerate(pdf_files, 1):
            print(f"  [{i}/{len(pdf_files)}] Processando: {os.path.basename(pdf_file)}")
            
            try:
                result = split_pdf_by_page(pdf_file)
                
                if result:
                    all_results.extend(result)
                    print(f"       ✅ Separado em {len(result)} página(s)")
                else:
                    print(f"       ⚠️  Nenhuma página separada")
                    
            except Exception as e:
                print(f"       ❌ Erro: {str(e)}")
        
        # Resumo final
        print("\n" + "  " + "-" * 60)
        print(f"  📊 RESUMO:")
        print(f"     • PDFs processados: {len(pdf_files)}")
        print(f"     • Total de páginas separadas: {len(all_results)}")
        print("  " + "-" * 60)
        
        return all_results
        
    except Exception as e:
        print(f"  ❌ ERRO GERAL: {str(e)}")
        return []


def test_3_split_by_type(pdf_path):
    """TESTE 3: Separar PDF por tipo de documento"""
    print_header("TESTE 3: Separar PDF por Tipo")
    
    # CONFIGURE ESTE CAMINHO (PDF com múltiplos documentos)
    # pdf_path = "C:/Users/matheus.recieri/Desktop/Empresas/EmpresaABC/Contabil/2025/OK-259,90 - NF 11958 AMPARO HOTEL 2542C - P 824.pdf"
    
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


def test_4_extract_data(pdf_path):
    """TESTE 4: Extrair dados de um PDF"""
    print_header("TESTE 4: Extrair Dados do PDF")
    
    # CONFIGURE ESTE CAMINHO
    #  pdf_path = "C:/Users/matheus.recieri/Desktop/Empresas/EmpresaABC/Contabil/2025/OK-259,90 - NF 11958 AMPARO HOTEL 2542C - P 824.pdf"
    
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


def test_5_create_folders(base_path):
    """TESTE 5: Criar estrutura de pastas"""
    print_header("TESTE 5: Criar Estrutura de Pastas")
    
    # CONFIGURE ESTE CAMINHO
    # base_path = "C:/Users/matheus.recieri/Desktop/Empresas/EmpresaABC/Contabil/2025"
    
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


def test_6_scan_and_split_pages(base_path):
    """TESTE 6: Escanear e separar todo o diretório por páginas"""
    print_header("TESTE 6: Processar Diretório Completo (por páginas)")
    
    # CONFIGURE ESTE CAMINHO
    # base_path = "C:/Users/matheus.recieri/Desktop/Empresas/EmpresaABC/Contabil/2025"
    
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


def test_7_scan_and_split_by_type(base_path):
    """TESTE 7: Escanear e separar todo o diretório por tipo"""
    print_header("TESTE 7: Processar Diretório Completo (por tipo)")
    
    # CONFIGURE ESTE CAMINHO
    # base_path = "C:/Users/matheus.recieri/Desktop/Empresas/EmpresaABC/Contabil/2025"
    
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


def test_8_full_workflow(base_path):
    """TESTE 8: Fluxo Completo do Sistema - Simulação de Uso Real"""
    print_header("TESTE 8: Fluxo Completo do Sistema (Produção)")
    
    # CONFIGURE ESTE CAMINHO
    # base_path = "C:/Users/matheus.recieri/Desktop/testes_pdf - 05"
    
    print(f"\n  📁 Diretório de trabalho: {base_path}")
    print("\n  ⚙️  Este teste simula o uso completo do sistema:")
    print("     1. Escanear diretório")
    print("     2. Separar PDFs com múltiplas páginas")
    print("     3. Identificar tipo de cada documento")
    print("     4. Extrair dados (valor, data)")
    print("     5. Organizar em pastas por tipo")
    print("     6. Gerar relatório final")
    
    if not os.path.exists(base_path):
        print(f"\n  ❌ ERRO: Diretório não encontrado!")
        return
    
    try:
        # ==========================================
        # PASSO 1: ESCANEAR DIRETÓRIO
        # ==========================================
        print("\n" + "  " + "=" * 60)
        print("  📍 PASSO 1: ESCANEANDO DIRETÓRIO")
        print("  " + "=" * 60)
        
        original_files = scan_directory(base_path)
        print(f"\n  ✅ Encontrados: {len(original_files)} arquivo(s) PDF")
        
        if len(original_files) == 0:
            print("\n  ⚠️  Nenhum PDF encontrado! Abortando teste.")
            return
        
        print("\n  📄 Arquivos encontrados:")
        for i, pdf in enumerate(original_files[:10], 1):
            print(f"     {i}. {os.path.basename(pdf)}")
        if len(original_files) > 10:
            print(f"     ... e mais {len(original_files) - 10} arquivo(s)")
        
        # ==========================================
        # PASSO 2: SEPARAR PDFs POR PÁGINA
        # ==========================================
        print("\n" + "  " + "=" * 60)
        print("  📍 PASSO 2: SEPARANDO PDFs COM MÚLTIPLAS PÁGINAS")
        print("  " + "=" * 60)
        
        print("\n  🔄 Processando arquivos...")
        all_split_files = []
        
        for i, pdf_file in enumerate(original_files, 1):
            print(f"\n  [{i}/{len(original_files)}] {os.path.basename(pdf_file)}")
            
            try:
                split_results = split_pdf_by_page(pdf_file)
                
                if split_results and len(split_results) > 1:
                    all_split_files.extend(split_results)
                    print(f"       ✅ Separado em {len(split_results)} página(s)")
                else:
                    all_split_files.append(pdf_file)
                    print(f"       ℹ️  Documento único (1 página)")
                    
            except Exception as e:
                print(f"       ❌ Erro ao separar: {str(e)}")
                all_split_files.append(pdf_file)
        
        print(f"\n  📊 Total de documentos após separação: {len(all_split_files)}")
        
        # ==========================================
        # PASSO 3: EXTRAIR DADOS DE CADA DOCUMENTO
        # ==========================================
        print("\n" + "  " + "=" * 60)
        print("  📍 PASSO 3: EXTRAINDO DADOS DOS DOCUMENTOS")
        print("  " + "=" * 60)
        
        print("\n  🔍 Analisando conteúdo...")
        extracted_data = []
        
        for i, pdf_file in enumerate(all_split_files, 1):
            print(f"\n  [{i}/{len(all_split_files)}] Analisando: {os.path.basename(pdf_file)}")
            
            try:
                data = extract_pdf_data(pdf_file)
                extracted_data.append(data)
                
                print(f"       📋 Tipo: {data.get('tipo', 'N/A')}")
                print(f"       💰 Valor: R$ {data.get('valor', 'N/A')}")
                print(f"       📅 Data: {data.get('data', 'N/A')}")
                
                if 'erro' in data:
                    print(f"       ⚠️  Aviso: {data['erro']}")
                    
            except Exception as e:
                print(f"       ❌ Erro na extração: {str(e)}")
                extracted_data.append({
                    'arquivo': pdf_file,
                    'tipo': 'Erro',
                    'erro': str(e)
                })
        
        # ==========================================
        # PASSO 4: CRIAR ESTRUTURA DE PASTAS
        # ==========================================
        print("\n" + "  " + "=" * 60)
        print("  📍 PASSO 4: CRIANDO ESTRUTURA DE PASTAS")
        print("  " + "=" * 60)
        
        folders = create_output_folders(base_path)
        print("\n  ✅ Estrutura de pastas criada!")
        
        # ==========================================
        # PASSO 5: ORGANIZAR ARQUIVOS POR TIPO
        # ==========================================
        print("\n" + "  " + "=" * 60)
        print("  📍 PASSO 5: ORGANIZANDO ARQUIVOS POR TIPO")
        print("  " + "=" * 60)
        
        print("\n  📦 Movendo arquivos para pastas correspondentes...")
        
        stats = {
            "notas_fiscais": 0,
            "recibos": 0,
            "outros": 0,
            "erros": 0
        }
        
        for data in extracted_data:
            try:
                arquivo = data.get('arquivo')
                tipo = data.get('tipo', 'Outros')
                
                # Determina pasta de destino
                if "Nota Fiscal" in tipo:
                    destino_folder = folders['notas_fiscais']
                    stats['notas_fiscais'] += 1
                    categoria = "Nota Fiscal"
                elif "Recibo" in tipo:
                    destino_folder = folders['recibos']
                    stats['recibos'] += 1
                    categoria = "Recibo"
                else:
                    destino_folder = folders['outros']
                    stats['outros'] += 1
                    categoria = "outros"
                
                # Copia arquivo para a pasta
                destino_file = os.path.join(destino_folder, os.path.basename(arquivo))
                
                # Evita sobrescrever
                if os.path.exists(destino_file):
                    base_name = os.path.splitext(os.path.basename(arquivo))[0]
                    ext = os.path.splitext(os.path.basename(arquivo))[1]
                    counter = 1
                    while os.path.exists(destino_file):
                        new_name = f"{base_name}_{counter}{ext}"
                        destino_file = os.path.join(destino_folder, new_name)
                        counter += 1
                
                shutil.copy2(arquivo, destino_file)
                print(f"  ✅ {os.path.basename(arquivo)} → {categoria}")
                
            except Exception as e:
                print(f"  ❌ Erro ao organizar {os.path.basename(arquivo)}: {str(e)}")
                stats['erros'] += 1
        
        # ==========================================
        # PASSO 6: RELATÓRIO FINAL
        # ==========================================
        print("\n" + "  " + "=" * 60)
        print("  📍 PASSO 6: RELATÓRIO FINAL")
        print("  " + "=" * 60)
        
        # Calcular totais
        total_valor_notas = 0
        total_valor_recibos = 0
        
        for data in extracted_data:
            valor_str = data.get('valor')
            tipo = data.get('tipo', '')
            
            if valor_str and valor_str != 'N/A':
                try:
                    # Converter "1.234,56" para 1234.56
                    valor_num = float(valor_str.replace('.', '').replace(',', '.'))
                    
                    if "Nota Fiscal" in tipo:
                        total_valor_notas += valor_num
                    elif "Recibo" in tipo:
                        total_valor_recibos += valor_num
                except:
                    pass
        
        print("\n  📊 ESTATÍSTICAS GERAIS:")
        print("  " + "-" * 60)
        print(f"     📁 Arquivos originais: {len(original_files)}")
        print(f"     📄 Documentos processados: {len(all_split_files)}")
        print(f"     ✅ Dados extraídos: {len(extracted_data)}")
        
        print("\n  📋 DOCUMENTOS POR TIPO:")
        print("  " + "-" * 60)
        print(f"     📄 Notas Fiscais: {stats['notas_fiscais']}")
        print(f"     🧾 Recibos: {stats['recibos']}")
        print(f"     ❓ Outros: {stats['outros']}")
        print(f"     ❌ Erros: {stats['erros']}")
        
        print("\n  💰 VALORES TOTAIS:")
        print("  " + "-" * 60)
        print(f"     📄 Notas Fiscais: R$ {total_valor_notas:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        print(f"     🧾 Recibos: R$ {total_valor_recibos:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        print(f"     💵 Total Geral: R$ {(total_valor_notas + total_valor_recibos):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        
        print("\n  📂 ESTRUTURA DE PASTAS CRIADA:")
        print("  " + "-" * 60)
        for nome, caminho in folders.items():
            qtd_arquivos = len([f for f in os.listdir(caminho) if f.endswith('.pdf')]) if os.path.exists(caminho) else 0
            print(f"     📁 {nome}: {qtd_arquivos} arquivo(s)")
            print(f"        {caminho}")
        
        print("\n  " + "=" * 60)
        print("  ✅ PROCESSAMENTO CONCLUÍDO COM SUCESSO!")
        print("  " + "=" * 60)
        
        return {
            'stats': stats,
            'total_notas': total_valor_notas,
            'total_recibos': total_valor_recibos,
            'folders': folders
        }
        
    except Exception as e:
        print(f"\n  ❌ ERRO CRÍTICO: {str(e)}")
        import traceback
        print(f"\n  📋 Detalhes do erro:")
        print(traceback.format_exc())
        return None


def test_9_organize_files(base_path):
    """TESTE 9: Organizar arquivos em pastas por tipo"""
    print_header("TESTE 9: Organizar Arquivos por Tipo")
    
    # CONFIGURE ESTE CAMINHO
    # base_path = "C:/Users/matheus.recieri/Desktop/Empresas/EmpresaABC/Contabil/2025"
    
    print(f"\n  📁 Diretório: {base_path}")
    print("  ⚠️  ATENÇÃO: Isso vai criar pastas e copiar arquivos!")
    print("  💡 Descomente esta função no main() para executar")
    
    return {}
    
    # Descomente abaixo para executar de verdade:
    # if not os.path.exists(base_path):
    #     print(f"  ❌ ERRO: Diretório não encontrado!")
    #     return {}
    
    # try:
    #     # copy_mode=True: COPIA (mantém originais)
    #     # copy_mode=False: MOVE (remove originais)
    #     stats = organize_files(base_path, copy_mode=True)
    #     return stats
    # except Exception as e:
    #     print(f"  ❌ ERRO: {str(e)}")
    #     return {}


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
    test_8_full_workflow(base_path)
    
    # Teste de organização (descomente para usar)
    # test_9_organize_files()
    
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