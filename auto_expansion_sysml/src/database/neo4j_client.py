from neo4j import GraphDatabase
from typing import List, Dict, Any, Optional
import logging
from auto_expansion_sysml.config.config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
import json
from auto_expansion_sysml.src.models.llm_client_factory import get_client

logger = logging.getLogger(__name__)


class Neo4jClient:
    def __init__(
        self,
        uri: str = NEO4J_URI,
        user: str = NEO4J_USER,
        password: str = NEO4J_PASSWORD,
    ):
        """初始化飞机系统层次结构的Neo4j客户端。"""
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self._create_constraints()

    def _create_constraints(self):
        """为System节点创建约束以确保唯一性。"""
        with self.driver.session() as session:
            # 检查约束是否存在
            constraints = session.run("SHOW CONSTRAINTS").data()
            constraint_exists = any(
                c.get("name", "") == "unique_system_id" for c in constraints
            )

            if not constraint_exists:
                try:
                    session.run(
                        "CREATE CONSTRAINT unique_system_id FOR (s:System) REQUIRE s.id IS UNIQUE"
                    )
                    logger.info("为System节点创建了约束")
                except Exception as e:
                    logger.error(f"创建约束时出错: {str(e)}")

    def close(self):
        """关闭Neo4j连接。"""
        self.driver.close()

    def create_system(
        self, system_id: str, name: str, system_type: str = "System"
    ) -> None:
        """
        创建一个新的系统节点。

        参数:
            system_id: 系统的唯一标识符
            name: 系统的显示名称
            system_type: 系统的类型（默认为"System"）
        """
        with self.driver.session() as session:
            session.run(
                "MERGE (s:System {id: $id}) " "SET s.name = $name, s.type = $type",
                id=system_id,
                name=name,
                type=system_type,
            )

    def create_subsystem_relationship(self, parent_id: str, child_id: str) -> None:
        """
        创建父系统和子系统之间的HAS_SUBSYSTEM关系。

        参数:
            parent_id: 父系统的ID
            child_id: 子系统的ID
        """
        with self.driver.session() as session:
            session.run(
                "MATCH (parent:System {id: $parent_id}), (child:System {id: $child_id}) "
                "MERGE (parent)-[:HAS_SUBSYSTEM]->(child)",
                parent_id=parent_id,
                child_id=child_id,
            )

    def get_system_by_id(self, system_id: str) -> Optional[Dict[str, Any]]:
        """
        通过ID检索系统。

        参数:
            system_id: 要检索的系统ID

        返回:
            系统数据，如果未找到则返回None
        """
        with self.driver.session() as session:
            result = session.run("MATCH (s:System {id: $id}) RETURN s", id=system_id)
            record = result.single()
            if record:
                return dict(record["s"])
            return None

    def get_parent_system(self, system_id: str) -> Optional[Dict[str, Any]]:
        """
        查找给定系统的父系统。

        参数:
            system_id: 要查找父系统的系统ID

        返回:
            父系统数据，如果未找到则返回None
        """
        with self.driver.session() as session:
            result = session.run(
                "MATCH (parent:System)-[:HAS_SUBSYSTEM]->(child:System {id: $id}) "
                "RETURN parent",
                id=system_id,
            )
            record = result.single()
            if record:
                return dict(record["parent"])
            return None

    def get_nearest_parent(self, system_name: str) -> Optional[Dict[str, Any]]:
        """
        使用层次化方法为给定系统名称查找最近的父系统。

        该方法的工作原理是:
        1. 首先获取与"airplane"直接相连的所有顶级系统
        2. 使用OpenAI确定哪个顶级系统最有可能是父系统
        3. 如果找到可能的父系统，递归检查其子系统
        4. 当找到没有子系统的系统或确定了最合适的父系统时停止

        参数:
            system_name: 要查找父系统的系统名称

        返回:
            最合适的父系统数据，如果未找到则返回None
        """
        # 首先，检查"airplane"是否存在作为根系统
        airplane_system = self.get_system_by_id("airplane")
        if not airplane_system:
            # 如果没有airplane系统存在，我们无法继续层次化方法
            return None

        # 获取所有顶级系统（airplane的直接子系统）
        top_level_systems = self.get_all_subsystems("airplane")
        if not top_level_systems:
            return None

        # 在这里导入OpenAIClient以避免循环导入
        openai_client = get_client()

        # 从顶级系统开始
        current_level = None
        current_systems = top_level_systems

        while current_systems:
            # 使用OpenAI在此级别查找最可能的父系统
            most_likely_parent_name = openai_client.find_most_likely_parent_system(
                system_name, current_systems, current_level
            )

            if not most_likely_parent_name:
                # 如果没有找到可能的父系统，返回当前级别作为后备
                return current_level if current_level else None

            # 查找与名称匹配的系统对象
            most_likely_parent = next(
                (s for s in current_systems if s["name"] == most_likely_parent_name),
                None,
            )

            if not most_likely_parent:
                # 如果我们无法通过名称找到系统，尝试模糊匹配
                most_likely_parent = next(
                    (
                        s
                        for s in current_systems
                        if most_likely_parent_name.lower() in s["name"].lower()
                    ),
                    None,
                )

            if not most_likely_parent:
                # 如果仍然没有匹配，返回当前级别作为后备
                return current_level if current_level else None

            # 获取最可能父系统的子系统
            subsystems = self.get_all_subsystems(most_likely_parent["id"])

            # 如果没有子系统，我们找到了父系统
            if not subsystems:
                return most_likely_parent

            # 否则，继续向下层次结构
            current_level = most_likely_parent
            current_systems = subsystems

        # 如果我们在没有找到父系统的情况下退出循环，返回我们检查的最后一个级别
        return current_level

    def get_all_subsystems(self, system_id: str) -> List[Dict[str, Any]]:
        """
        获取给定系统的所有直接子系统。

        参数:
            system_id: 父系统的ID

        返回:
            子系统数据列表
        """
        with self.driver.session() as session:
            result = session.run(
                "MATCH (parent:System {id: $id})-[:HAS_SUBSYSTEM]->(sub:System) "
                "RETURN sub",
                id=system_id,
            )
            return [dict(record["sub"]) for record in result]

    def delete_system(self, system_id: str) -> None:
        """
        删除系统及其关系。

        参数:
            system_id: 要删除的系统ID
        """
        with self.driver.session() as session:
            session.run("MATCH (s:System {id: $id}) " "DETACH DELETE s", id=system_id)

    def system_exists(self, system_id: str) -> bool:
        """
        检查具有给定ID的系统是否存在。

        参数:
            system_id: 要检查的系统ID

        返回:
            如果系统存在则为True，否则为False
        """
        with self.driver.session() as session:
            result = session.run(
                "MATCH (s:System {id: $id}) RETURN count(s) as count", id=system_id
            )
            return result.single()["count"] > 0

    def get_all_systems(self) -> List[Dict[str, Any]]:
        """
        获取数据库中的所有系统。

        返回:
            所有系统数据的列表
        """
        # TODO 应该排除根节点
        with self.driver.session() as session:
            result = session.run("MATCH (s:System) RETURN s")
            return [dict(record["s"]) for record in result]

    def has_subsystems(self, system_id: str) -> bool:
        """
        检查系统是否有子系统，用于判断系统是否已处理过。

        参数:
            system_id: 要检查的系统ID

        返回:
            如果系统有子系统，返回True；否则返回False
        """
        with self.driver.session() as session:
            result = session.run(
                "MATCH (s:System {id: $id})-[:HAS_SUBSYSTEM]->() "
                "RETURN count(*) as count",
                id=system_id,
            )
            return result.single()["count"] > 0

    def mark_system_as_processed(self, system_id: str) -> None:
        """
        标记系统为已处理。

        参数:
            system_id: 要标记的系统ID
        """
        with self.driver.session() as session:
            # 创建一个到自身的PROCESSED关系来标记它已处理过
            session.run(
                "MATCH (s:System {id: $id}) " "MERGE (s)-[:PROCESSED]->(s)",
                id=system_id,
            )
            logger.info(f"系统 {system_id} 已被标记为已处理")

    def is_system_processed(self, system_id: str) -> bool:
        """
        检查系统是否已被标记为处理过。

        参数:
            system_id: 要检查的系统ID

        返回:
            如果系统已被处理，返回True；否则返回False
        """
        with self.driver.session() as session:
            # 检查系统是否有到自身的PROCESSED关系
            result = session.run(
                "MATCH (s:System {id: $id}) "
                "WHERE (s)-[:PROCESSED]->(s) "
                "RETURN count(*) as count",
                id=system_id,
            )
            return result.single()["count"] > 0

    def mark_system_as_atomic(self, system_id: str) -> None:
        """
        标记系统为原子组件（不可分解的基本组件）。

        参数:
            system_id: 要标记的系统ID
        """
        with self.driver.session() as session:
            # 创建一个到自身的ATOMICITY关系来标记它为原子组件
            session.run(
                "MATCH (s:System {id: $id}) " "MERGE (s)-[:ATOMICITY]->(s)",
                id=system_id,
            )
            logger.info(f"系统 {system_id} 已被标记为原子组件")

    def is_system_atomic(self, system_id: str) -> bool:
        """
        检查系统是否已被标记为原子组件。

        参数:
            system_id: 要检查的系统ID

        返回:
            如果系统是原子组件，返回True；否则返回False
        """
        with self.driver.session() as session:
            # 检查系统是否有到自身的ATOMICITY关系
            result = session.run(
                "MATCH (s:System {id: $id}) "
                "WHERE (s)-[:ATOMICITY]->(s) "
                "RETURN count(*) as count",
                id=system_id,
            )
            return result.single()["count"] > 0

    def mark_components_as_atomic(self, component_names: List[str]) -> None:
        """
        将给定名称列表中的所有组件标记为原子组件。

        参数:
            component_names: 要标记为原子组件的系统名称列表
        """
        with self.driver.session() as session:
            for name in component_names:
                # 先获取匹配该名称的系统
                result = session.run(
                    "MATCH (s:System) WHERE s.name = $name RETURN s.id as id", name=name
                )
                records = list(result)

                if records:
                    for record in records:
                        system_id = record["id"]
                        # 标记为原子组件
                        self.mark_system_as_atomic(system_id)
                        logger.info(f"将组件 '{name}' (ID: {system_id}) 标记为原子组件")
                else:
                    logger.warning(f"未找到名称为 '{name}' 的组件")

    def delete_all_nodes(self):
        """
        删除数据库中的所有节点及其关系。
        警告：此操作将清空整个数据库！
        """
        with self.driver.session() as session:
            # 首先删除所有关系，然后删除所有节点
            session.run("MATCH ()-[r]-() DELETE r")
            session.run("MATCH (n) DELETE n")
            logger.info("已删除所有节点和关系")
