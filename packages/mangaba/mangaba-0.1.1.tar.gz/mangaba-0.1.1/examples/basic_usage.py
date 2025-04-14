#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Exemplo básico de uso do pacote Mangaba.

Este script demonstra como configurar e usar o Mangaba para criar
uma equipe simples de agentes.
"""

import asyncio
import os

# Importando o pacote principal
import mangaba
from mangaba.config import configure_api

# Definir sua chave API do Gemini (obtenha em https://ai.google.dev/)
API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not API_KEY:
    API_KEY = input("Digite sua chave de API do Gemini: ")

# Configurar a API
configure_api(API_KEY)

async def simple_example():
    """Exemplo simples de uso com um único agente"""
    # Criação dos componentes básicos
    memory = mangaba.ContextualMemory()
    model = mangaba.GeminiModel()
    search_tool = mangaba.GoogleSearchTool()
    
    # Criação do agente
    pesquisador = mangaba.Agent(
        name="Pesquisador", 
        role="Encontra informações", 
        model=model, 
        tools=[search_tool], 
        memory=memory
    )
    
    # Definição da tarefa
    tarefa = mangaba.Task(
        description="Quais são as tendências tecnológicas para 2025?", 
        agent=pesquisador
    )
    
    # Execução
    equipe = mangaba.Crew(agents=[pesquisador], tasks=[tarefa])
    await equipe.run()
    
    # Resultado
    print("\nResultado final:")
    print(tarefa.result)

if __name__ == "__main__":
    asyncio.run(simple_example()) 