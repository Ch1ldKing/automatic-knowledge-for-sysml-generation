from pymongo import MongoClient
from typing import Dict, Any, List, Optional
import logging
import json
from auto_expansion_sysml.config.config import (
    MONGODB_URI,
    MONGODB_DB,
    MONGODB_COLLECTION,
)

logger = logging.getLogger(__name__)


class MongoDBClient:
    def __init__(self, uri: str = MONGODB_URI, db_name: str = MONGODB_DB):
        """Initialize MongoDB client for storing all airplane system data."""
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.systems = self.db[MONGODB_COLLECTION]

        # Create indexes
        self.systems.create_index("system_id", unique=True)

    def close(self):
        """Close the MongoDB connection."""
        self.client.close()

    def save_system(
        self,
        system_id: str,
        system_name: str,
        requirement: Any = "",
        sysml: Any = "",
    ) -> None:
        """
        Save or update a system with all its data.

        Args:
            system_id: ID of the system
            system_name: Name of the system
            requirement: System requirements as text or dict
            sysml: SysML model as text or dict
        """
        # Convert dict to JSON string if needed
        if isinstance(requirement, dict):
            requirement = json.dumps(requirement, ensure_ascii=False)
        if isinstance(sysml, dict):
            sysml = json.dumps(sysml, ensure_ascii=False)

        # First check if system exists
        existing_system = self.systems.find_one({"system_id": system_id})

        if existing_system:
            # Update all fields
            update_data = {
                "system_name": system_name,
                "requirement": requirement,
                "sysml": sysml,
            }
            self.systems.update_one({"system_id": system_id}, {"$set": update_data})
        else:
            # Create new document
            system_doc = {
                "system_id": system_id,
                "system_name": system_name,
                "requirement": requirement,
                "sysml": sysml,
            }
            self.systems.insert_one(system_doc)

    def save_requirement(self, system_id: str, requirement: str) -> None:
        """
        Save or update a system requirement.

        Args:
            system_id: ID of the system
            requirement: System requirement as text
        """
        # Get the system to ensure we have the name
        system = self.get_system(system_id)
        if not system:
            logger.warning(f"System {system_id} not found when saving requirement")
            return

        system_name = system.get("system_name", "")
        sysml = system.get("sysml", "")

        self.save_system(system_id, system_name, requirement=requirement, sysml=sysml)

    def save_sysml(self, system_id: str, sysml: str) -> None:
        """
        Save or update a SysML model.

        Args:
            system_id: ID of the system
            sysml: SysML model as text (JSON string)
        """
        # Get the system to ensure we have the name
        system = self.get_system(system_id)
        if not system:
            logger.warning(f"System {system_id} not found when saving SysML model")
            return

        system_name = system.get("system_name", "")
        requirement = system.get("requirement", "")

        self.save_system(system_id, system_name, requirement=requirement, sysml=sysml)

    def get_system(self, system_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a complete system by system ID.

        Args:
            system_id: ID of the system

        Returns:
            System document or None if not found
        """
        return self.systems.find_one({"system_id": system_id}, {"_id": 0})

    def get_requirement(self, system_id: str) -> str:
        """
        Retrieve a system requirement by system ID.

        Args:
            system_id: ID of the system

        Returns:
            System requirement as text or empty string if not found
        """
        doc = self.systems.find_one({"system_id": system_id})
        if doc and "requirement" in doc:
            return doc["requirement"]
        return ""

    def get_sysml(self, system_id: str) -> str:
        """
        Retrieve a SysML model by system ID.

        Args:
            system_id: ID of the system

        Returns:
            SysML model as text (JSON string) or empty string if not found
        """
        doc = self.systems.find_one({"system_id": system_id})
        if doc and "sysml" in doc:
            return doc["sysml"]
        return ""

    def delete_system(self, system_id: str) -> None:
        """
        Delete a system completely.

        Args:
            system_id: ID of the system to delete
        """
        self.systems.delete_one({"system_id": system_id})

    def delete_requirement(self, system_id: str) -> None:
        """
        Delete only the requirement of a system.

        Args:
            system_id: ID of the system
        """
        self.systems.update_one({"system_id": system_id}, {"$set": {"requirement": ""}})

    def delete_sysml(self, system_id: str) -> None:
        """
        Delete only the SysML model of a system.

        Args:
            system_id: ID of the system
        """
        self.systems.update_one({"system_id": system_id}, {"$set": {"sysml": ""}})

    def system_exists(self, system_id: str) -> bool:
        """
        Check if a system exists with the given ID.

        Args:
            system_id: ID of the system to check

        Returns:
            True if the system exists, False otherwise
        """
        return self.systems.count_documents({"system_id": system_id}) > 0

    def requirement_exists(self, system_id: str) -> bool:
        """
        Check if a requirement exists for the given system ID.

        Args:
            system_id: ID of the system to check

        Returns:
            True if the requirement exists and is not empty, False otherwise
        """
        doc = self.systems.find_one(
            {"system_id": system_id, "requirement": {"$ne": ""}}
        )
        return doc is not None

    def sysml_exists(self, system_id: str) -> bool:
        """
        Check if a SysML model exists for the given system ID.

        Args:
            system_id: ID of the system to check

        Returns:
            True if the SysML model exists and is not empty, False otherwise
        """
        doc = self.systems.find_one({"system_id": system_id, "sysml": {"$ne": ""}})
        return doc is not None

    def get_all_systems(self) -> List[Dict[str, str]]:
        """
        Retrieve all systems.

        Returns:
            List of all system documents
        """
        return list(self.systems.find({}, {"_id": 0}))

    def migrate_old_data(self):
        """
        Migrate data from old collections (specifications and sysml_models)
        to the new unified collection.
        This method is for transition purposes only.
        """
        specs_collection = self.db["specifications"]
        models_collection = self.db["sysml_models"]

        # Get all specifications
        specs = list(specs_collection.find({}))
        for spec in specs:
            if "system_id" in spec and "specification" in spec:
                # Get the corresponding model if it exists
                model = models_collection.find_one({"system_id": spec["system_id"]})
                model_data = model.get("model", {}) if model else {}

                # Save to new unified collection
                self.save_system(
                    system_id=spec["system_id"],
                    system_name=model_data.get("name", "") if model_data else "",
                    requirement=spec["specification"],
                    sysml=json.dumps(model_data),
                )

        logger.info(
            f"Migrated {len(specs)} systems from old collections to new unified collection"
        )
