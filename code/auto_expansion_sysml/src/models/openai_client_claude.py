import logging
import json
import os
import re
from typing import Dict, Any, List, Optional
import openai
from auto_expansion_sysml.config.config import (
    OPENAI_API_KEY,
    OPENAI_BASE_URL,
    OPENAI_MODEL,
    OPENAI_EMBEDDING_MODEL,
)
from auto_expansion_sysml.src.models.my_json_schema import sysml_json_schema, spec_json_schema

# 配置OpenAI
openai.api_key = OPENAI_API_KEY
if OPENAI_BASE_URL:
    openai.base_url = OPENAI_BASE_URL

# 配置工具模型参数，可以放到config.py中
UTIL_MODEL_NAME = "gpt-4o-mini-2024-07-18"
UTIL_MODEL_BASE_URL = "https://api.oaipro.com/v1"
UTIL_MODEL_API_KEY = os.getenv("UTIL_MODEL_API_KEY")

logger = logging.getLogger(__name__)


class OpenAIClient:
    def __init__(
        self,
        model: str = OPENAI_MODEL,
        embedding_model: str = OPENAI_EMBEDDING_MODEL,
        api_key: str = OPENAI_API_KEY,
        base_url: str = OPENAI_BASE_URL,
    ):
        """初始化OpenAI客户端，用于生成规格说明和模型。"""
        self.model = model
        self.embedding_model = embedding_model

        # 配置客户端特定的OpenAI设置，增加超时时间
        self.openai = openai.OpenAI(
            api_key=api_key, base_url=base_url, timeout=60.0  # 增加超时时间到60秒
        )

        # 配置用于工具函数的OpenAI客户端
        self.util_openai = openai.OpenAI(
            api_key=UTIL_MODEL_API_KEY,
            base_url=UTIL_MODEL_BASE_URL,
            timeout=60.0,
        )

    def _extract_json_from_response(self, response_text: str) -> str:
        """
        从OpenAI响应中提取JSON内容，处理各种格式如代码块。

        参数:
            response_text: 包含JSON内容的响应文本

        返回:
            清理后的JSON字符串
        """
        # 尝试捕获Markdown代码块中的JSON
        code_block_pattern = r"```(?:json)?\s*([\s\S]*?)\s*```"
        code_block_match = re.search(code_block_pattern, response_text)

        if code_block_match:
            # 代码块中找到内容
            return code_block_match.group(1).strip()

        # 寻找可能的JSON对象 (大括号包围的内容)
        json_pattern = r"\{[\s\S]*\}"
        json_match = re.search(json_pattern, response_text)

        if json_match:
            return json_match.group(0).strip()

        # 如果没有找到明显的JSON模式，返回原始内容
        return response_text.strip()

    def _parse_json_response(self, response_text: str) -> Dict[str, Any]:
        """
        从OpenAI响应中提取和解析JSON内容。

        参数:
            response_text: 包含JSON内容的响应文本

        返回:
            解析后的JSON对象
        """
        try:
            # 首先尝试直接解析
            return json.loads(response_text)
        except json.JSONDecodeError:
            # 如果直接解析失败，尝试提取JSON内容
            extracted_json = self._extract_json_from_response(response_text)
            try:
                return json.loads(extracted_json)
            except json.JSONDecodeError as e:
                logger.error(f"JSON解析失败: {str(e)}")
                logger.error(f"原始文本: {response_text}")
                logger.error(f"提取后文本: {extracted_json}")
                # 如果仍然失败，返回一个空字典
                return {}

    def _collect_streaming_response(self, response) -> str:
        """
        从流式响应中收集完整的内容。

        参数:
            response: OpenAI流式响应对象

        返回:
            收集到的完整响应内容
        """
        collected_content = ""
        for chunk in response:
            # 检查chunk.choices是否为空
            if not chunk.choices:
                continue

            delta = chunk.choices[0].delta
            # 如果delta有content属性并且不为None
            if hasattr(delta, "content") and delta.content is not None:
                collected_content += delta.content

        return collected_content

    def _collect_streaming_response_with_display(self, response, display=False) -> str:
        """
        从流式响应中收集完整的内容，并可选择显示流式输出过程。

        参数:
            response: OpenAI流式响应对象
            display: 是否显示流式输出过程

        返回:
            收集到的完整响应内容
        """
        collected_content = ""
        reasoning_content = ""
        is_answering = False

        for chunk in response:
            # 如果chunk.choices为空，可能是usage信息
            if not chunk.choices:
                if display and hasattr(chunk, "usage"):
                    print("\nUsage:")
                    print(chunk.usage)
                continue

            delta = chunk.choices[0].delta

            # 处理思考过程（如果有）
            if (
                hasattr(delta, "reasoning_content")
                and delta.reasoning_content is not None
            ):
                reasoning_content += delta.reasoning_content
                if display:
                    print(delta.reasoning_content, end="", flush=True)
            elif hasattr(delta, "content") and delta.content is not None:
                # 开始回复标记（第一次收到内容时）
                if delta.content != "" and not is_answering and display:
                    print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
                    is_answering = True

                collected_content += delta.content

                # 显示回复过程
                if display:
                    print(delta.content, end="", flush=True)

        return collected_content

    def _get_utility_client(self):
        """获取用于工具函数的OpenAI客户端，使用gpt-4o-mini-2024-07-18模型"""
        return self.util_openai

    def generate_embedding(self, text: str) -> List[float]:
        """
        使用OpenAI嵌入模型为文本生成嵌入向量。

        参数:
            text: 要生成嵌入的文本

        返回:
            文本的向量嵌入
        """
        response = self.openai.embeddings.create(model=self.embedding_model, input=text)
        return response.data[0].embedding

    def generate_specification(
        self,
        system_name: str,
        parent_specification: Optional[Dict[str, Any]] = None,
        display_stream: bool = False,
    ) -> Dict[str, Any]:
        """
        根据系统名称和可选的父系统规格说明生成系统规格说明。

        参数:
            system_name: 要生成规格说明的系统名称
            parent_specification: 父系统的规格说明（可选）
            display_stream: 是否在控制台显示流式响应过程

        返回:
            系统的生成规格说明
        """
        # 创建提示

        if parent_specification:
            prompt = f"""Give specification of the system {system_name}. Output in JSON.
The Specification of parentSystem is {json.dumps(parent_specification, indent=2)}
Your task is to create a comprehensive system design document for {system_name}, including the design scenario, system components, relationships between components, and system attributes.
Please provide the following:
1. designScenario: Including the name of {system_name}, a detailed description, and a list of requirements
2. systemComponents: All major components that constitute {system_name} and their subComponents
3. relationships: The association, aggregation, dependency, or composition relationships between components
4. attributes: Key attributes and parameters describing {system_name} and its components

Use airplane engineering terminology in your descriptions. Ensure requirements are categorized as functional, performance, safety, or nonFunctional, and provide detailed descriptions for each requirement.

Component descriptions should include their type, functionality, and relationships with other components. System attributes should include name, type, value, and description. All relationships must clearly specify source and target components."""
        else:
            prompt = f"""Give specification of the system {system_name}. Output in JSON.

Your task is to create a comprehensive system design document for {system_name}, including the design scenario, system components, relationships between components, and system attributes.
Please provide the following:
1. designScenario: Including the name of {system_name}, a detailed description, and a list of requirements
2. systemComponents: All major components that constitute {system_name} and their subComponents
3. relationships: The association, aggregation, dependency, or composition relationships between components
4. attributes: Key attributes and parameters describing {system_name} and its components

Use airplane engineering terminology in your descriptions. Ensure requirements are categorized as functional, performance, safety, or nonFunctional, and provide detailed descriptions for each requirement.

Component descriptions should include their type, functionality, and relationships with other components. System attributes should include name, type, value, and description. All relationships must clearly specify source and target components."""

        try:
            response = self.openai.chat.completions.create(
                model=self.model,
                # temperature=0,
                messages=[
                    # {
                    #     "role": "system",
                    #     "content": "You're expert in System Design and Requirements Engineering of Passenger Airplane. Give specification of the given system. Output in JSON。",
                    # },
                    {
                        "role": "user",
                        "content": prompt
                        + f"the output has to follow the json_schema{spec_json_schema},do not output anything else",
                    },
                ],
                stream=True,
                # response_format=spec_json_schema
            )

            # 使用增强版流式响应收集器（可选择显示过程）
            content = self._collect_streaming_response_with_display(
                response, display=display_stream
            )
            specification = self._parse_json_response(content)
            return specification

        except Exception as e:
            logger.error(f"生成规格说明时出错: {str(e)}")
            # 返回基本规格说明作为后备
            return {
                "description": f"{system_name}的基本描述",
                "requirements": [f"{system_name}的基本需求"],
                "parameters": {"basic_param": "basic_value"},
            }

    def generate_sysml_model(
        self,
        system_name: str,
        specification: Dict[str, Any],
        parent_model: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        为系统生成JSON格式的SysML模型。

        参数:
            system_name: 要生成模型的系统名称
            specification: 系统的规格说明
            parent_model: 父系统的SysML模型（可选）

        返回:
            JSON格式的生成SysML模型
        """
        # 创建提示
        if parent_model:
            prompt = f"""You need to analysis the Specification of sub system in airplane. Generate the Sysml model of the system {system_name}. Output in JSON.

The Specification of the system: {json.dumps(specification, indent=2)}

Your task is to generate a SysML model that is compatible with the parent system model for {system_name}.
The Sysml Model of parent system {json.dumps(parent_model, indent=2)}
The model should include:
1. A system block representing {system_name}
2. Subsystems that compose {system_name} (using compositions, aggregations, or associations)
3. Interface blocks and flow specifications for system interfaces
4. Ports (proxy ports, full ports, flow ports) for system interactions
5. Key attributes and operations of the system
6. Value types and enumerations for system properties
7. Constraint blocks for system constraints
8. Comments for additional documentation
In the model, it should be specific and technical. Use airplane engineering terminology and follow SysML conventions."""

        else:
            prompt = f"""You need to analysis the Specification of sub system in airplane. Generate the Sysml model of the system {system_name}. Output in JSON.

The Specification of the system: {json.dumps(specification, indent=2)}

The model should include:
1. A system block representing {system_name}
2. Subsystems that compose {system_name} (using compositions, aggregations, or associations)
3. Interface blocks and flow specifications for system interfaces
4. Ports (proxy ports, full ports, flow ports) for system interactions
5. Key attributes and operations of the system
6. Value types and enumerations for system properties
7. Constraint blocks for system constraints
8. Comments for additional documentation

In the model, it should be specific and technical. Use airplane engineering terminology and follow SysML conventions."""

        try:
            response = self.openai.chat.completions.create(
                model=self.model,
                # temperature=0,
                messages=[
                    # {
                    #     "role": "system",
                    #     "content": "You're expert in Model Based System Engineering and Requirements Engineering of Passenger Airplane. Please give the Sysml Model of the given specification. Output in JSON",
                    # },
                    {
                        "role": "user",
                        "content": prompt
                        + f"the output has to follow the json_schema{sysml_json_schema},do not output anything else",
                    },
                ],
                stream=True,
                # response_format=sysml_json_schema,
            )

            # 收集流式响应内容
            content = self._collect_streaming_response(response)
            model = self._parse_json_response(content)

            return model

        except Exception as e:
            logger.error(f"生成SysML模型时出错: {str(e)}")
            # 返回基本模型作为后备
            return {
                "id": f"{system_name.lower().replace(' ', '_')}",
                "name": system_name,
                "type": "SysMLModel",
                "elements": [],
                "relationships": [],
            }

    def evaluate_model(
        self, system_name: str, specification: Dict[str, Any], model: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        根据规格说明评估SysML模型。

        参数:
            system_name: 系统名称
            specification: 系统的规格说明
            model: 要评估的SysML模型

        返回:
            评估结果
        """
        prompt = f"""Evaluate the quality of the SysML model for airplane {system_name}.

System has the following specification: {json.dumps(specification, indent=2)}

The SysML model is: {json.dumps(model, indent=2)}

Your task is to evaluate how well the SysML model meets the specification. Consider:
1. Completeness: Does the model cover all aspects of the specification?
2. Correctness: Are model elements correctly defined?
3. Consistency: Is the model internally consistent?
4. Clarity: Is the model clear and understandable?

Format the response as a JSON object with the following structure:
{{
  "overall_score": 0-10,
  "completeness_score": 0-10,
  "correctness_score": 0-10,
  "consistency_score": 0-10,
  "clarity_score": 0-10,
  "strengths": ["strength1", "strength2", ...],
  "weaknesses": ["weakness1", "weakness2", ...],
  "improvement_suggestions": ["suggestion1", "suggestion2", ...]
}}
DO NOT Output anything else, just the JSON object.
"""

        try:
            response = self.openai.chat.completions.create(
                model=self.model,
                # temperature=0.2,
                messages=[
                    # {
                    #     "role": "system",
                    #     "content": "You're expert in System Design and Requirements Engineering of Passenger Airplane.",
                    # },
                    {"role": "user", "content": prompt},
                ],
                stream=True,
                # response_format={"type": "json_object"},
            )

            # 收集流式响应内容
            content = self._collect_streaming_response(response)
            evaluation = self._parse_json_response(content)
            return evaluation

        except Exception as e:
            logger.error(f"评估模型时出错: {str(e)}")
            # 返回基本评估作为后备
            return {
                "overall_score": 5,
                "completeness_score": 5,
                "correctness_score": 5,
                "consistency_score": 5,
                "clarity_score": 5,
                "strengths": ["基本评估"],
                "weaknesses": ["评估失败"],
                "improvement_suggestions": ["尝试使用更详细的模型再次尝试"],
            }

    def improve_model(
        self,
        system_name: str,
        specification: Dict[str, Any],
        model: Dict[str, Any],
        evaluation: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        根据评估改进SysML模型。

        参数:
            system_name: 系统名称
            specification: 系统的规格说明
            model: 原始SysML模型
            evaluation: 评估结果

        返回:
            改进的SysML模型
        """
        prompt = f"""Improve the SysML model for subsystem "{system_name}" in airplane based on evaluation feedback.

System has the following specification: {json.dumps(specification, indent=2)}

Original SysML model is: {json.dumps(model, indent=2)}

Evaluation Feedback is: {json.dumps(evaluation, indent=2)}

Your task is to improve the SysML model by addressing weaknesses identified in the evaluation and implementing improvement suggestions.
Maintain the same JSON structure but enhance the content to better match the specification and address evaluation feedback.

Format the response as a complete improved SysML model with the same JSON structure as the original."""

        try:
            response = self.openai.chat.completions.create(
                model=self.model,
                messages=[
                    # {
                    #     "role": "system",
                    #     "content": "You're expert in System Design and Requirements Engineering of Passenger Airplane.",
                    # },
                    {
                        "role": "user",
                        "content": prompt
                        + f"the output has to follow the json_schema{sysml_json_schema},do not output anything else",
                    },
                ],
                stream=True,
                # response_format=sysml_json_schema,
            )

            # 收集流式响应内容
            content = self._collect_streaming_response(response)
            improved_model = self._parse_json_response(content)
            return improved_model

        except Exception as e:
            logger.error(f"改进模型时出错: {str(e)}")
            # 返回原始模型作为后备
            return model

    def extract_subsystems(
        self, model: Dict[str, Any], parent_system_name: str = None
    ) -> List[str]:
        """
        用 JSON解析 从SysML模型中提取子系统名称。

        参数:
            model: 要提取子系统的SysML模型
            parent_system_name: 父系统的名称，将被排除在结果之外

        返回:
            子系统名称列表
        """
        import re

        def process_name(name):
            """处理名称：在大写字母处分割，然后移除包含Package或Block的单词，用空格连接剩余单词"""
            # 在大写字母处添加空格进行分割
            # 使用正则表达式在大写字母前添加空格，但不处理首字母
            split_name = re.sub(r"(?<!^)(?=[A-Z])", " ", name).split()

            # 过滤掉包含"package"或"block"的单词（不区分大小写）
            filtered_words = []
            for word in split_name:
                if "package" not in word.lower() and "block" not in word.lower():
                    filtered_words.append(word)

            # 如果过滤后没有剩余单词，返回原始名称
            if not filtered_words:
                return name

            # 用空格重新连接单词
            return " ".join(filtered_words)

        subsystems = []

        # 首先检查model是否为字典
        if not isinstance(model, dict):
            logger.error(f"模型不是字典类型: {type(model)}")
            return subsystems

        # 检查elements是否为字典
        if "elements" not in model or not isinstance(model["elements"], dict):
            logger.error(
                f"模型中的elements不是字典类型: {type(model.get('elements', 'missing'))}"
            )
            return subsystems

        # 提取packages中的名称
        if "packages" in model["elements"] and isinstance(
            model["elements"]["packages"], list
        ):
            for package in model["elements"]["packages"]:
                if isinstance(package, dict) and "name" in package:
                    # 处理名称
                    cleaned_name = process_name(package["name"])

                    # 与parent_system_name比较并添加到子系统列表
                    if cleaned_name != parent_system_name:
                        subsystems.append(cleaned_name)

        # 提取blocks中的名称
        if "blocks" in model["elements"] and isinstance(
            model["elements"]["blocks"], list
        ):
            for block in model["elements"]["blocks"]:
                if isinstance(block, dict) and "name" in block:
                    # 处理名称
                    cleaned_name = process_name(block["name"])

                    # 与parent_system_name比较并添加到子系统列表
                    if cleaned_name != parent_system_name:
                        subsystems.append(cleaned_name)

        return subsystems

    def check_granularity(self, system_name: str, threshold_terms: List[str]) -> bool:
        """
        根据阈值术语检查系统是否达到了粒度级别。

        参数:
            system_name: 要检查的系统名称
            threshold_terms: 表示粒度级别的术语列表

        返回:
            如果系统已达到粒度级别则为True，否则为False
        """
        prompt = f"""
System name: {system_name}
Granularity threshold terms: {', '.join(threshold_terms)}

As an aerospace systems modeling expert, determine if the given system name has reached a sufficiently fine level of granularity.

Examples of components with sufficient granularity:
- Fuel pump
- Seat adjustment switch
- Landing light bulb
- Flight control computer processor
- Battery
- Cable
- Sensor

Examples of components with insufficient granularity:
- Engine system
- Hydraulic system
- Cabin system
- Electrical system
- Flight control system
- Navigation system

Has the system name "{system_name}" reached a sufficiently fine level of granularity like the examples? Consider the component's complexity and whether it can be meaningfully divided into multiple subcomponents. If the component is already a basic unit or cannot be meaningfully decomposed further, consider it as having reached sufficient granularity.
"""

        try:
            # 使用工具模型客户端
            response = self._get_utility_client().chat.completions.create(
                model=UTIL_MODEL_NAME,
                temperature=0.5,
                messages=[
                    {
                        "role": "system",
                        "content": "As an aerospace systems modeling expert, determine if the given system name has reached a sufficiently fine level of granularity. Output in JSON format: {'result': 'true' or 'false'}",
                    },
                    {"role": "user", "content": prompt},
                ],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "result_schema",
                        "strict": True,
                        "schema": {
                            "type": "object",
                            "properties": {"result": {"type": "boolean"}},
                            "additionalProperties": False,
                            "required": ["result"],
                        },
                    },
                },
            )

            result = json.loads(response.choices[0].message.content)
            return result["result"]

        except Exception as e:
            logger.error(f"检查系统粒度时出错: {str(e)}")
            # 如果API调用失败，回退到简单字符串匹配
            system_name_lower = system_name.lower()
            return any(term.lower() in system_name_lower for term in threshold_terms)

    def are_systems_semantically_same(
        self, system_name1: str, system_name2: str
    ) -> bool:
        """
        检查两个系统名称是否语义上相同。

        参数:
            system_name1: 第一个系统名称
            system_name2: 第二个系统名称

        返回:
            如果系统名称语义上相同则为True，否则为False
        """
        prompt = f"""
        System 1: {system_name1}
        System 2: {system_name2}
        """

        try:
            # 使用工具模型客户端
            response = self._get_utility_client().chat.completions.create(
                model=UTIL_MODEL_NAME,
                temperature=0.5,
                messages=[
                    {
                        "role": "system",
                        "content": "As an aerospace systems expert, determine if the following two system names refer to the same aircraft system SEMANTICALLY. Output in JSON. {{'result': 'true' or 'false'}}",
                    },
                    {
                        "role": "user",
                        "content": "System1: propulsion_system System2: engine control system",
                    },
                    {"role": "assistant", "content": "{{'result': 'false'}}"},
                    {"role": "user", "content": prompt},
                ],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "result_schema",
                        "strict": True,
                        "schema": {
                            "type": "object",
                            "properties": {"result": {"type": "boolean"}},
                            "additionalProperties": False,
                            "required": ["result"],
                        },
                    },
                },
            )

            result = json.loads(response.choices[0].message.content)
            return result["result"]

        except Exception as e:
            logger.error(f"比较系统名称时出错: {str(e)}")
            # 如果出错，保守地假设它们是不同的
            return False

    def find_matching_system_name(
        self, system_name: str, existing_systems: List[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """
        查找系统名称是否与任何现有系统在语义上匹配。

        参数:
            system_name: 要检查的系统名称
            existing_systems: 具有名称和ID的现有系统列表

        返回:
            如果找到匹配的系统则返回该系统，否则返回None
        """

        for system in existing_systems:
            if self.are_systems_semantically_same(system_name, system["name"]):
                return system
        return None

    def find_most_likely_parent_system(
        self,
        target_system_name: str,
        candidate_systems: List[Dict[str, Any]],
        current_level: Optional[Dict[str, Any]] = None,
    ) -> Optional[str]:
        """
        使用OpenAI确定给定系统最可能的父系统。把当前系统及其子系统都给模型判断，看看是和子系统同级还是某个子系统的子系统。

        参数:
            target_system_name: 目标系统名称
            candidate_systems: 候选父系统列表
            current_level: 当前层级系统（如果有）

        返回:
            最可能的父系统名称，如果无法确定则返回None
        """
        if not candidate_systems:
            return None

        # 准备系统数据
        systems_data = []
        for system in candidate_systems:
            systems_data.append(
                {
                    "name": system["name"],
                    "id": system["id"],
                    "type": system.get("type", "System"),
                }
            )

        # 创建OpenAI提示
        if current_level:
            prompt = f"""As an aerospace systems expert, determine which system is the most likely parent of '{target_system_name}'.
            
Current system level: {current_level["name"]}
Candidate systems (siblings or children of {current_level["name"]}):
{json.dumps(systems_data, indent=2)}

Analyze whether '{target_system_name}' is:
1. A direct subsystem of {current_level["name"]} (same level as the candidates)
2. A subsystem of one of the candidate systems
"""
        else:
            prompt = f"""As an aerospace systems expert, determine which top-level aircraft system is the most likely parent of '{target_system_name}'.
            
Top-level aircraft systems:
{json.dumps(systems_data, indent=2)}

Determine which of these systems would most likely contain '{target_system_name}' as a subsystem.
"""
        try:
            # 使用工具模型客户端
            response = self._get_utility_client().chat.completions.create(
                model=UTIL_MODEL_NAME,
                temperature=0.3,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an aerospace systems engineering expert. Respond only with the requested JSON format.",
                    },
                    {"role": "user", "content": prompt},
                ],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "parent_system_name_schema",
                        "strict": True,
                        "schema": {
                            "type": "object",
                            "properties": {"parent_system_name": {"type": "string"}},
                            "additionalProperties": False,
                            "required": ["parent_system_name"],
                        },
                    },
                },
            )

            result = json.loads(response.choices[0].message.content)
            return result["parent_system_name"]

        except Exception as e:
            logger.error(f"使用OpenAI查找父系统时出错: {str(e)}")
            # 如果OpenAI失败，返回第一个系统作为后备
            return candidate_systems[0]["name"] if candidate_systems else None

    def generate_specification_with_reference(
        self, system_name: str, reference_specification: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        根据系统名称和参考规格说明重新生成系统规格说明。
        即使系统语义匹配已存在的系统，也会生成新的规格说明，但会参考已有数据。

        参数:
            system_name: 要生成规格说明的系统名称
            reference_specification: 参考系统的规格说明

        返回:
            系统的生成规格说明
        """
        prompt = f"""You need to analysis the Specification of sub system in airplane. Generate a new specification for the system {system_name}. Output in JSON.

You are provided with a reference specification of a semantically similar system:
{json.dumps(reference_specification, indent=2)}

Your task is to create a comprehensive system design document for {system_name}, including the design scenario, system components, relationships between components, and system attributes.
Use the reference specification as inspiration, but create a new, original specification that might improve upon or differ from the reference in meaningful ways.

Please provide the following:
1. designScenario: Including the name of {system_name}, a detailed description, and a list of requirements
2. systemComponents: All major components that constitute {system_name} and their subComponents
3. relationships: The association, aggregation, dependency, or composition relationships between components
4. attributes: Key attributes and parameters describing {system_name} and its components

Use airplane engineering terminology in your descriptions. Ensure requirements are categorized as functional, performance, safety, or nonFunctional, and provide detailed descriptions for each requirement.
"""

        try:
            response = self.openai.chat.completions.create(
                model=self.model,
                messages=[
                    # {
                    #     "role": "system",
                    #     "content": "You're expert in System Design and Requirements Engineering of Passenger Airplane. Give specification of the given system. Output in JSON。",
                    # },
                    {
                        "role": "user",
                        "content": prompt
                        + f"the output has to follow the json_schema{spec_json_schema},do not output anything else",
                    },
                ],
                stream=True,
                # response_format=spec_json_schema
            )

            # 收集流式响应内容
            content = self._collect_streaming_response(response)
            specification = self._parse_json_response(content)
            return specification

        except Exception as e:
            logger.error(f"使用参考生成规格说明时出错: {str(e)}")
            # 返回基本规格说明作为后备
            return {
                "description": f"{system_name}的基本描述",
                "requirements": [f"{system_name}的基本需求"],
                "parameters": {"basic_param": "basic_value"},
            }

    def generate_sysml_model_with_reference(
        self,
        system_name: str,
        specification: Dict[str, Any],
        reference_model: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        为系统生成JSON格式的SysML模型，参考但不复制已有模型。

        参数:
            system_name: 要生成模型的系统名称
            specification: 系统的规格说明
            reference_model: 参考系统的SysML模型

        返回:
            JSON格式的生成SysML模型
        """
        prompt = f"""You need to analysis the Specification of subsystem in airplane. Generate a new SysML model for the system {system_name}. Output in JSON.

System specification: {json.dumps(specification, indent=2)}

You are provided with a reference SysML model of a semantically similar system:
{json.dumps(reference_model, indent=2)}

Your task is to generate a new, original SysML model for {system_name} that draws inspiration from the reference model but is not identical to it. The model should:
1. Follow the same JSON structure as the reference model
2. Include similar elements but adapted specifically for {system_name}
3. Reflect the requirements in the provided specification
4. Improve upon the reference model where appropriate

The model should include:
1. A system block representing {system_name}
2. Subsystems that compose {system_name} (using compositions, aggregations, or associations)
3. Interface blocks and flow specifications for system interfaces
4. Ports (proxy ports, full ports, flow ports) for system interactions
5. Key attributes and operations of the system
6. Value types and enumerations for system properties
7. Constraint blocks for system constraints
8. Comments for additional documentation

In the model, it should be specific and technical. Use airplane engineering terminology and follow SysML conventions."""

        try:
            response = self.openai.chat.completions.create(
                model=self.model,
                messages=[
                    # {
                    #     "role": "system",
                    #     "content": "You're expert in Model Based System Engineering and Requirements Engineering of Passenger Airplane. Please give the Sysml Model of the given specification. Output in JSON",
                    # },
                    {
                        "role": "user",
                        "content": prompt
                        + f"the output has to follow the json_schema{sysml_json_schema},do not output anything else",
                    },
                ],
                stream=True,
                # response_format=sysml_json_schema,
            )

            # 收集流式响应内容
            content = self._collect_streaming_response(response)
            model = self._parse_json_response(content)
            return model

        except Exception as e:
            logger.error(f"使用参考生成SysML模型时出错: {str(e)}")
            # 返回基本模型作为后备
            return {
                "id": f"{system_name.lower().replace(' ', '_')}",
                "name": system_name,
                "type": "SysMLModel",
                "elements": [],
                "relationships": [],
            }

    def generate_specification_with_no_rag(self, system_name: str) -> Dict[str, Any]:
        """
        生成系统规格说明，不使用任何数据库信息或RAG（检索增强生成）

        参数:
            system_name: 要生成规格说明的系统名称

        返回:
            系统的生成规格说明
        """
        prompt = f"""Generate a comprehensive specification document for an airplane subsystem: {system_name}. Output in JSON format.

Create a detailed system design document including:
1. designScenario: Name, comprehensive description, and categorized requirements
2. systemComponents: Major components and their subcomponents that make up {system_name}
3. relationships: All connections between components (association, aggregation, dependency, composition)
4. attributes: Key parameters and characteristics of {system_name} and its components

Requirements should be categorized as functional, performance, safety, or nonFunctional.
Use precise aerospace engineering terminology throughout.
Component descriptions must include type, functionality, and relationship details.
Attribute definitions must include name, type, value, and detailed description.
"""

        try:
            response = self.openai.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert aerospace systems engineer specializing in Model-Based Systems Engineering. You create detailed specifications for aircraft systems.",
                    },
                    {
                        "role": "user",
                        "content": prompt
                        + f"the output has to follow the json_schema{spec_json_schema},do not output anything else",
                    },
                ],
            )

            specification = self._parse_json_response(
                response.choices[0].message.content
            )
            return specification

        except Exception as e:
            logger.error(f"生成规格说明时出错: {str(e)}")
            # 返回基本规格说明作为后备
            return {
                "designScenario": {
                    "name": system_name,
                    "description": f"Basic description of {system_name}",
                    "requirements": [],
                },
                "systemComponents": [],
                "relationships": [],
                "attributes": [],
            }

    def generate_sysml_model_with_no_rag(self, system_name: str) -> Dict[str, Any]:
        """
        不使用RAG直接生成SysML模型。

        参数:
            system_name: 系统名称

        返回:
            生成的SysML模型
        """
        # 创建一个提示
        prompt = f"""Generate a SysML model for the {system_name} system.

Please create a comprehensive SysML model in JSON format that represents the {system_name} system. Your model should include:

1. Structural elements such as blocks, parts, and ports
2. Behavioral elements such as activities, actions, and states
3. Requirements and their relationships
4. Parametric constraints if applicable

Use standard SysML terminology and structure your model according to SysML best practices. Ensure the model is complete and represents all key aspects of {system_name}."""

        try:
            # 使用Claude进行生成
            response = self.openai.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert in SysML modeling for aerospace systems. Generate a complete SysML model in JSON format for the given system.",
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                response_format={"type": "json_object"},
            )

            content = response.choices[0].message.content
            model = self._parse_json_response(content)
            return model

        except Exception as e:
            logger.error(f"生成SysML模型时出错: {str(e)}")
            return {"error": str(e)}

    def generate_sysml_model_with_rag(
        self, system_name: str, relevant_context: str
    ) -> Dict[str, Any]:
        """
        使用RAG检索到的相关上下文生成SysML模型。

        参数:
            system_name: 系统名称
            relevant_context: 通过RAG检索获得的相关上下文信息

        返回:
            生成的SysML模型
        """
        # 创建包含RAG上下文的提示
        prompt = f"""Generate a SysML model for the {system_name} system using the following relevant context:

RELEVANT CONTEXT:
{relevant_context}

Please create a comprehensive SysML model in JSON format that represents the {system_name} system. Your model should include:

1. Structural elements such as blocks, parts, and ports
2. Behavioral elements such as activities, actions, and states
3. Requirements and their relationships
4. Parametric constraints if applicable

Use the provided context to inform your model design, especially for components, relationships, and requirements.
Use standard SysML terminology and structure your model according to SysML best practices. Ensure the model is complete and represents all key aspects of {system_name}.

The model should be technically precise, follow SysML conventions, and use proper aerospace engineering terminology.
Elements must have clear and consistent IDs, names, types, and relationships.
"""

        try:
            response = self.openai.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert in Model-Based Systems Engineering for aerospace systems, specializing in SysML modeling. Create a comprehensive model based on the provided context information.",
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                response_format={"type": "json_object"},
            )

            content = response.choices[0].message.content
            model = self._parse_json_response(content)
            return model

        except Exception as e:
            logger.error(f"使用RAG生成SysML模型时出错: {str(e)}")
            # 返回基本模型作为后备
            return {
                "id": f"{system_name.lower().replace(' ', '_')}",
                "name": system_name,
                "type": "SysMLModel",
                "elements": {
                    "blocks": [],
                    "interfaceBlocks": [],
                    "valueTypes": [],
                    "constraintBlocks": [],
                    "packages": [],
                },
                "relationships": [],
            }
