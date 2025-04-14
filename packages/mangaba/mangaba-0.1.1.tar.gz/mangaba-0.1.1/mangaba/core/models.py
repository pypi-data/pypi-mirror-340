# -*- coding: utf-8 -*-
# mangaba/core/models.py
# Definições das classes principais do Mangaba

import asyncio
from typing import List, Optional, Dict
from dataclasses import dataclass

try:
    import google.generativeai as genai
except ImportError:
    raise ImportError(
        "O pacote 'google-generativeai' não está instalado. "
        "Execute 'pip install google-generativeai' para instalá-lo."
    )

try:
    from googlesearch import search
except ImportError:
    raise ImportError(
        "O pacote 'googlesearch-python' não está instalado. "
        "Execute 'pip install googlesearch-python' para instalá-lo."
    )

# ContextualMemory (com memória global)
class ContextualMemory:
    def __init__(self, max_context_size: int = 10):
        self.individual_data: Dict[str, List[str]] = {}
        self.global_data: List[str] = []
        self.max_context_size = max_context_size

    def store_individual(self, agent_name: str, content: str):
        agent_history = self.individual_data.setdefault(agent_name, [])
        agent_history.append(content)
        if len(agent_history) > self.max_context_size:
            agent_history.pop(0)

    def store_global(self, content: str):
        self.global_data.append(content)
        if len(self.global_data) > self.max_context_size:
            self.global_data.pop(0)

    def retrieve_individual(self, agent_name: str) -> List[str]:
        return self.individual_data.get(agent_name, [])

    def retrieve_global(self) -> List[str]:
        return self.global_data

# GeminiModel (com tratamento de erro)
class GeminiModel:
    def __init__(self, model_name: str = "gemini-1.5-flash", temperature: float = 0.7, top_k: int = 40):
        self.model = genai.GenerativeModel(model_name)
        self.temperature = temperature
        self.top_k = top_k

    async def generate(self, prompt: str) -> str:
        try:
            await asyncio.sleep(0.5)  # Simula latência
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=self.temperature,
                    top_k=self.top_k
                )
            )
            return response.text
        except Exception as e:
            return f"Erro na geração: {str(e)}"

# GoogleSearchTool (busca real)
class GoogleSearchTool:
    async def run(self, query: str) -> str:
        await asyncio.sleep(0.3)  # Simula latência de rede
        try:
            results = list(search(query, num_results=3))
            return f"Resultados da busca: {', '.join(results)}"
        except Exception as e:
            return f"Erro na busca: {str(e)}"

# Agent
class Agent:
    def __init__(self, name: str, role: str, model, tools: Optional[List] = None, memory=None):
        self.name = name
        self.role = role
        self.model = model
        self.tools = tools or []
        self.memory = memory

    async def execute(self, input_text: str, dependencies: List[str] = None) -> str:
        print(f"[{self.name}] Executando: {input_text}")

        individual_context = self.memory.retrieve_individual(self.name) if self.memory else []
        global_context = self.memory.retrieve_global() if self.memory else []
        deps_text = f"Dependências: {dependencies}" if dependencies else ""
        enriched_input = (
            f"Contexto individual: {individual_context[-3:]}\n"
            f"Contexto global: {global_context[-3:]}\n"
            f"{deps_text}\nTarefa: {input_text}"
        )

        tool_outputs = []
        for tool in self.tools:
            tool_result = await tool.run(input_text)
            tool_outputs.append(f"[{tool.__class__.__name__}] {tool_result}")

        final_input = f"{enriched_input}\nResultados das ferramentas: {tool_outputs}" if tool_outputs else enriched_input

        response = await self.model.generate(final_input)

        if len(response) < 50:
            response = await self.model.generate(f"{final_input}\nPor favor, forneça mais detalhes.")

        if self.memory:
            self.memory.store_individual(self.name, f"Entrada: {input_text}\nResposta: {response}")
            self.memory.store_global(f"[{self.name}] {response}")

        return response

# Task
@dataclass
class Task:
    description: str
    agent: "Agent"
    priority: int = 0
    dependencies: Optional[List["Task"]] = None
    result: Optional[str] = None
    executed: bool = False  # Controle para evitar reexecução

    def get_dependencies_results(self) -> List[str]:
        if not self.dependencies:
            return []
        return [task.result for task in self.dependencies if task.result]

# Crew (com controle de execução)
class Crew:
    def __init__(self, agents: List[Agent], tasks: List[Task]):
        self.agents = {agent.name: agent for agent in agents}
        self.tasks = sorted(tasks, key=lambda t: t.priority, reverse=True)

    async def run_task(self, task: Task):
        if task.executed:  # Evita executar a mesma tarefa mais de uma vez
            return

        if task.dependencies:
            await asyncio.gather(*(self.run_task(dep) for dep in task.dependencies if not dep.executed))

        agent = self.agents[task.agent.name]
        dependencies_results = task.get_dependencies_results()
        result = await agent.execute(task.description, dependencies_results)
        task.result = result
        task.executed = True  # Marca como executada
        print(f"[{agent.name}] Resultado: {result}")

    async def run(self):
        await asyncio.gather(*(self.run_task(task) for task in self.tasks)) 