from PyPDF2 import PdfReader

def verificar_palavra_em_pdf(caminho_pdf: str, palavra: str) -> bool:
    try:
        leitor = PdfReader(caminho_pdf)
        for pagina in leitor.pages:
            texto = pagina.extract_text()
            if texto and palavra.lower() in texto.lower():
                return True
        return False
    except Exception as e:
        print(f'Erro ao ler PDF: {e}')
        return False