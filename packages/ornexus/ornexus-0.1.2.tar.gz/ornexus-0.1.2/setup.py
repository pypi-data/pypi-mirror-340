from setuptools import setup, find_packages
import os

# Ler o README.md para usar como long_description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Configuração do pacote
setup(
    name="ornexus",
    version="0.1.2",
    author="OrNexus",
    author_email="contato@ornexus.com",
    description="Framework para criação de agentes com Agno",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/luandetoni/ornexus",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "ornexus": ["config/*.yaml"],
    },
    install_requires=[
        "agno",
        "pyyaml",
        "python-dotenv",
    ],
    extras_require={
        "agno": [
            "agno",
            "pymongo",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "ornexus=ornexus.cli:main",
        ],
    },
) 