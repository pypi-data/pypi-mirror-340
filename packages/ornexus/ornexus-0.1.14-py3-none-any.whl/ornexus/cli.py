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
    
    
    # Criar arquivo __init__.py do projeto
    with open(project_dir / "__init__.py", "w") as f:
        f.write('"""Projeto gerado pelo framework OrNexus"""\n\n')

    with open(project_dir / ".env", "w") as f:
        f.write('ANONYMIZED_TELEMETRY=true\n')
        f.write('OPENAI_API_KEY=\n')
        f.write('ANTHROPIC_API_KEY=\n')
        f.write('MONGODB_CONN=\n')
    
    # Criar arquivo main.py do projeto
    with open(project_dir / f"{project_name}.py", "w") as f:
        f.write(f'''from typing import Dict, Any, Optional
from pathlib import Path
import os
from datetime import datetime

from agno.agent import Agent
from agno.team import Team
from agno.models.anthropic import Claude
from agno.models.openai import OpenAIChat
from ornexus import OrNexusConfig

#===============================================================================#
# Configuração de conhecimento para o OrNexus
# Para mais informações sobre como configurar e utilizar bases de conhecimento,
# consulte a documentação oficial do Agno em: https://docs.agno.com/knowledge/introduction
#===============================================================================#

# from agno.knowledge.text import TextKnowledgeBase
# from agno.document.chunking.recursive import RecursiveChunking
# from agno.vectordb.mongodb import MongoDb

# # Exemplo de conexão do MongoDB Atlas
# mongodb_uri = os.getenv("MONGODB_CONN")
# print(f"Usando MongoDB URI: {{mongodb_uri}}")

# # Exemplo de inicialização do TextKnowledgeBase com MongoDB e RecursiveChunking
# knowledge = TextKnowledgeBase(
#     path=str(knowledge_dir),  # Caminho para a pasta knowledge com arquivos .txt
#     vector_db=MongoDb(
#         database="ornexus_knw",
#         collection_name="knowledge", 
#         db_url=mongodb_uri,
#         wait_until_index_ready=60,
#         wait_after_insert=300
#     ),
#     chunking_strategy=RecursiveChunking()
# )

@OrNexusConfig
class {class_name}:
    """Aplicação baseada no framework OrNexus"""
    
    def __init__(self, recreate=False):
        # self.knowledge = knowledge        
        # if recreate:
        #     self.knowledge.load(recreate=True)
        # else:
        #     self.knowledge.load(recreate=False)

        self.sonnet3_7 = Claude(
            id="claude-3-7-sonnet-20250219",
            temperature=0.0,
            max_tokens=8000
        )
        
        self.gpt4o = OpenAIChat(
            id="gpt-4o",
            temperature=0.0,
        )

    @OrNexusConfig.agent
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
            # knowledge=self.knowledge
        )
    
    @OrNexusConfig.agent
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
            # knowledge=self.knowledge
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
            result = await {class_name}().kickoff(kwargs['inputs'])
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
        "datenow": datetime.now().strftime("%Y-%m-%d"),
    }}
    asyncio.run(main(inputs=inputs))
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
    
    # Comando 'deploy'
    deploy_parser = subparsers.add_parser("deploy", help="Cria estrutura de API no projeto")
    deploy_parser.add_argument("--path", "-p", help="Caminho para o projeto (opcional)")
    
    # Comando 'version'
    version_parser = subparsers.add_parser("version", help="Mostra a versão do framework")
    
    args = parser.parse_args()
    
    if args.command == "init":
        create_project_structure(args.project_name)
    
    elif args.command == "run":
        # Implementar a execução direta de projetos
        print("Execução direta de projetos não implementada ainda.")
    
    elif args.command == "deploy":
        deploy_api_structure(args.path)
    
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
    """
    # Criar diretório knowledge se não existir
    knowledge_dir = Path("knowledge")
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    print(f"✅ Diretório {knowledge_dir} criado!")


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
            
        # Contador de arquivos de texto na pasta principal
        txt_files = list(knowledge_dir.glob('*.txt'))
        print(f"Encontrados {len(txt_files)} arquivos de texto (.txt) em {knowledge_dir}")
        
    except Exception as e:
        print(f"Erro ao exibir resumo dos arquivos de conhecimento: {e}") 

def deploy_api_structure(project_path=None):
    """
    Cria a estrutura de API completa para um projeto OrNexus executando o script
    install_api_structure.sh na pasta do projeto
    
    Args:
        project_path: Caminho para o projeto (opcional, usa diretório atual se não fornecido)
    """
    import subprocess
    import os
    
    # Determinar o caminho do projeto
    if project_path:
        project_dir = Path(project_path)
    else:
        project_dir = Path.cwd()
    
    print(f"📁 Criando estrutura de API em: {project_dir}")
    
    # Verificar se é um projeto válido do OrNexus
    if not (project_dir / "knowledge").exists():
        print(f"❌ Erro: O diretório não parece ser um projeto OrNexus válido.")
        print("  Execute 'ornexus init <nome_projeto>' primeiro para criar um projeto.")
        return False
    
    # Localizar o script install_api_structure.sh no pacote
    package_dir = Path(__file__).parent.absolute()  # Caminho para a pasta ornexus
    script_path = package_dir / "deploy" / "install_api_structure.sh"
    
    if not script_path.exists():
        print(f"❌ Erro: Script de instalação não encontrado em {script_path}")
        return False
    
    # Garantir que o script tem permissões de execução
    script_path.chmod(0o755)
    
    # Mudar para o diretório do projeto antes de executar o script
    original_dir = os.getcwd()
    os.chdir(project_dir)
    
    try:
        print(f"⚙️ Executando script de instalação: {script_path}")
        result = subprocess.run(["bash", str(script_path)], check=True)
        
        if result.returncode == 0:
            print(f"✅ Estrutura de API criada com sucesso em {project_dir}")
            return True
        else:
            print(f"❌ Erro ao executar o script de instalação (código: {result.returncode})")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar o script: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False
    finally:
        # Voltar ao diretório original
        os.chdir(original_dir) 