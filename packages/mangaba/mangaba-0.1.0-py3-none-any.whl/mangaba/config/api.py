# -*- coding: utf-8 -*-
# mangaba/config/api.py
# Configuracao da API do Gemini para uso fora do Google Colab

try:
    import google.generativeai as genai
except ImportError:
    raise ImportError(
        "O pacote 'google-generativeai' nao esta instalado. "
        "Execute 'pip install google-generativeai' para instala-lo."
    )

def configure_api(api_key: str):
    """
    Configura a API do Gemini com a chave fornecida.
    
    Args:
        api_key (str): Chave de API do Gemini
        
    Returns:
        bool: True se a configuracao foi bem-sucedida
        
    Raises:
        ValueError: Se a chave de API for invalida
    """
    if not api_key:
        raise ValueError(
            "A chave da API nao pode estar vazia. "
            "Obtenha uma chave em: https://ai.google.dev/"
        )
        
    try:
        genai.configure(api_key=api_key)
        # Teste simples para verificar a API
        test_model = genai.GenerativeModel("gemini-1.5-flash")
        test_response = test_model.generate_content("Teste de API")
        print("API do Gemini configurada com sucesso!")
        return True
    except Exception as e:
        raise ValueError(f"Falha ao configurar a API do Gemini: {str(e)}") 