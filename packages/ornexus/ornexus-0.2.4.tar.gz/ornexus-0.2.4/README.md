# OrNexus

Framework para criação rápida de projetos com agentes usando a biblioteca Agno.

## Instalação

```bash
pip install ornexus
```

Para instalar com suporte completo para o Agno:

```bash
pip install ornexus[agno]
```

## Uso Básico

```python
from ornexus import OrNexus

# Criar uma instância do OrNexus
ornexus = OrNexus()

# Executar o time de agentes
result = ornexus.team().run({
    "topico": "Impactos da política monetária dos bancos centrais em mercados emergentes",
    "tema": "Como as decisões do FED afetam economias emergentes em 2024",
    "extra_instruction": "Considere os impactos da política monetária recente dos bancos centrais."
})

print(result)
```

## Criando Seu Próprio Projeto

```bash
# Inicializar um novo projeto
ornexus init meu_projeto

# Navegar para o diretório do projeto
cd meu_projeto

# Executar o projeto
python -m meu_projeto
```

## Personalização

Você pode personalizar os agentes e tarefas editando os arquivos YAML na pasta `config`:

- `agents.yaml`: Define os papéis e metas dos agentes
- `tasks.yaml`: Define as instruções e saídas esperadas para cada tarefa

## Requisitos

- Python 3.8+
- Agno
- MongoDB (para armazenamento de conhecimento vetorial) 