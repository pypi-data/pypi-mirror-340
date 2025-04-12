# -*- coding: utf-8 -*-
# mangaba/cases/cases.py
# Casos de uso do Mangaba

import asyncio
from mangaba.core.models import ContextualMemory, GeminiModel, GoogleSearchTool, Agent, Task, Crew

# Case de Uso 1: Analise de Tendencias de Mercado
async def case_mercado():
    print("\n=== Case 1: Analise de Tendencias de Mercado ===")
    memory = ContextualMemory(max_context_size=5)
    model = GeminiModel(temperature=0.8, top_k=50)
    search_tool = GoogleSearchTool()

    pesquisador = Agent(name="Pesquisador", role="Busca dados", model=model, tools=[search_tool], memory=memory)
    analista = Agent(name="Analista", role="Analisa dados", model=model, memory=memory)
    escritor = Agent(name="Escritor", role="Escreve relatorio", model=model, memory=memory)

    tarefa_pesquisa = Task(description="Buscar dados sobre tendencias em tecnologias verdes em 2025", agent=pesquisador, priority=2)
    tarefa_analise = Task(description="Analisar os dados encontrados", agent=analista, priority=1, dependencies=[tarefa_pesquisa])
    tarefa_relatorio = Task(description="Gerar relatorio executivo", agent=escritor, priority=0, dependencies=[tarefa_analise])

    equipe = Crew(agents=[pesquisador, analista, escritor], tasks=[tarefa_pesquisa, tarefa_analise, tarefa_relatorio])
    await equipe.run()

# Case de Uso 2: Planejamento Educacional
async def case_educacao():
    print("\n=== Case 2: Planejamento Educacional ===")
    memory = ContextualMemory(max_context_size=5)
    model = GeminiModel(temperature=0.8, top_k=50)
    search_tool = GoogleSearchTool()

    pesquisador = Agent(name="Pesquisador", role="Busca dados", model=model, tools=[search_tool], memory=memory)
    analista = Agent(name="Analista", role="Analisa dados", model=model, memory=memory)
    escritor = Agent(name="Escritor", role="Escreve relatorio", model=model, memory=memory)

    tarefa_pesquisa = Task(description="Buscar dados sobre IA na educacao em 2025", agent=pesquisador, priority=2)
    tarefa_analise = Task(description="Analisar os dados encontrados", agent=analista, priority=1, dependencies=[tarefa_pesquisa])
    tarefa_relatorio = Task(description="Gerar relatorio executivo", agent=escritor, priority=0, dependencies=[tarefa_analise])

    equipe = Crew(agents=[pesquisador, analista, escritor], tasks=[tarefa_pesquisa, tarefa_analise, tarefa_relatorio])
    await equipe.run()

# Funcao principal para execucao
async def main():
    await case_mercado()
    await case_educacao()

if __name__ == "__main__":
    asyncio.run(main())  # Usa asyncio.run para execucao fora do Colab; no Colab, use await main() 