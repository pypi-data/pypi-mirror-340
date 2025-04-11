"""
Interface de linha de comando para o framework OrNexus
"""

import os
import sys
import argparse
import shutil
from pathlib import Path
import asyncio
import re

def normalize_class_name(project_name):
    """
    Normaliza o nome do projeto para usar como nome de classe
    
    Args:
        project_name: Nome do projeto
        
    Returns:
        Nome da classe normalizado (PascalCase)
    """
    # Remover caracteres não alfanuméricos e substituir por espaços
    normalized = re.sub(r'[^a-zA-Z0-9]', ' ', project_name)
    # Dividir em palavras, capitalizar cada palavra e juntar
    return ''.join(word.capitalize() for word in normalized.split())

def create_project_structure(project_name):
    """
    Cria a estrutura básica de um novo projeto
    
    Args:
        project_name: Nome do projeto a ser criado
    """
    # Obter o diretório do pacote ornexus
    package_dir = Path(__file__).parent.absolute()
    
    # Normalizar o nome do projeto para nome de classe
    class_name = normalize_class_name(project_name)
    
    # Criar o diretório do projeto
    project_dir = Path(project_name)
    if project_dir.exists():
        print(f"Erro: O diretório {project_name} já existe.")
        return False
    
    # Criar estrutura de diretórios
    dirs = [
        project_dir,
        project_dir / "config",
        project_dir / "knowledge",
        project_dir / "knowledge" / "macro",
    ]
    
    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"Criado diretório: {dir_path}")
    
    # Copiar arquivos de template
    templates = {
        package_dir / "config" / "agents.yaml": project_dir / "config" / "agents.yaml",
        package_dir / "config" / "tasks.yaml": project_dir / "config" / "tasks.yaml",
    }
    
    for src, dest in templates.items():
        shutil.copy2(src, dest)
        print(f"Copiado: {src} -> {dest}")
    
    # Criar arquivo README.txt no diretório knowledge
    readme_path = project_dir / "knowledge" / "README.txt"
    with open(readme_path, "w") as f:
        f.write("# Diretório de conhecimento para OrNexus\n\n")
        f.write("Coloque seus arquivos de conhecimento (.txt) neste diretório para uso pelo framework.\n")
    print(f"Criado arquivo: {readme_path}")
    
    # Criar arquivo __init__.py do projeto
    with open(project_dir / "__init__.py", "w") as f:
        f.write('"""Projeto gerado pelo framework OrNexus"""\n\n')
    
    # Criar arquivo main.py do projeto
    with open(project_dir / "main.py", "w") as f:
        f.write(f'''"""
Aplicação principal baseada no framework OrNexus
"""

from typing import Dict, Any, Optional
from pathlib import Path
import os
from datetime import datetime

from agno.agent import Agent
from agno.team import Team
from agno.models.anthropic import Claude

from agno.knowledge.text import TextKnowledgeBase
from agno.document.chunking.recursive import RecursiveChunking
from agno.vectordb.mongodb import MongoDb

from ornexus import OrNexusConfig, agent

# Usando diretamente a conexão do MongoDB Atlas
mongodb_uri = os.getenv("MONGODB_CONN")
print(f"Usando MongoDB URI: {{mongodb_uri}}")

# 1. Verifique se o diretório knowledge existe
knowledge_dir = Path("knowledge")
if not knowledge_dir.exists():
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    print(f"Criado diretório: {{knowledge_dir.absolute()}}")
    
    # Criar um arquivo README.txt de exemplo
    readme_path = knowledge_dir / "README.txt"
    if not readme_path.exists():
        with open(readme_path, "w") as f:
            f.write("# Diretório de conhecimento para OrNexus\\n\\n")
            f.write("Coloque seus arquivos de conhecimento (.txt) neste diretório para uso pelo framework.\\n")

# Garantir que o diretório macro existe
macro_dir = knowledge_dir / "macro"
if not macro_dir.exists():
    macro_dir.mkdir(parents=True, exist_ok=True)
    print(f"Criado diretório: {{macro_dir.absolute()}}")

# Contador de arquivos de texto
txt_files = list(knowledge_dir.glob('*.txt'))
print(f"Encontrados {{len(txt_files)}} arquivos de texto (.txt) em {{knowledge_dir}}")

# Contador de arquivos de texto na pasta macro
macro_txt_files = list(macro_dir.glob('*.txt'))
print(f"Encontrados {{len(macro_txt_files)}} arquivos de texto (.txt) em {{macro_dir}}")

# 2. Inicialização corrigida do TextKnowledgeBase
macro_knowledge = TextKnowledgeBase(
    path=str(macro_dir),  # Caminho para a pasta macro com arquivos .txt
    vector_db=MongoDb(
        database="ornexus_knw",
        collection_name="knowledge", 
        db_url=mongodb_uri,
        wait_until_index_ready=60,
        wait_after_insert=300
    ),
    chunking_strategy=RecursiveChunking()
)

@OrNexusConfig
class {class_name}:
    """Aplicação baseada no framework OrNexus"""
    
    def __init__(self, recreate=False):
        self.sonnet3_7 = Claude(
            id="claude-3-7-sonnet-20250219",
            temperature=0.0,
            max_tokens=8000
        )
        self.macro_knowledge = macro_knowledge
        if recreate:
            self.macro_knowledge.load(recreate=True)
        else:
            self.macro_knowledge.load(recreate=False)
        
    @agent
    def pesquisador(self) -> Agent:
        return Agent(
            name="Pesquisador Econômico",
            role=self.config_agents['researcher']['role'],
            goal=self.config_agents['researcher']['goal'],
            description=self.config_agents['researcher']['backstory'],
            instructions=self.config_tasks['pesquisador']['description'],
            expected_output=self.config_tasks['pesquisador']['expected_output'],
            model=self.sonnet3_7,
            debug_mode=True,
            telemetry=False,
            knowledge=self.macro_knowledge
        )
    
    @agent
    def redator_twitter(self) -> Agent:
        return Agent(
            name="Redator de Conteúdo para Twitter",
            role=self.config_agents['content_writer']['role'],
            goal=self.config_agents['content_writer']['goal'],
            description=self.config_agents['content_writer']['backstory'],
            instructions=self.config_tasks['redator_twitter']['description'],
            expected_output=self.config_tasks['redator_twitter']['expected_output'],
            model=self.sonnet3_7,
            debug_mode=True,
            telemetry=False,
            knowledge=self.macro_knowledge
        )
    
    def team(self) -> Team:
        return Team(
            mode="collaborate",
            members=self.agents,
            model=self.sonnet3_7,
            debug_mode=True,
            success_criteria="Uma análise econômica completa com conteúdo pronto para redes sociais.",
            telemetry=False
        )

async def main(**kwargs):
    try:
        if 'inputs' in kwargs:
            result = await {class_name}().team().arun(kwargs['inputs'])
            return result
        else:
            print("Nenhum input fornecido.")
            return None
    except Exception as e:
        print(f"Erro: {{e}}")
        return None

if __name__ == "__main__":
    import asyncio
    inputs = {{
        "topico": "Impactos da política monetária dos bancos centrais em mercados emergentes",
        "tema": "Como as decisões do FED afetam economias emergentes em 2024",
        "data_referencia": datetime.now().strftime("%Y-%m-%d"),
        "extra_instruction": "Considere os impactos da política monetária recente dos bancos centrais e tendências inflacionárias."
    }}
    result = asyncio.run(main(inputs=inputs))
    print(result)
''')
    
    # Criar arquivo para executar o projeto
    with open(project_dir / "__main__.py", "w") as f:
        f.write(f'''"""
Ponto de entrada para execução do projeto
"""

import asyncio
from .main import main, {class_name}
from datetime import datetime

if __name__ == "__main__":
    inputs = {{
        "topico": "Impactos da política monetária dos bancos centrais em mercados emergentes",
        "tema": "Como as decisões do FED afetam economias emergentes em 2024",
        "data_referencia": datetime.now().strftime("%Y-%m-%d"),
        "extra_instruction": "Considere os impactos da política monetária recente dos bancos centrais e tendências inflacionárias."
    }}
    result = asyncio.run(main(inputs=inputs))
    print(result)
''')
    
    print(f"\nProjeto '{project_name}' criado com sucesso!")
    print(f"Classe principal: {class_name}")
    print("\nPara executar o projeto, use:")
    print(f"  cd {project_name}")
    print(f"  python -m {project_name}")
    
    return True

def main():
    """Função principal da CLI"""
    parser = argparse.ArgumentParser(description="OrNexus CLI - Framework para criação de agentes")
    subparsers = parser.add_subparsers(dest="command", help="Comando a ser executado")
    
    # Comando 'init'
    init_parser = subparsers.add_parser("init", help="Inicializa um novo projeto")
    init_parser.add_argument("project_name", help="Nome do projeto a ser criado")
    
    # Comando 'run'
    run_parser = subparsers.add_parser("run", help="Executa um projeto existente")
    run_parser.add_argument("project_path", help="Caminho para o projeto")
    run_parser.add_argument("--input", "-i", help="Arquivo JSON com os inputs")
    
    # Comando 'version'
    version_parser = subparsers.add_parser("version", help="Mostra a versão do framework")
    
    args = parser.parse_args()
    
    if args.command == "init":
        create_project_structure(args.project_name)
    
    elif args.command == "run":
        # Implementar a execução direta de projetos
        print("Execução direta de projetos não implementada ainda.")
    
    elif args.command == "version":
        from ornexus import __version__
        print(f"OrNexus v{__version__}")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

def init_project():
    """
    Inicializa o projeto OrNexus:
    - Cria diretório knowledge
    - Cria diretório knowledge/macro
    - Cria arquivo README.txt
    """
    # Criar diretório knowledge se não existir
    knowledge_dir = Path("knowledge")
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    print(f"✅ Diretório {knowledge_dir} criado!")

    # Criar diretório macro se não existir
    macro_dir = knowledge_dir / "macro"
    macro_dir.mkdir(parents=True, exist_ok=True)
    print(f"✅ Diretório {macro_dir} criado!")

    # Criar arquivo README.txt no diretório knowledge
    readme_path = knowledge_dir / "README.txt"
    with open(readme_path, "w") as f:
        f.write("# Diretório de conhecimento para OrNexus\n\n")
        f.write("Coloque seus arquivos de conhecimento (.txt) neste diretório para uso pelo framework.\n")
    print(f"✅ Arquivo {readme_path} criado!")

def show_knowledge_summary():
    """
    Exibe um resumo dos arquivos de conhecimento
    """
    try:
        # 1. Verifique se o diretório knowledge existe
        knowledge_dir = Path("knowledge")
        if not knowledge_dir.exists():
            print(f"❌ Diretório {knowledge_dir} não encontrado!")
            return
            
        # Verifica pasta macro
        macro_dir = knowledge_dir / "macro"
        if not macro_dir.exists():
            print(f"❌ Diretório {macro_dir} não encontrado!")
            macro_dir.mkdir(parents=True, exist_ok=True)
            print(f"✅ Diretório {macro_dir} criado!")
            
        # Contador de arquivos de texto na pasta principal
        txt_files = list(knowledge_dir.glob('*.txt'))
        print(f"Encontrados {len(txt_files)} arquivos de texto (.txt) em {knowledge_dir}")
        
        # Contador de arquivos de texto na pasta macro
        macro_txt_files = list(macro_dir.glob('*.txt'))
        print(f"Encontrados {len(macro_txt_files)} arquivos de texto (.txt) em {macro_dir}")
        
    except Exception as e:
        print(f"Erro ao exibir resumo dos arquivos de conhecimento: {e}") 