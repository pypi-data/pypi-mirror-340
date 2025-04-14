[![PyPI version](https://badge.fury.io/py/mangaba.svg)](https://badge.fury.io/py/mangaba)

# Mangaba - Framework de Automação com Agentes Inteligentes

<img src="https://github.com/dheiver2/mangaba_ai/blob/main/img.png" width="300">

Framework Python para criação de equipes de agentes AI autônomos que colaboram para resolver tarefas complexas.

## ✨ Funcionalidades Principais

- **Arquitetura Multi-Agente**: Crie equipes de agentes especializados
- **Memória Contextual**: Histórico individual e compartilhado entre agentes
- **Integração Gemini**: Utilize os modelos mais avançados da Google
- **Ferramentas Externas**: Busca no Google e outras APIs
- **Gerenciamento de Tarefas**: Dependências e priorização automática
- **Processamento Assíncrono**: Execução paralela para maior eficiência

## 🚀 Começando

### Pré-requisitos
- Python 3.9+
- Conta no Google AI Studio (para API key do Gemini)

### Instalação

**Método 1: Instalação via pip (mais simples)**
```bash
pip install mangaba
```

**Método 2: Instalação direta do repositório com pré-instalação**
```bash
git clone https://github.com/dheiver2/mangaba_ai.git
cd mangaba_ai
# Execute o script de pré-instalação das dependências (recomendado)
python setup.py.pre
# Depois instale o pacote
pip install .
```

**Método 3: Instalação com requisitos em lote**
```bash
git clone https://github.com/dheiver2/mangaba_ai.git
cd mangaba_ai
# Primeiro instale as dependências
pip install -r requirements.txt
# Depois instale o pacote
pip install .
```

### Verificação da Instalação
Para verificar se o Mangaba foi instalado corretamente, execute:
```python
import mangaba
print(mangaba.__version__)  # Deve exibir a versão atual
```

### Solução de problemas

1. Se encontrar erros sobre dependências, instale-as manualmente:
```bash
pip install google-generativeai googlesearch-python requests aiohttp tenacity
```

2. Para ambiente Windows com problemas de codificação:
```bash
set PYTHONIOENCODING=utf-8
pip install mangaba
```

3. Em caso de falha na instalação em modo editável:
```bash
python setup.py develop
```

### Configuração
1. Obtenha sua API key do Gemini em https://ai.google.dev/
2. Configure a API em seu código:

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

# Configure a API (veja seção de configuração)

async def exemplo():
    # Criação dos agentes
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

    # Definição de tarefas
    tarefa = mangaba.Task(
        description="Buscar inovações em IA", 
        agent=pesquisador
    )

    # Execução
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
├── config/            # Módulo de configuração
│   ├── __init__.py
│   └── api.py         # Funções para configuração da API
├── core/              # Módulo principal
│   ├── __init__.py
│   └── models.py      # Definições das classes principais
└── cases/             # Casos de uso
    ├── __init__.py
    └── cases.py       # Exemplos prontos
```

## 🤝 Como Contribuir

1. Faça um fork do projeto
2. Crie sua branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Distribuído sob licença MIT. Veja `LICENSE` para mais informações.

## ✉️ Contato

Dheiver Santos - [@dheiver](https://github.com/dheiver2) - dheiver.santos@gmail.com

Project Link: [https://github.com/dheiver2/mangaba_ai](https://github.com/dheiver2/mangaba_ai)