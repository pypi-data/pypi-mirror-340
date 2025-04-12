# -*- coding: utf-8 -*-
"""
Mangaba - Framework de Automacao com Agentes Inteligentes

Um framework Python para criacao de equipes de agentes AI autonomos 
que colaboram para resolver tarefas complexas.
"""

__version__ = "0.1.0"

# Verificacao e instalacao automatica de dependencias
import importlib.util
import subprocess
import sys
import warnings


def _check_and_install_dependency(package_name, pip_name=None):
    """Verifica se um pacote esta instalado e o instala se necessario."""
    if pip_name is None:
        pip_name = package_name
    
    if importlib.util.find_spec(package_name) is None:
        warnings.warn(
            f"Dependencia '{package_name}' nao encontrada. Instalando automaticamente...",
            ImportWarning
        )
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", pip_name],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print(f"[+] {package_name} instalado com sucesso!")
        except subprocess.CalledProcessError:
            raise ImportError(
                f"Nao foi possivel instalar '{pip_name}' automaticamente. "
                f"Por favor, instale manualmente com 'pip install {pip_name}'"
            )


# Verificacao de dependencias principais
_check_and_install_dependency("google", "google-generativeai>=0.8.3")
_check_and_install_dependency("googlesearch", "googlesearch-python>=1.2.1")
_check_and_install_dependency("requests", "requests>=2.32.3")
_check_and_install_dependency("aiohttp", "aiohttp>=3.10.5")
_check_and_install_dependency("tenacity", "tenacity>=8.5.0")

# Importa as classes principais para facilitar o acesso direto
from mangaba.core.models import (
    ContextualMemory,
    GeminiModel,
    GoogleSearchTool,
    Agent,
    Task,
    Crew
) 