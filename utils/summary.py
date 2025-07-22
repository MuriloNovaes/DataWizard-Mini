from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import nltk

def generate_summary(text: str, sentences_count: int = 3) -> str:
    """"
    Gera um resumo automático usando o algoritmo LSA. 

    Parâmetros:
    - text: Texto Completo extraido do PDF
    - setences_count: Quantidade de frases no resumo

    Retorna:
    - Resumo como uma única string
    """
    try:
        # Verifica e instala dependências automaticamente
        nltk.download('punkt', quiet=True)
        nltk.download('punkt_tab', quiet=True)
        
        parser = PlaintextParser.from_string(text, Tokenizer("portuguese"))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, sentences_count)
        return " ".join([str(sentence) for sentence in summary])
    
    except Exception as e:
        error_msg = f"""
        Erro ao gerar resumo. Verifique:
        1. Pacotes NLTK: execute no terminal:
           python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab')"
        2. NumPy instalado: pip install numpy
        Erro original: {str(e)}
        """
        raise Exception(error_msg)