import fitz #PyMuPDP
import re

def extract_text_from_pdf(filepath: str) -> str:
    """"
    Extrai o texto de um arquivo PDF

    Parâmetros:
    - filepath: Caminho completo do arquivo PDF

    Retorna:
    - Texto extraido(Como string)
    """

    text = ""

    try:
        # Abre o PDF
        doc = fitz.open(filepath)

        # Itera pelas páginas e extrai o texto
        for page in doc:
            text += page.get_text()

        return text.strip()
    
    except Exception as e:
        raise Exception(f"Erro ao extrair texto do PDF: {str(e)}")

def clean_text(text: str) -> str:
    """"
    Remove informações sensiveis e formata o texto extraído do PDF

    Parâmetros:
    - text: Texto Cru extraído do PDF

    Retorna:
    - Texto limpo e formatado
    """

    # 1. Remove e-mails
    text = re.sub(r'\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b', '[EMAIL]', text)

    # 2. Remove números de telefone
    text = re.sub(r'\(?\d{2}\)?[\s-]?\d{4,5}[\s-]?\d{4}\b', '[TEL]', text)

    # 3. Remove múltiplos espaços/quebras de linha
    text = re.sub(r'\s+', ' ', text).strip()

    return text