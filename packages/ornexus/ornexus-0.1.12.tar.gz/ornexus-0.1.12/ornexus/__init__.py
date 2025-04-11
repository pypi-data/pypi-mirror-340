"""
OrNexus - Framework para criação de agentes com Agno
"""

try:
    import importlib.metadata
    __version__ = importlib.metadata.version("ornexus")
except ImportError:
    # Fallback para Python < 3.8
    try:
        import pkg_resources
        __version__ = pkg_resources.get_distribution("ornexus").version
    except Exception:
        __version__ = "0.1.3"  # Versão hardcoded como fallback 

from .utils import OrNexusConfig
from .main import OrNexus, main
from .utils.config_utils import OrNexusConfig

__all__ = ["OrNexus", "OrNexusConfig", "main"] 