"""
LLMClient - 轻量级LLM API客户端库

作者: Leo <marticle.ios@gmail.com>
"""

from .config import LLMConfig
from .client import LLMClient

__version__ = "0.1.0"
__author__ = "Leo"
__email__ = "marticle.ios@gmail.com"

__all__ = ["LLMClient", "LLMConfig"]