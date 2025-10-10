from services.splitter_pdf import split_pdf_by_type

arquivos = split_pdf_by_type(r"C:\temp\multi.pdf")
print("Arquivos gerados:")
for a in arquivos:
    print(a)