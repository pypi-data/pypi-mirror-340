# Mangaba - Framework de Automacao com Agentes Inteligentes

<img src="https://github.com/dheiver2/mangaba_ai/blob/main/img.png" width="300">

Framework Python para criacao de equipes de agentes AI autonomos que colaboram para resolver tarefas complexas.

## ✨ Funcionalidades Principais

- **Arquitetura Multi-Agente**: Crie equipes de agentes especializados
- **Memoria Contextual**: Historico individual e compartilhado entre agentes
- **Integracao Gemini**: Utilize os modelos mais avancados da Google
- **Ferramentas Externas**: Busca no Google e outras APIs
- **Gerenciamento de Tarefas**: Dependencias e priorizacao automatica
- **Processamento Assincrono**: Execucao paralela para maior eficiencia

## 🚀 Comecando

### Pre-requisitos
- Python 3.9+
- Conta no Google AI Studio (para API key do Gemini)

### Instalacao

**Metodo 1: Instalacao via pip (mais simples)**
```bash
pip install mangaba
```

**Metodo 2: Instalacao direta do repositorio com pre-instalacao**
```bash
git clone https://github.com/dheiver2/mangaba_ai.git
cd mangaba_ai
# Execute o script de pre-instalacao das dependencias (recomendado)
python setup.py.pre
# Depois instale o pacote
pip install .
```

**Metodo 3: Instalacao com requisitos em lote**
```bash
git clone https://github.com/dheiver2/mangaba_ai.git
cd mangaba_ai
# Primeiro instale as dependencias
pip install -r requirements.txt
# Depois instale o pacote
pip install .
```

### Verificacao da Instalacao
Para verificar se o Mangaba foi instalado corretamente, execute:
```python
import mangaba
print(mangaba.__version__)  # Deve exibir a versao atual
```

### Solucao de problemas

1. Se encontrar erros sobre dependencias, instale-as manualmente:
```bash
pip install google-generativeai googlesearch-python requests aiohttp tenacity
```

2. Para ambiente Windows com problemas de codificacao:
```bash
set PYTHONIOENCODING=utf-8
pip install mangaba
```

3. Em caso de falha na instalacao em modo editavel:
```bash
python setup.py develop
```

### Configuracao
1. Obtenha sua API key do Gemini em https://ai.google.dev/
2. Configure a API em seu codigo:

```python
import mangaba
from mangaba.config import configure_api

# Configure a API com sua chave
configure_api("sua_chave_aqui")
```

## 📚 Exemplo de Uso

```python
import asyncio
import mangaba

# Configure a API (veja secao de configuracao)

async def exemplo():
    # Criacao dos agentes
    memory = mangaba.ContextualMemory()
    model = mangaba.GeminiModel()
    search_tool = mangaba.GoogleSearchTool()

    pesquisador = mangaba.Agent(
        name="Pesquisador", 
        role="Busca dados", 
        model=model, 
        tools=[search_tool], 
        memory=memory
    )

    # Definicao de tarefas
    tarefa = mangaba.Task(
        description="Buscar inovacoes em IA", 
        agent=pesquisador
    )

    # Execucao
    equipe = mangaba.Crew(agents=[pesquisador], tasks=[tarefa])
    await equipe.run()
    
    # Resultado
    print(tarefa.result)

if __name__ == "__main__":
    asyncio.run(exemplo())
```

## 🏗 Estrutura do Projeto

```
mangaba/
├── __init__.py        # Exporta as classes principais
├── config/            # Modulo de configuracao
│   ├── __init__.py
│   └── api.py         # Funcoes para configuracao da API
├── core/              # Modulo principal
│   ├── __init__.py
│   └── models.py      # Definicoes das classes principais
└── cases/             # Casos de uso
    ├── __init__.py
    └── cases.py       # Exemplos prontos
```

## 🤝 Como Contribuir

1. Faca um fork do projeto
2. Crie sua branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudancas (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licenca

Distribuido sob licenca MIT. Veja `LICENSE` para mais informacoes.

## ✉️ Contato

Dheiver Santos - [@dheiver](https://github.com/dheiver2) - dheiver.santos@gmail.com

Project Link: [https://github.com/dheiver2/mangaba_ai](https://github.com/dheiver2/mangaba_ai)