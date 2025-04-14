# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import subprocess
import sys

# Garantir que as dependências básicas de build estejam instaladas
try:
    import pip
    print("[-] pip está instalado")
except ImportError:
    print("[!] pip não está instalado corretamente")

# Instalando dependências antes da build
DEPENDENCIES = [
    "google-generativeai>=0.8.3",
    "googlesearch-python>=1.2.1",
    "requests>=2.32.3",
    "aiohttp>=3.10.5",
    "tenacity>=8.5.0",
]

print("[+] Instalando dependências necessárias para a build...")
for dep in DEPENDENCIES:
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", dep],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print(f"  [+] {dep}")
    except subprocess.CalledProcessError:
        print(f"  [!] Falha ao instalar {dep}")

# Carrega o README para a descrição longa
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mangaba",
    version="0.1.1-dev",
    description="Framework Python para criação de equipes de agentes AI autônomos",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Dheiver Santos",
    author_email="dheiver.santos@gmail.com",
    url="https://github.com/dheiver2/mangaba_ai",
    packages=find_packages(),
    install_requires=DEPENDENCIES,
    setup_requires=["wheel"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.9",
    keywords="ai, agents, llm, gemini, autonomous",
) 