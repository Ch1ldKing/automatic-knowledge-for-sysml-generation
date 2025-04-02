import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Neo4j Configuration
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

# MongoDB Configuration
MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DB = os.getenv("MONGODB_DB")
MONGODB_COLLECTION = "YOUR_COLLECTION_NAME"  # Replace with your collection name

# Milvus Configuration
MILVUS_HOST = os.getenv("MILVUS_HOST")
MILVUS_PORT = os.getenv("MILVUS_PORT")
MILVUS_COLLECTION = os.getenv("MILVUS_COLLECTION")
VECTOR_DIMENSION = 3072  # OpenAI text-embedding-3-large model dimension

# Default OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL")

# Provider-specific configurations for backward compatibility
OPENAI_API_KEY_GPT = os.getenv("OPENAI_API_KEY_GPT")
OPENAI_BASE_URL_GPT = os.getenv("OPENAI_BASE_URL_GPT")
OPENAI_MODEL_GPT = os.getenv("OPENAI_MODEL_GPT")

OPENAI_API_KEY_CLAUDE = os.getenv("OPENAI_API_KEY_CLAUDE")
OPENAI_BASE_URL_CLAUDE = os.getenv("OPENAI_BASE_URL_CLAUDE")
OPENAI_MODEL_CLAUDE = os.getenv("OPENAI_MODEL_CLAUDE")

OPENAI_API_KEY_DPSK = os.getenv("OPENAI_API_KEY_DPSK")
OPENAI_BASE_URL_DPSK = os.getenv("OPENAI_BASE_URL_DPSK")
OPENAI_MODEL_DPSK = os.getenv("OPENAI_MODEL_DPSK")

OPENAI_API_KEY_QWEN = os.getenv("OPENAI_API_KEY_QWEN")
OPENAI_BASE_URL_QWEN = os.getenv("OPENAI_BASE_URL_QWEN")
OPENAI_MODEL_QWEN = os.getenv("OPENAI_MODEL_QWEN")

# System Configuration
AUTO_EXPAND = os.getenv("AUTO_EXPAND", "False").lower() == "true"

# Paths
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data")
