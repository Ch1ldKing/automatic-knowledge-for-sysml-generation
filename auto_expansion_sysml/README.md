# Airplane SysML Self-Expanding Knowledge Base

An intelligent system for Model-Based Systems Engineering (MBSE) that uses SysML to model aircraft systems and subsystems. The knowledge base automatically expands as new systems are modeled.

## Features

- Hierarchical modeling of airplane systems and subsystems
- Automatic generation of specifications for new systems based on existing knowledge
- SysML model generation in JSON format
- Quality evaluation and improvement of generated models
- Automatic expansion of the knowledge base
- Integration with Neo4j for system relationships, MongoDB for model storage, and Milvus for vector embeddings

## Architecture

- **Neo4j**: Stores system relationships and hierarchical structure
- **MongoDB**: Stores specifications and SysML JSON models
- **Milvus**: Stores vector embeddings for semantic search
- **OpenAI API**: Provides LLM capabilities for model generation and improvement

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Configure environment variables:
   - Create a `.env` file in the root directory with your API keys and database connections
   - You can customize OpenAI API endpoint by setting `OPENAI_BASE_URL` (for custom endpoints or local services)

3. Initialize the database:
   ```
   python -m airplane_mbse.src.database.init_db
   ```

4. Start the API server:
   ```
   python -m airplane_mbse.src.api.main
   ```

## Usage

The system can be used in two modes:

1. **User-driven mode**: User inputs a system to model, and the system generates specifications and models
2. **Automatic mode**: System automatically expands the knowledge base by modeling subsystems

## License

MIT License 