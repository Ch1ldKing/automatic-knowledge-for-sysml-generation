from pymilvus import (
    connections,
    Collection,
    CollectionSchema,
    FieldSchema,
    DataType,
    utility,
)
import numpy as np
from typing import List, Dict, Any, Optional
import logging
import json
from auto_expansion_sysml.config.config import (
    MILVUS_HOST,
    MILVUS_PORT,
    MILVUS_COLLECTION,
    VECTOR_DIMENSION,
)

logger = logging.getLogger(__name__)


class MilvusClient:
    def __init__(
        self,
        host: str = MILVUS_HOST,
        port: str = MILVUS_PORT,
        collection_name: str = MILVUS_COLLECTION,
    ):
        """Initialize Milvus client for specification vector embeddings."""
        self.host = host
        self.port = port
        self.collection_name = collection_name

        # Connect to Milvus
        connections.connect(host=self.host, port=self.port)

        # Create collection if it doesn't exist
        self._create_collection_if_not_exists()

        # Get collection
        self.collection = Collection(self.collection_name)
        self.collection.load()

    def _create_collection_if_not_exists(self):
        """Create the Milvus collection if it doesn't exist."""
        if utility.has_collection(self.collection_name):
            return

        # Define fields for the collection
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="system_id", dtype=DataType.VARCHAR, max_length=100),
            FieldSchema(
                name="embedding", dtype=DataType.FLOAT_VECTOR, dim=VECTOR_DIMENSION
            ),
        ]

        # Create schema and collection
        schema = CollectionSchema(
            fields=fields, description="Airplane system specifications"
        )
        collection = Collection(name=self.collection_name, schema=schema)

        # Create index for vector field
        index_params = {
            "metric_type": "COSINE",
            "index_type": "IVF_FLAT",
            "params": {"nlist": 128},
        }
        collection.create_index(field_name="embedding", index_params=index_params)
        logger.info(f"Created Milvus collection: {self.collection_name}")

    def close(self):
        """Release the collection and disconnect from Milvus."""
        self.collection.release()
        connections.disconnect(alias="default")

    def insert_specification(self, system_id: str, embedding: List[float]) -> None:
        """
        Insert a specification embedding into Milvus.

        Args:
            system_id: ID of the system
            embedding: Vector embedding of the specification
        """
        # TODO 这个是不是有点问题 First, check if this system_id already exists
        self.delete_specification(system_id)

        # Insert the new embedding
        data = [[system_id], [embedding]]  # system_id  # embedding

        self.collection.insert([data[0], data[1]])
        self.collection.flush()

    def search_similar_specifications(
        self, embedding: List[float], top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search for similar specifications based on embedding.

        Args:
            embedding: Vector embedding to search for
            top_k: Number of top results to return

        Returns:
            List of similar specifications with system_id and similarity score
        """
        search_params = {"metric_type": "COSINE", "params": {"nprobe": 10}}
        results = self.collection.search(
            data=[embedding],
            anns_field="embedding",
            param=search_params,
            limit=top_k,
            output_fields=["system_id"],
        )

        similar_specs = []
        for hits in results:
            for hit in hits:
                similar_specs.append(
                    {"system_id": hit.entity.get("system_id"), "similarity": hit.score}
                )

        return similar_specs

    def delete_specification(self, system_id: str) -> None:
        """
        Delete a specification embedding by system ID.

        Args:
            system_id: ID of the system to delete
        """
        expr = f'system_id == "{system_id}"'
        self.collection.delete(expr)

    def specification_exists(self, system_id: str) -> bool:
        """
        Check if a specification embedding exists for the given system ID.

        Args:
            system_id: ID of the system to check

        Returns:
            True if the embedding exists, False otherwise
        """
        expr = f'system_id == "{system_id}"'
        result = self.collection.query(expr=expr, output_fields=["system_id"])
        return len(result) > 0
