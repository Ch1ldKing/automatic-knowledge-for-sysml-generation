import logging
import json
from typing import Dict, Any, List, Optional, Tuple
import time
import re
import pdb
from auto_expansion_sysml.src.database.neo4j_client import Neo4jClient
from auto_expansion_sysml.src.database.mongodb_client import MongoDBClient
from auto_expansion_sysml.src.database.milvus_client import MilvusClient
from auto_expansion_sysml.src.models.llm_client_factory import get_client
from auto_expansion_sysml.config.config import GRANULARITY_THRESHOLD, AUTO_EXPAND

logger = logging.getLogger(__name__)


class ModelingService:
    def __init__(self, provider: str = "gpt"):
        """
        初始化建模服务，包含所有必需的客户端。

        参数:
            provider: LLM提供商 ('gpt', 'claude', 'dpsk', 或 'qwen')
        """
        self.neo4j_client = Neo4jClient()
        self.mongodb_client = MongoDBClient()
        # self.milvus_client = MilvusClient()
        self.openai_client = get_client(provider)
        self.provider = provider

    def close(self):
        """关闭所有数据库连接。"""
        self.neo4j_client.close()
        self.mongodb_client.close()
        # self.milvus_client.close()

    def generate_system_id(
        self, system_name: str, parent_id: Optional[str] = None
    ) -> str:
        """
        根据系统名称和可选的父ID生成唯一的系统ID。

        参数:
            system_name: 系统名称
            parent_id: 父系统的ID（可选），已经弃用，防止不兼容未删除

        返回:
            生成的系统ID
        """
        # 转换为小写并将空格替换为下划线
        base_id = system_name.lower().replace(" ", "_")
        # 移除任何特殊字符
        base_id = re.sub(r"[^a-z0-9_]", "", base_id)

        # 不再将父ID添加为前缀
        return base_id

    def model_system(
        self, system_name: str, auto_expand: bool = AUTO_EXPAND
    ) -> Dict[str, Any]:
        """
        使用MBSE方法对系统进行建模。

        参数:
            system_name: 要建模的系统名称
            auto_expand: 是否自动扩展子系统

        返回:
            包含状态和数据的建模结果
        """
        try:
            # 首先，检查这个系统在语义上是否存在
            all_systems = self.neo4j_client.get_all_systems()
            matching_system = self.openai_client.find_matching_system_name(
                system_name, all_systems
            )

            if matching_system:
                logger.info(
                    f"找到语义匹配的系统: {matching_system['name']} (ID: {matching_system['id']})"
                )
                system_id = matching_system["id"]
                # 使用数据库中的标准化名称
                system_name = matching_system["name"]

                # 检索现有数据
                specification = self.mongodb_client.get_requirement(system_id)
                model = self.mongodb_client.get_sysml(system_id)

                return {
                    "status": "success",
                    "message": f"系统在语义上匹配现有系统: {system_name}",
                    "system_id": system_id,
                    "specification": specification,
                    "model": model,
                    "is_new": False,
                }

            # 为新系统生成系统ID
            system_id = self.generate_system_id(system_name)

            # 通过ID检查系统是否已存在（备用方案）
            if self.neo4j_client.system_exists(system_id):
                logger.info(f"系统 {system_id} 已存在于数据库中")
                specification = self.mongodb_client.get_requirement(system_id)
                model = self.mongodb_client.get_sysml(system_id)

                return {
                    "status": "success",
                    "message": f"系统 {system_name} 已存在于数据库中",
                    "system_id": system_id,
                    "specification": specification,
                    "model": model,
                    "is_new": False,
                }

            # 在语义上查找最近的父系统
            # 首先从Neo4j获取父系统，利用OpenAI检查语义关系
            parent_system = self.neo4j_client.get_nearest_parent(system_name)

            # # 如果没查询到，就检查我们是否有潜在的父系统，使用LLM检查语义关系
            # if not parent_system and all_systems:
            #     # 过滤只包括潜在的父系统（避免过于具体的子系统）
            #     # TODO 不能有.就不要
            #     potential_parents = [s for s in all_systems if "." not in s["id"]]

            #     # 尝试在潜在的父系统中找到语义父系统
            #     for system in potential_parents:
            #         # 检查当前系统是否可能是这个潜在父系统的语义子系统
            #         prompt = f"""作为航空航天系统专家，确定'{system_name}'是否是'{system['name']}'的子系统或组件。
            #         只回答'true'或'false'。不要解释。"""

            #         response = self.openai_client.openai.chat.completions.create(
            #             model=self.openai_client.model,
            #             messages=[
            #                 {
            #                     "role": "system",
            #                     "content": "您是航空航天系统工程专家。只回答'true'或'false'。",
            #                 },
            #                 {"role": "user", "content": prompt},
            #             ],
            #         )

            #         result = response.choices[0].message.content.strip().lower()
            #         if result == "true":
            #             parent_system = system
            #             logger.info(f"找到语义父系统: {parent_system['name']}")
            #             break

            parent_id = parent_system["id"] if parent_system else None

            # 如果我们找到了父系统，更新系统ID以包含父前缀
            if parent_id:
                system_id = self.generate_system_id(system_name, parent_id)

            # 获取父系统的规格说明和模型
            parent_specification = None
            parent_model = None
            if parent_id:
                parent_specification = self.mongodb_client.get_requirement(parent_id)
                parent_model = self.mongodb_client.get_sysml(parent_id)

            # 为系统生成规格说明
            specification = self.openai_client.generate_specification(
                system_name, parent_specification
            )

            # 生成SysML模型
            model = self.openai_client.generate_sysml_model(
                system_name, specification, parent_model
            )

            # 评估模型
            evaluation = self.openai_client.evaluate_model(
                system_name, specification, model
            )

            # 如果评估分数低，改进模型
            if evaluation["overall_score"] < 7:
                model = self.openai_client.improve_model(
                    system_name, specification, model, evaluation
                )

            # 在Neo4j中保存系统
            self.neo4j_client.create_system(system_id, system_name)

            # 如果我们有父系统，创建关系
            if parent_id:
                self.neo4j_client.create_subsystem_relationship(parent_id, system_id)

            # 在MongoDB中保存规格说明和模型
            self.mongodb_client.save_system(
                system_id, system_name, specification, model
            )

            # 为规格说明创建嵌入
            # spec_text = json.dumps(specification)
            # embedding = self.openai_client.generate_embedding(spec_text)

            # 在Milvus中保存嵌入
            # TODO 这个地方会报错
            # self.milvus_client.insert_specification(system_id, embedding)

            # 从模型中提取子系统
            if auto_expand:
                self._process_subsystems(system_id, system_name, model)

            return {
                "status": "success",
                "message": f"成功建模系统 {system_name}",
                "system_id": system_id,
                "specification": specification,
                "model": model,
                "is_new": True,
            }

        except Exception as e:
            logger.error(f"建模系统 {system_name} 时出错: {str(e)}")
            return {
                "status": "error",
                "message": f"建模系统时出错: {str(e)}",
                "system_id": None,
                "specification": None,
                "model": None,
                "is_new": False,
            }

    def _process_subsystems(
        self, parent_id: str, parent_name: str, model: Dict[str, Any]
    ) -> None:
        """
        处理从SysML模型中提取的子系统。

        参数:
            parent_id: 父系统的ID
            parent_name: 父系统的名称
            model: 父系统的SysML模型
        """
        # 确保模型是字典类型而非字符串
        if isinstance(model, str):
            try:
                model = json.loads(model)
                logger.info(f"成功将系统 {parent_id} 的模型从字符串解析为字典")
            except json.JSONDecodeError as e:
                logger.error(f"解析系统 {parent_id} 的模型字符串时出错: {str(e)}")
                return

        # 提取子系统
        subsystems = self.openai_client.extract_subsystems(model, parent_name)

        logger.info(f"从模型中提取了 {len(subsystems)} 个子系统")

        # 获取所有现有系统进行语义比较
        all_systems = self.neo4j_client.get_all_systems()

        # 对于每个子系统，检查它是否在语义上已经存在
        for subsystem_name in subsystems:
            # 跳过空名称
            if not subsystem_name or len(subsystem_name.strip()) == 0:
                continue

            # 检查子系统是否处于粒度级别
            if self.openai_client.check_granularity(
                subsystem_name, GRANULARITY_THRESHOLD
            ):
                logger.info(f"子系统 {subsystem_name} 处于粒度级别，不再进一步扩展")
                continue

            # 检查这个子系统是否在语义上匹配现有系统
            matching_system = self.openai_client.find_matching_system_name(
                subsystem_name, all_systems
            )

            if matching_system:
                # 如果我们找到了语义匹配，使用其ID并创建关系
                subsystem_id = matching_system["id"]
                subsystem_name = matching_system["name"]  # 使用标准化名称

                logger.info(
                    f"子系统 {subsystem_name} 在语义上匹配现有系统 {subsystem_id}"
                )

                # 如果尚不存在，则创建与父系统的关系
                if not self.neo4j_client.system_exists(subsystem_id):
                    self.neo4j_client.create_system(subsystem_id, subsystem_name)

                # 创建关系
                self.neo4j_client.create_subsystem_relationship(parent_id, subsystem_id)
                continue

            # 如果没有语义匹配，生成新ID
            subsystem_id = self.generate_system_id(subsystem_name, parent_id)

            # 通过ID检查子系统是否已存在
            if self.neo4j_client.system_exists(subsystem_id):
                logger.info(f"子系统 {subsystem_id} 已存在于数据库中")

                # 如果关系不存在，则创建关系
                self.neo4j_client.create_subsystem_relationship(parent_id, subsystem_id)
                continue

            # 在Neo4j中创建子系统
            self.neo4j_client.create_system(subsystem_id, subsystem_name)

            # 创建与父系统的关系
            self.neo4j_client.create_subsystem_relationship(parent_id, subsystem_id)

            logger.info(f"创建了新子系统: {subsystem_name} (ID: {subsystem_id})")

        # 如果全局启用了自动扩展，这些子系统将来会被建模

    def auto_expand_system(self, system_id: str, depth: int = 1) -> Dict[str, Any]:
        """
        通过建模其子系统自动扩展系统。

        参数:
            system_id: 要扩展的系统ID
            depth: 扩展深度（要深入的层级数）

        返回:
            扩展结果
        """
        try:
            # 获取系统
            system = self.neo4j_client.get_system_by_id(system_id)
            if not system:
                return {
                    "status": "error",
                    "message": f"未找到系统 {system_id}",
                    "expanded_subsystems": [],
                }

            # 获取模型
            model = self.mongodb_client.get_sysml(system_id)
            if not model:
                return {
                    "status": "error",
                    "message": f"未找到系统 {system_id} 的模型",
                    "expanded_subsystems": [],
                }

            # 确保模型是字典类型而非字符串
            if isinstance(model, str):
                try:
                    model = json.loads(model)
                    logger.info("成功将模型从字符串解析为字典")
                except json.JSONDecodeError as e:
                    logger.error(f"解析模型字符串时出错: {str(e)}")
                    return {
                        "status": "error",
                        "message": f"解析系统 {system_id} 的模型时出错: {str(e)}",
                        "expanded_subsystems": [],
                    }

            # 提取子系统
            subsystems = self.openai_client.extract_subsystems(model)

            logger.info(f"找到 {len(subsystems)} 个可能扩展的子系统")

            # 获取所有现有系统进行语义比较
            all_systems = self.neo4j_client.get_all_systems()
            expanded_subsystems = []

            # 建模每个子系统
            for subsystem_name in subsystems:
                # 跳过空名称
                if not subsystem_name or len(subsystem_name.strip()) == 0:
                    continue

                logger.info(f"处理自动扩展的子系统: {subsystem_name}")

                # 检查子系统是否处于粒度级别
                if self.openai_client.check_granularity(
                    subsystem_name, GRANULARITY_THRESHOLD
                ):
                    logger.info(f"子系统 {subsystem_name} 处于粒度级别，不再进一步扩展")
                    continue

                # 检查这个子系统是否在语义上匹配现有系统
                matching_system = self.openai_client.find_matching_system_name(
                    subsystem_name, all_systems
                )

                if matching_system:
                    # 如果我们找到了语义匹配，使用其ID并创建关系
                    existing_id = matching_system["id"]
                    standardized_name = matching_system["name"]

                    logger.info(
                        f"子系统 {subsystem_name} 在语义上匹配现有系统 {existing_id}"
                    )

                    # 如果尚不存在，则创建与父系统的关系
                    if not self.neo4j_client.system_exists(existing_id):
                        self.neo4j_client.create_system(existing_id, standardized_name)

                    # 创建关系
                    self.neo4j_client.create_subsystem_relationship(
                        system_id, existing_id
                    )

                    # 获取现有数据
                    specification = self.mongodb_client.get_requirement(existing_id)
                    model = self.mongodb_client.get_sysml(existing_id)

                    # 记录为已处理
                    expanded_subsystems.append(
                        {"name": standardized_name, "id": existing_id, "is_new": False}
                    )

                    # 如果深度 > 1，则递归扩展
                    if depth > 1:
                        logger.info(f"递归扩展子系统: {standardized_name}")
                        nested_result = self.auto_expand_system(existing_id, depth - 1)
                        # 注意：如果需要，我们可以在这里处理nested_result

                    continue

                # 使用完整的建模过程建模子系统
                result = self.model_system(subsystem_name)

                if result["status"] == "success":
                    expanded_subsystems.append(
                        {
                            "name": subsystem_name,
                            "id": result["system_id"],
                            "is_new": result["is_new"],
                        }
                    )

                    # 如果深度 > 1 且它是新系统，则递归扩展
                    if depth > 1 and result["is_new"]:
                        logger.info(f"递归扩展子系统: {subsystem_name}")
                        nested_result = self.auto_expand_system(
                            result["system_id"], depth - 1
                        )
                        # 注意：如果需要，我们可以在这里处理nested_result

                # 短暂休眠以避免API过载
                time.sleep(1)

            return {
                "status": "success",
                "message": f"成功扩展系统 {system_id}",
                "expanded_subsystems": expanded_subsystems,
            }

        except Exception as e:
            logger.error(f"扩展系统 {system_id} 时出错: {str(e)}")
            return {
                "status": "error",
                "message": f"扩展系统时出错: {str(e)}",
                "expanded_subsystems": [],
            }

    def global_auto_modeling(self, exclude_root: bool = True) -> Dict[str, Any]:
        """
        全局自动建模：遍历图数据库中的所有节点（除根节点外），
        解析它们的SysML模型并为所有子系统构建模型。
        仅在子系统粒度判断为小时停止对该子系统建模。

        参数:
            exclude_root: 是否排除根节点"airplane"，默认为True

        返回:
            包含处理结果的字典
        """
        try:
            # 保存已确认为小粒度的系统名称
            small_granularity_systems = set()
            all_modeled_subsystems = []

            # 对所有未处理的系统进行建模，直到没有新系统为止
            while True:
                # 获取所有系统
                all_systems = self.neo4j_client.get_all_systems()

                # 如果排除根节点，移除airplane系统
                if exclude_root:
                    all_systems = [s for s in all_systems if s["id"] != "airplane"]

                # 筛选出未处理的系统 - 未处理系统是指没有子系统的系统
                unprocessed_systems = []
                for system in all_systems:
                    if not self._has_subsystems(system["id"]):
                        unprocessed_systems.append(system)

                # 如果没有未处理的系统，结束循环
                if not unprocessed_systems:
                    logger.info("所有系统已处理完毕，全局建模完成")
                    break

                logger.info(
                    f"继续全局自动建模，本轮有 {len(unprocessed_systems)} 个系统需要处理"
                )

                # 本轮新建模的子系统数量
                new_subsystems_count = 0

                # 处理当前未处理的系统
                for system in unprocessed_systems:
                    system_id = system["id"]
                    system_name = system["name"]

                    # 获取系统模型
                    model = self.mongodb_client.get_sysml(system_id)
                    if not model:
                        logger.warning(f"系统 {system_id} 获取sysml失败")
                        # TODO 获取不到就是处理过吗？ 处理创建一个空的子系统关系，使其被标记为已处理
                        # self.neo4j_client.mark_system_as_processed(system_id)
                        continue

                    # 确保模型是字典类型而非字符串
                    if isinstance(model, str):
                        try:
                            model = json.loads(model)
                            logger.info(
                                f"成功将系统 {system_id} 的模型从字符串解析为字典"
                            )
                        except json.JSONDecodeError as e:
                            logger.error(
                                f"解析系统 {system_id} 的模型字符串时出错: {str(e)}"
                            )
                            # 创建一个空的子系统关系，使其被标记为已处理
                            # self.neo4j_client.mark_system_as_processed(system_id)
                            continue

                    # 提取子系统
                    subsystems = self.openai_client.extract_subsystems(
                        model, system_name
                    )
                    logger.info(
                        f"从系统 {system_id} 中提取了 {len(subsystems)} 个子系统"
                    )

                    # 跳过没有子系统的系统
                    if not subsystems:
                        logger.info(f"系统 {system_id} 提取子系统失败")
                        # TODO 解析错误就是已处理吗？ 创建一个空的子系统关系，使其被标记为已处理
                        # self.neo4j_client.mark_system_as_processed(system_id)
                        continue

                    # 处理每个子系统
                    system_subsystems = []
                    for subsystem_name in subsystems:
                        # 跳过空名称
                        if not subsystem_name or len(subsystem_name.strip()) == 0:
                            continue

                        # 如果子系统已被判断为小粒度，跳过
                        if subsystem_name in small_granularity_systems:
                            logger.info(
                                f"子系统 {subsystem_name} 已被确认为小粒度，跳过建模"
                            )
                            continue

                        # 检查子系统是否处于粒度级别
                        if self.openai_client.check_granularity(
                            subsystem_name, GRANULARITY_THRESHOLD
                        ):
                            logger.info(
                                f"子系统 {subsystem_name} 处于粒度级别，标记为小粒度并跳过"
                            )
                            small_granularity_systems.add(subsystem_name)
                            continue

                        # 为子系统建模
                        result = self.model_subsystem(
                            subsystem_name, system_id, system_name
                        )

                        if result["status"] == "success":
                            # 记录子系统信息
                            subsystem_info = {
                                "parent_id": system_id,
                                "parent_name": system_name,
                                "name": subsystem_name,
                                "id": result["system_id"],
                                "is_new": result["is_new"],
                            }
                            system_subsystems.append(subsystem_info)
                            new_subsystems_count += 1

                            # 短暂休眠以避免API过载
                            time.sleep(1)
                        elif result["status"] == "skipped":
                            # 记录被跳过的子系统（避免闭环）
                            logger.info(
                                f"跳过子系统 {subsystem_name}: {result['message']}"
                            )

                    # 添加到总结果
                    all_modeled_subsystems.extend(system_subsystems)

                    # 记录进度
                    processed_count = sum(
                        1 for s in all_systems if self._has_subsystems(s["id"])
                    )
                    logger.info(f"已处理 {processed_count}/{len(all_systems)} 个系统")

                    # 标记系统为已处理
                    self.neo4j_client.mark_system_as_processed(system_id)

                # 如果本轮没有新建模的子系统，结束循环
                if new_subsystems_count == 0:
                    logger.info("本轮没有新建模的子系统，全局建模完成")
                    break

                logger.info(
                    f"本轮共建模了 {new_subsystems_count} 个新子系统，继续下一轮处理"
                )

            # 统计已处理系统数量
            processed_systems = [
                s["id"] for s in all_systems if self._has_subsystems(s["id"])
            ]

            return {
                "status": "success",
                "message": f"全局自动建模完成，共处理了 {len(processed_systems)} 个系统，建模了 {len(all_modeled_subsystems)} 个子系统",
                "processed_systems": processed_systems,
                "small_granularity_systems": list(small_granularity_systems),
                "modeled_subsystems": all_modeled_subsystems,
            }

        except Exception as e:
            logger.error(f"全局自动建模过程中出错: {str(e)}")
            return {
                "status": "error",
                "message": f"全局自动建模失败: {str(e)}",
                "processed_systems": [],
                "modeled_subsystems": [],
            }

    def _has_subsystems(self, system_id: str) -> bool:
        """
        检查系统是否有子系统，用于判断系统是否已被处理过。

        参数:
            system_id: 要检查的系统ID

        返回:
            如果系统有子系统或被标记为已处理，返回True；否则返回False
        """
        return self.neo4j_client.is_system_processed(system_id)

    def model_subsystem(
        self, subsystem_name: str, parent_id: str, parent_name: str
    ) -> Dict[str, Any]:
        """
        为全局自动建模过程建模子系统，与model_system不同，此函数专门用于处理已知父系统关系的场景。

        参数:
            subsystem_name: 要建模的子系统名称
            parent_id: 父系统的ID
            parent_name: 父系统的名称

        返回:
            包含状态和数据的建模结果
        """
        try:
            # 获取所有系统进行语义匹配
            all_systems = self.neo4j_client.get_all_systems()
            matching_system = self.openai_client.find_matching_system_name(
                subsystem_name, all_systems
            )

            # 检查是否找到语义匹配的系统
            if matching_system:
                matching_id = matching_system["id"]
                standardized_name = matching_system["name"]

                logger.info(
                    f"子系统 {subsystem_name} 在语义上匹配现有系统: {standardized_name} (ID: {matching_id})"
                )

                # 重要：检查匹配系统是否就是父系统本身，避免创建自引用闭环
                if matching_id == parent_id:
                    logger.warning(
                        f"子系统 {subsystem_name} 在语义上匹配其自身的父系统 {parent_name}，跳过关系创建"
                    )
                    return {
                        "status": "skipped",
                        "message": f"子系统在语义上匹配其父系统，避免闭环",
                        "system_id": matching_id,
                        "is_new": False,
                    }

                # 检索匹配系统的现有数据
                specification = self.mongodb_client.get_requirement(matching_id)
                model = self.mongodb_client.get_sysml(matching_id)

                # 如果尚不存在于Neo4j中，则创建系统节点
                if not self.neo4j_client.system_exists(matching_id):
                    self.neo4j_client.create_system(matching_id, standardized_name)

                # 创建与父系统的关系
                self.neo4j_client.create_subsystem_relationship(parent_id, matching_id)

                return {
                    "status": "success",
                    "message": f"使用语义匹配的现有系统: {standardized_name}",
                    "system_id": matching_id,
                    "specification": specification,
                    "model": model,
                    "is_new": False,
                }

            # 为新子系统生成系统ID，使用父系统信息
            subsystem_id = self.generate_system_id(subsystem_name)

            # 检查系统是否已通过ID存在
            if self.neo4j_client.system_exists(subsystem_id):
                logger.info(f"子系统 {subsystem_id} 已存在于数据库中")
                specification = self.mongodb_client.get_requirement(subsystem_id)
                model = self.mongodb_client.get_sysml(subsystem_id)

                # 确保与父系统的关系存在
                self.neo4j_client.create_subsystem_relationship(parent_id, subsystem_id)

                return {
                    "status": "success",
                    "message": f"子系统 {subsystem_name} 已存在于数据库中",
                    "system_id": subsystem_id,
                    "specification": specification,
                    "model": model,
                    "is_new": False,
                }

            # 获取父系统的规格说明和模型，用于参考
            parent_specification = self.mongodb_client.get_requirement(parent_id)
            parent_model = self.mongodb_client.get_sysml(parent_id)

            # 为子系统生成规格说明
            specification = self.openai_client.generate_specification(
                subsystem_name, parent_specification
            )

            # 生成SysML模型
            model = self.openai_client.generate_sysml_model(
                subsystem_name, specification, parent_model
            )

            # 评估模型
            evaluation = self.openai_client.evaluate_model(
                subsystem_name, specification, model
            )

            # 如果评估分数低，改进模型
            if evaluation["overall_score"] < 7:
                model = self.openai_client.improve_model(
                    subsystem_name, specification, model, evaluation
                )

            # 在Neo4j中保存系统
            self.neo4j_client.create_system(subsystem_id, subsystem_name)

            # 创建与父系统的关系
            self.neo4j_client.create_subsystem_relationship(parent_id, subsystem_id)

            # 在MongoDB中保存规格说明和模型
            self.mongodb_client.save_system(
                subsystem_id, subsystem_name, specification, model
            )

            return {
                "status": "success",
                "message": f"成功建模子系统 {subsystem_name}",
                "system_id": subsystem_id,
                "specification": specification,
                "model": model,
                "is_new": True,
            }

        except Exception as e:
            logger.error(f"建模子系统 {subsystem_name} 时出错: {str(e)}")
            return {
                "status": "error",
                "message": f"建模子系统时出错: {str(e)}",
                "system_id": None,
                "specification": None,
                "model": None,
                "is_new": False,
            }

    def model_system_single(self, system_name: str) -> Dict[str, Any]:
        """
        对系统进行单次建模，即使语义上匹配已存在的系统也会生成新模型。
        生成的模型和规格说明不会存入数据库，并且不会处理子系统。

        参数:
            system_name: 要建模的系统名称

        返回:
            包含状态和数据的建模结果
        """
        try:
            # 首先，检查这个系统在语义上是否存在
            all_systems = self.neo4j_client.get_all_systems()
            matching_system = self.openai_client.find_matching_system_name(
                system_name, all_systems
            )

            # 生成系统ID (不会被存储，只是用于结果返回)
            system_id = self.generate_system_id(system_name)

            # 查找父系统和相关参考数据
            parent_system = None
            matching_specification = None
            matching_model = None
            parent_specification = None
            parent_model = None

            if matching_system:
                logger.info(
                    f"找到语义匹配的系统: {matching_system['name']} (ID: {matching_system['id']})"
                )
                # 使用匹配系统的数据作为参考，但仍然会生成新的模型
                matching_specification = self.mongodb_client.get_requirement(
                    matching_system["id"]
                )
                matching_model = self.mongodb_client.get_sysml(matching_system["id"])
                # 标准化系统名称
                system_name = matching_system["name"]
            else:
                # 没有语义匹配，查找最近的父系统
                parent_system = self.neo4j_client.get_nearest_parent(system_name)
                # parent_system = None
                if parent_system:
                    parent_id = parent_system["id"]
                    parent_specification = self.mongodb_client.get_requirement(
                        parent_id
                    )
                    parent_model = self.mongodb_client.get_sysml(parent_id)

            # 为系统生成规格说明，优先使用匹配系统的规格作为参考，其次是父系统的规格
            if matching_specification:
                # 使用匹配的规格作为参考，但仍然生成新的规格
                specification = (
                    self.openai_client.generate_specification_with_reference(
                        system_name, matching_specification
                    )
                )
            else:
                # 使用父系统规格作为参考或没有参考
                specification = self.openai_client.generate_specification(
                    system_name, parent_specification
                )

            # 生成SysML模型，优先使用匹配系统的模型作为参考，其次是父系统的模型
            if matching_model:
                # 使用匹配的模型作为参考，但仍然生成新的模型
                model = self.openai_client.generate_sysml_model_with_reference(
                    system_name, specification, matching_model
                )
            else:
                # 使用父系统模型作为参考或没有参考
                model = self.openai_client.generate_sysml_model(
                    system_name, specification, parent_model
                )

            # 评估模型
            evaluation = self.openai_client.evaluate_model(
                system_name, specification, model
            )

            # 如果评估分数低，改进模型
            if evaluation["overall_score"] < 7:
                model = self.openai_client.improve_model(
                    system_name, specification, model, evaluation
                )

            return {
                "status": "success",
                "message": f"成功单次建模系统 {system_name}",
                "system_id": system_id,
                "specification": specification,
                "model": model,
                "is_new": True,
                "is_stored": False,  # 表明该模型未存储到数据库
                "reference_system": matching_system["id"] if matching_system else None,
                "parent_system": parent_system["id"] if parent_system else None,
            }

        except Exception as e:
            logger.error(f"单次建模系统 {system_name} 时出错: {str(e)}")
            return {
                "status": "error",
                "message": f"单次建模系统时出错: {str(e)}",
                "system_id": None,
                "specification": None,
                "model": None,
                "is_new": False,
                "is_stored": False,
            }
