import os
import logging
from typing import Optional
from importlib import import_module

logger = logging.getLogger(__name__)

# Define available model providers
SUPPORTED_PROVIDERS = ["gpt", "claude", "dpsk", "qwen"]


def get_client(provider: str = "gpt", **kwargs):
    """
    Factory function to get the appropriate OpenAI client based on provider name.

    Args:
        provider: Provider name ('gpt', 'claude', 'dpsk', or 'qwen')
        **kwargs: Additional parameters to pass to the client's constructor

    Returns:
        An instance of OpenAIClient for the specified provider
    """
    if provider not in SUPPORTED_PROVIDERS:
        logger.warning(f"Unsupported provider: {provider}. Falling back to 'gpt'")
        provider = "gpt"

    # Get environment variables for the specified provider
    api_key = os.getenv(f"OPENAI_API_KEY_{provider.upper()}")
    base_url = os.getenv(f"OPENAI_BASE_URL_{provider.upper()}")
    model = os.getenv(f"OPENAI_MODEL_{provider.upper()}")
    embedding_model = os.getenv("OPENAI_EMBEDDING_MODEL")

    if not api_key:
        logger.warning(
            f"API key not found for provider {provider}. Check your .env file."
        )

    if not base_url:
        logger.warning(
            f"Base URL not found for provider {provider}. Check your .env file."
        )

    if not model:
        logger.warning(
            f"Model not found for provider {provider}. Check your .env file."
        )

    # Import the appropriate client module
    try:
        module_name = f"airplane_mbse.src.models.openai_client_{provider}"
        client_module = import_module(module_name)

        # Create and return the client instance
        return client_module.OpenAIClient(
            api_key=api_key,
            base_url=base_url,
            model=model,
            embedding_model=embedding_model,
        )

    except ImportError as e:
        logger.error(f"Failed to import client module for provider {provider}: {e}")
        logger.info("Falling back to the default GPT client")

        # Fallback to GPT client
        from auto_expansion_sysml.src.models.openai_client_gpt import OpenAIClient

        return OpenAIClient(
            api_key=os.getenv("OPENAI_API_KEY_GPT"),
            base_url=os.getenv("OPENAI_BASE_URL_GPT"),
            model=os.getenv("OPENAI_MODEL_GPT"),
            embedding_model=embedding_model,
            **kwargs,
        )


class BaseLLMClient:
    """LLM 客户端基类，定义了接口方法"""

    def __init__(self):
        pass

    def generate_text(self, prompt: str, system_message: str = None) -> str:
        """生成文本"""
        raise NotImplementedError

    def generate_sysml_model(self, system_name: str, specification: str) -> dict:
        """生成SysML模型"""
        raise NotImplementedError

    def generate_sysml_model_with_no_rag(self, system_name: str) -> dict:
        """不使用RAG直接生成SysML模型"""
        raise NotImplementedError

    def generate_sysml_model_with_rag(
        self, system_name: str, relevant_context: str
    ) -> dict:
        """使用RAG检索到的相关上下文生成SysML模型"""
        raise NotImplementedError
