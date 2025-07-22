from fastapi import FastAPI, UploadFile, File, HTTPException
import os 
from datetime import datetime
from utils.pdf import extract_text_from_pdf, clean_text
from utils.summary import generate_summary

# Inicializa o FastAPI (cria a "aplicação web")
app = FastAPI(title="DataWizard Mini", description="API para resumir PDFs")

# Configuração
UPLOAD_DIR = "uploads" # Pasta onde os PDFs serão salvos
os.makedirs(UPLOAD_DIR, exist_ok=True) # Cria a pasta se não existir

# Rota raiz(apenas para teste)
@app.get("/")
def home():
    return {"message": "Bem-vindo ao DataWizard Mini!"
            "Envie um PDF para/upload para obter um resumo!"}

# Rota para upload de arquivos PDF
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Recebe um arquivo PDF e retorna informações básicas.
    
    Parâmetros:
    - file: Arquivo enviado pelo usuário (Obrigatório ser PDF).

    Retorna:
    - Nome do arquivo, caminho de salvamento e data de upload.
    """

    # Validação do tipo de arquivo
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Apenas arquivos .pdf são aceitos!"
        )
    
    # Gera um nome único para o arquivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    
    try:
        # Salva o arquivo no servidor
        with open(filepath, "wb") as f:
            content = await file.read() # Lê o conteúdo do arquivo
            f.write(content) # Escreve no disco

        # Extrai o texto e calcula métricas
        extracted_text = extract_text_from_pdf(filepath) 
        cleaned_text = clean_text(extracted_text)
        summary = generate_summary(cleaned_text) # Gera o resumo do texto limpo
        word_count = len(extracted_text.split())

        # Resposta completa
        return {
            "filename": file.filename,
            "saved_path": filepath,
            "upload_time": timestamp,
            "text_sample": extracted_text[:200] + "..." if len(extracted_text) > 200 else extracted_text,
            "word_count": word_count,
            "status": "success",
            "summary": generate_summary(extracted_text),
            "summary_sentences": 3
        }
    except Exception as e:
        # Remove o arquivo se ocorrer um erro após o salvamento
        if os.path.exists(filepath):
            os.remove(filepath)
        raise HTTPException(500, detail=f"Erro ao processar PDF: {str(e)}")

