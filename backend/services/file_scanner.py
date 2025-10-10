import os

# recebe um string base_path que é o caminho inicial (entrada de dados do front end)
def scan_directory(base_path: str):
    dados = []  # guarda o caminho completo dos arquivos
    
    # percorre todas as pastas e subpastas a partir do base_path
    # root camniho atual da pasta
    # dirs lista de subpastas
    # files lista de arquivos dentro de root
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.lower().endswith((".pdf", ".xml")):
                full_path = os.path.join(root, file)
                dados.append(full_path) #cria o caminho completo juntando a pasta root com o nome do arquivo

    return dados            