sysml_json_schema = {
        "type": "json_schema",
        "json_schema": {
            "name": "SysML_Block_Definition_Diagram",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "diagramType": {
                        "type": "string",
                        "const": "BDD",
                        "description": "SysML 图的类型，固定为 BDD (块定义图)",
                    },
                    "elements": {
                        "type": "object",
                        "properties": {
                            "packages": {
                                "type": ["array", "null"],
                                "description": "包 (Package)",
                                "items": {"$ref": "#/$defs/Package"},
                            },
                            "blocks": {
                                "type": ["array", "null"],
                                "description": "块 (Block)",
                                "items": {"$ref": "#/$defs/Block"},
                            },
                            "interfaceBlocks": {
                                "type": ["array", "null"],
                                "description": "接口块 (Interface Block)",
                                "items": {"$ref": "#/$defs/InterfaceBlock"},
                            },
                            "flowSpecifications": {
                                "type": ["array", "null"],
                                "description": "流规范 (Flow Specification)",
                                "items": {"$ref": "#/$defs/FlowSpecification"},
                            },
                            "constraintBlocks": {
                                "type": ["array", "null"],
                                "description": "约束块 (Constraint Block)",
                                "items": {"$ref": "#/$defs/ConstraintBlock"},
                            },
                            "domains": {
                                "type": ["array", "null"],
                                "description": "域 (Domain)",
                                "items": {"$ref": "#/$defs/Domain"},
                            },
                            "valueTypes": {
                                "type": ["array", "null"],
                                "description": "值类型 (Value Type)",
                                "items": {"$ref": "#/$defs/ValueType"},
                            },
                            "enumerations": {
                                "type": ["array", "null"],
                                "description": "枚举 (Enumeration)",
                                "items": {"$ref": "#/$defs/Enumeration"},
                            },
                            "signals": {
                                "type": ["array", "null"],
                                "description": "信号 (Signal)",
                                "items": {"$ref": "#/$defs/Signal"},
                            },
                            "instances": {
                                "type": ["array", "null"],
                                "description": "实例 (Instance)",
                                "items": {"$ref": "#/$defs/Instance"},
                            },
                            "interfaces": {
                                "type": ["array", "null"],
                                "description": "接口 (Interface)",
                                "items": {"$ref": "#/$defs/Interface"},
                            },
                            "ports": {
                                "type": ["array", "null"],
                                "description": "端口 (Port)",
                                "items": {"$ref": "#/$defs/Port"},
                            },
                            "proxyPorts": {
                                "type": ["array", "null"],
                                "description": "代理端口 (Proxy Port)",
                                "items": {"$ref": "#/$defs/ProxyPort"},
                            },
                            "fullPorts": {
                                "type": ["array", "null"],
                                "description": "完整端口 (Full Port)",
                                "items": {"$ref": "#/$defs/FullPort"},
                            },
                            "flowPorts": {
                                "type": ["array", "null"],
                                "description": "流端口 (Flow Port)",
                                "items": {"$ref": "#/$defs/FlowPort"},
                            },
                            "interfaceRealizations": {
                                "type": ["array", "null"],
                                "description": "接口实现 (Interface Realization)",
                                "items": {"$ref": "#/$defs/InterfaceRealization"},
                            },
                            "links": {
                                "type": ["array", "null"],
                                "description": "连接 (Link)",
                                "items": {"$ref": "#/$defs/Link"},
                            },
                            "associationBlocks": {
                                "type": ["array", "null"],
                                "description": "关联块 (Association Block)",
                                "items": {"$ref": "#/$defs/AssociationBlock"},
                            },
                            "associationBlocksWithOwnedEnds": {
                                "type": ["array", "null"],
                                "description": "带拥有端的关联块 (Association Block with Owned Ends)",
                                "items": {
                                    "$ref": "#/$defs/AssociationBlockWithOwnedEnds"
                                },
                            },
                            "associations": {
                                "type": ["array", "null"],
                                "description": "关联 (Association)",
                                "items": {"$ref": "#/$defs/Association"},
                            },
                            "directedAssociations": {
                                "type": ["array", "null"],
                                "description": "有向关联 (Directed Association)",
                                "items": {"$ref": "#/$defs/DirectedAssociation"},
                            },
                            "aggregations": {
                                "type": ["array", "null"],
                                "description": "聚合 (Aggregation)",
                                "items": {"$ref": "#/$defs/Aggregation"},
                            },
                            "directedAggregations": {
                                "type": ["array", "null"],
                                "description": "有向聚合 (Directed Aggregation)",
                                "items": {"$ref": "#/$defs/DirectedAggregation"},
                            },
                            "compositions": {
                                "type": ["array", "null"],
                                "description": "组合 (Composition)",
                                "items": {"$ref": "#/$defs/Composition"},
                            },
                            "directedCompositions": {
                                "type": ["array", "null"],
                                "description": "有向组合 (Directed Composition)",
                                "items": {"$ref": "#/$defs/DirectedComposition"},
                            },
                            "generalizations": {
                                "type": ["array", "null"],
                                "description": "泛化 (Generalization)",
                                "items": {"$ref": "#/$defs/Generalization"},
                            },
                            "usages": {
                                "type": ["array", "null"],
                                "description": "使用 (Usage)",
                                "items": {"$ref": "#/$defs/Usage"},
                            },
                            "itemFlows": {
                                "type": ["array", "null"],
                                "description": "项流 (Item Flow)",
                                "items": {"$ref": "#/$defs/ItemFlow"},
                            },
                            "comments": {
                                "type": ["array", "null"],
                                "description": "注释 (Comment)",
                                "items": {"$ref": "#/$defs/Comment"},
                            },
                            "internalBlocks": {
                                "type": ["array", "null"],
                                "description": "内部块 (Internal Block) - 用于IBD",
                                "items": {"$ref": "#/$defs/InternalBlock"},
                            },
                            "requirements": {
                                "type": ["array", "null"],
                                "description": "需求 (Requirement) - 用于需求图",
                                "items": {"$ref": "#/$defs/Requirement"},
                            },
                            "actors": {
                                "type": ["array", "null"],
                                "description": "参与者 (Actor) - 用于用例图",
                                "items": {"$ref": "#/$defs/Actor"},
                            },
                            "useCases": {
                                "type": ["array", "null"],
                                "description": "用例 (UseCase) - 用于用例图",
                                "items": {"$ref": "#/$defs/UseCase"},
                            },
                            "activities": {
                                "type": ["array", "null"],
                                "description": "活动 (Activity) - 用于活动图",
                                "items": {"$ref": "#/$defs/Activity"},
                            },
                            "states": {
                                "type": ["array", "null"],
                                "description": "状态 (State) - 用于状态机图",
                                "items": {"$ref": "#/$defs/State"},
                            },
                            "lifelines": {
                                "type": ["array", "null"],
                                "description": "生命线 (Lifeline) - 用于序列图",
                                "items": {"$ref": "#/$defs/Lifeline"},
                            },
                            "messages": {
                                "type": ["array", "null"],
                                "description": "消息 (Message) - 用于序列图",
                                "items": {"$ref": "#/$defs/Message"},
                            },
                            "dependencies": {
                                "type": ["array", "null"],
                                "description": "依赖关系 (Dependency)",
                                "items": {"$ref": "#/$defs/Dependency"},
                            },
                            "realizations": {
                                "type": ["array", "null"],
                                "description": "实现关系 (Realization)",
                                "items": {"$ref": "#/$defs/Realization"},
                            },
                            "abstractions": {
                                "type": ["array", "null"],
                                "description": "抽象关系 (Abstraction)",
                                "items": {"$ref": "#/$defs/Abstraction"},
                            },
                            "includes": {
                                "type": ["array", "null"],
                                "description": "包含关系 (Include) - 用于用例图",
                                "items": {"$ref": "#/$defs/Include"},
                            },
                            "extends": {
                                "type": ["array", "null"],
                                "description": "扩展关系 (Extend) - 用于用例图",
                                "items": {"$ref": "#/$defs/Extend"},
                            },
                            "controlFlows": {
                                "type": ["array", "null"],
                                "description": "控制流 (ControlFlow) - 用于活动图",
                                "items": {"$ref": "#/$defs/ControlFlow"},
                            },
                            "objectFlows": {
                                "type": ["array", "null"],
                                "description": "对象流 (ObjectFlow) - 用于活动图",
                                "items": {"$ref": "#/$defs/ObjectFlow"},
                            },
                            "transitions": {
                                "type": ["array", "null"],
                                "description": "状态转换 (Transition) - 用于状态机图",
                                "items": {"$ref": "#/$defs/Transition"},
                            },
                            "parts": {
                                "type": ["array", "null"],
                                "description": "部件 (Part) - 用于IBD",
                                "items": {"$ref": "#/$defs/Part"},
                            },
                            "connectors": {
                                "type": ["array", "null"],
                                "description": "连接器 (Connector) - 用于IBD",
                                "items": {"$ref": "#/$defs/Connector"},
                            },
                            "constraints": {
                                "type": ["array", "null"],
                                "description": "约束 (Constraint)",
                                "items": {"$ref": "#/$defs/Constraint"},
                            },
                            "parameters": {
                                "type": ["array", "null"],
                                "description": "参数 (Parameter) - 用于参数图",
                                "items": {"$ref": "#/$defs/Parameter"},
                            },
                            "attributes": {
                                "type": ["array", "null"],
                                "description": "属性 (Attribute/Property)",
                                "items": {"$ref": "#/$defs/Attribute"},
                            },
                        },
                        "additionalProperties": False,
                        "required": [
                            "packages",
                            "blocks",
                            "interfaceBlocks",
                            "flowSpecifications",
                            "constraintBlocks",
                            "domains",
                            "valueTypes",
                            "enumerations",
                            "signals",
                            "instances",
                            "interfaces",
                            "ports",
                            "proxyPorts",
                            "fullPorts",
                            "flowPorts",
                            "interfaceRealizations",
                            "links",
                            "associationBlocks",
                            "associationBlocksWithOwnedEnds",
                            "associations",
                            "directedAssociations",
                            "aggregations",
                            "directedAggregations",
                            "compositions",
                            "directedCompositions",
                            "generalizations",
                            "usages",
                            "itemFlows",
                            "comments",
                            "internalBlocks",
                            "requirements",
                            "actors",
                            "useCases",
                            "activities",
                            "states",
                            "lifelines",
                            "messages",
                            "dependencies",
                            "realizations",
                            "abstractions",
                            "includes",
                            "extends",
                            "controlFlows",
                            "objectFlows",
                            "transitions",
                            "parts",
                            "connectors",
                            "constraints",
                            "parameters",
                            "attributes",
                        ],
                    },
                },
                "$defs": {
                    "Package": {
                        "type": "object",
                        "description": "包 (Package) 的定义",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "包的唯一标识符",
                            },
                            "type": {
                                "type": "string",
                                "const": "Package",
                                "description": "元素类型，固定为 Package",
                            },
                            "name": {
                                "type": "string",
                                "description": "包的名称",
                            },
                            "elementImports": {
                                "type": ["array", "null"],
                                "description": "包导入的元素 ID 列表",
                                "items": {"type": "string"},
                            },
                            "packageImports": {
                                "type": ["array", "null"],
                                "description": "导入的包的ID列表",
                                "items": {"type": "string"},
                            },
                        },
                        "additionalProperties": False,
                        "required": [
                            "id",
                            "type",
                            "name",
                            "elementImports",
                            "packageImports",
                        ],
                    },
                    "Block": {
                        "type": "object",
                        "description": "块 (Block) 的定义",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "块的唯一标识符",
                            },
                            "type": {
                                "type": "string",
                                "const": "Block",
                                "description": "元素类型，固定为 Block",
                            },
                            "name": {
                                "type": "string",
                                "description": "块的名称",
                            },
                            "isAbstract": {
                                "type": ["boolean", "null"],
                                "description": "是否为抽象块",
                            },
                            "isActive": {
                                "type": ["boolean", "null"],
                                "description": "是否为主动块",
                            },
                            "isEncapsulated": {
                                "type": ["boolean", "null"],
                                "description": "是否为封装块",
                            },
                            "attributeIds": {
                                "type": ["array", "null"],
                                "description": "块的属性 ID 列表",
                                "items": {"type": "string"},
                            },
                            "operationIds": {
                                "type": ["array", "null"],
                                "description": "块的操作 ID 列表",
                                "items": {"type": "string"},
                            },
                            "constraintIds": {
                                "type": ["array", "null"],
                                "description": "块的约束 ID 列表",
                                "items": {"type": "string"},
                            },
                            "partIds": {
                                "type": ["array", "null"],
                                "description": "块的部件 ID 列表",
                                "items": {"type": "string"},
                            },
                            "referenceIds": {
                                "type": ["array", "null"],
                                "description": "块的引用 ID 列表",
                                "items": {"type": "string"},
                            },
                            "valueIds": {
                                "type": ["array", "null"],
                                "description": "块的值属性 ID 列表",
                                "items": {"type": "string"},
                            },
                        },
                        "additionalProperties": False,
                        "required": [
                            "id",
                            "type",
                            "name",
                            "isAbstract",
                            "isActive",
                            "isEncapsulated",
                            "attributeIds",
                            "operationIds",
                            "constraintIds",
                            "partIds",
                            "referenceIds",
                            "valueIds",
                        ],
                    },
                    "InterfaceBlock": {
                        "type": "object",
                        "description": "接口块 (Interface Block) 的定义",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "接口块的唯一标识符",
                            },
                            "type": {
                                "type": "string",
                                "const": "InterfaceBlock",
                                "description": "元素类型，固定为 InterfaceBlock",
                            },
                            "name": {
                                "type": "string",
                                "description": "接口块的名称",
                            },
                            "attributeIds": {
                                "type": ["array", "null"],
                                "description": "接口块的属性 ID 列表",
                                "items": {"type": "string"},
                            },
                            "operationIds": {
                                "type": ["array", "null"],
                                "description": "接口块的操作 ID 列表",
                                "items": {"type": "string"},
                            },
                            "signalIds": {
                                "type": ["array", "null"],
                                "description": "接口块的信号 ID 列表",
                                "items": {"type": "string"},
                            },
                            "constraintIds": {
                                "type": ["array", "null"],
                                "description": "接口块的约束 ID 列表",
                                "items": {"type": "string"},
                            },
                        },
                        "additionalProperties": False,
                        "required": [
                            "id",
                            "type",
                            "name",
                            "attributeIds",
                            "operationIds",
                            "signalIds",
                            "constraintIds",
                        ],
                    },
                    "FlowSpecification": {
                        "type": "object",
                        "description": "流规范 (Flow Specification) 的定义",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "流规范的唯一标识符",
                            },
                            "type": {
                                "type": "string",
                                "const": "FlowSpecification",
                                "description": "元素类型，固定为 FlowSpecification",
                            },
                            "name": {
                                "type": "string",
                                "description": "流规范的名称",
                            },
                            "flowType": {
                                "type": ["string", "null"],
                                "description": "流动的类型 (例如：信息流, 物质流, 能量流)",
                            },
                            "dataType": {
                                "type": ["string", "null"],
                                "description": "数据类型 (如果适用)",
                            },
                            "unit": {
                                "type": ["string", "null"],
                                "description": "单位 (如果适用)",
                            },
                            "attributeIds": {
                                "type": ["array", "null"],
                                "description": "流规范的属性 ID 列表",
                                "items": {"type": "string"},
                            },
                        },
                        "additionalProperties": False,
                        "required": [
                            "id",
                            "type",
                            "name",
                            "flowType",
                            "dataType",
                            "unit",
                            "attributeIds",
                        ],
                    },
                    "ConstraintBlock": {
                        "type": "object",
                        "description": "约束块 (Constraint Block) 的定义",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "约束块的唯一标识符",
                            },
                            "type": {
                                "type": "string",
                                "const": "ConstraintBlock",
                                "description": "元素类型，固定为 ConstraintBlock",
                            },
                            "name": {
                                "type": "string",
                                "description": "约束块的名称",
                            },
                            "parameterIds": {
                                "type": ["array", "null"],
                                "description": "约束块的参数 ID 列表",
                                "items": {"type": "string"},
                            },
                            "expression": {
                                "type": "string",
                                "description": "约束表达式",
                            },
                            "attributeIds": {
                                "type": ["array", "null"],
                                "description": "约束块的属性 ID 列表",
                                "items": {"type": "string"},
                            },
                        },
                        "additionalProperties": False,
                        "required": [
                            "id",
                            "type",
                            "name",
                            "expression",
                            "parameterIds",
                            "attributeIds",
                        ],
                    },
                    "Domain": {
                        "type": "object",
                        "description": "域 (Domain) 的定义",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "域的唯一标识符",
                            },
                            "type": {
                                "type": "string",
                                "const": "Domain",
                                "description": "元素类型，固定为 Domain",
                            },
                            "name": {
                                "type": "string",
                                "description": "域的名称",
                            },
                            "attributeIds": {
                                "type": ["array", "null"],
                                "description": "域的属性 ID 列表",
                                "items": {"type": "string"},
                            },
                        },
                        "additionalProperties": False,
                        "required": ["id", "type", "name", "attributeIds"],
                    },
                    "ValueType": {
                        "type": "object",
                        "description": "值类型 (Value Type) 的定义",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "值类型的唯一标识符",
                            },
                            "type": {
                                "type": "string",
                                "const": "ValueType",
                                "description": "元素类型，固定为 ValueType",
                            },
                            "name": {
                                "type": "string",
                                "description": "值类型的名称",
                            },
                            "quantityKindId": {
                                "type": "string",
                                "description": "关联的 QuantityKind 的 ID",
                            },
                            "unitId": {
                                "type": "string",
                                "description": "关联的 Unit 的 ID",
                            },
                            "attributeIds": {
                                "type": "array",
                                "description": "值类型的属性 ID 列表",
                                "items": {"type": "string"},
                            },
                        },
                        "additionalProperties": False,
                        "required": [
                            "id",
                            "type",
                            "name",
                            "quantityKindId",
                            "unitId",
                            "attributeIds",
                        ],
                    },
                    "Enumeration": {
                        "type": "object",
                        "description": "枚举 (Enumeration) 的定义",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "枚举的唯一标识符",
                            },
                            "type": {
                                "type": "string",
                                "const": "Enumeration",
                                "description": "元素类型，固定为 Enumeration",
                            },
                            "name": {
                                "type": "string",
                                "description": "枚举的名称",
                            },
                            "literals": {
                                "type": "array",
                                "description": "枚举的字面值列表",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "id": {
                                            "type": "string",
                                            "description": "字面值的唯一标识符",
                                        },
                                        "name": {
                                            "type": "string",
                                            "description": "字面值的名称",
                                        },
                                    },
                                    "additionalProperties": False,
                                    "required": ["id", "name"],
                                },
                            },
                            "attributeIds": {
                                "type": ["array", "null"],
                                "description": "枚举的属性 ID 列表",
                                "items": {"type": "string"},
                            },
                        },
                        "additionalProperties": False,
                        "required": [
                            "id",
                            "type",
                            "name",
                            "literals",
                            "attributeIds",
                        ],
                    },
                    "Signal": {
                        "type": "object",
                        "description": "信号 (Signal) 的定义",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "信号的唯一标识符",
                            },
                            "type": {
                                "type": "string",
                                "const": "Signal",
                                "description": "元素类型，固定为 Signal",
                            },
                            "name": {
                                "type": "string",
                                "description": "信号的名称",
                            },
                            "parameterIds": {
                                "type": ["array", "null"],
                                "description": "信号的参数 ID 列表",
                                "items": {"type": "string"},
                            },
                            "attributeIds": {
                                "type": ["array", "null"],
                                "description": "信号的属性 ID 列表",
                                "items": {"type": "string"},
                            },
                        },
                        "additionalProperties": False,
                        "required": [
                            "id",
                            "type",
                            "name",
                            "parameterIds",
                            "attributeIds",
                        ],
                    },
                    "Instance": {
                        "type": "object",
                        "description": "实例 (Instance) 的定义",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "实例的唯一标识符",
                            },
                            "type": {
                                "type": "string",
                                "const": "Instance",
                                "description": "元素类型，固定为 Instance",
                            },
                            "name": {
                                "type": "string",
                                "description": "实例的名称",
                            },
                            "classifierId": {
                                "type": "string",
                                "description": "实例所属的分类器 (Block, InterfaceBlock 等) 的 ID",
                            },
                            "slotIds": {
                                "type": ["array", "null"],
                                "description": "实例的槽 (Slot) ID 列表，用于设置属性值",
                                "items": {"type": "string"},
                            },
                        },
                        "additionalProperties": False,
                        "required": [
                            "id",
                            "type",
                            "name",
                            "classifierId",
                            "slotIds",
                        ],
                    },
                    "Interface": {
                        "type": "object",
                        "description": "接口 (Interface) 的定义",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "接口的唯一标识符",
                            },
                            "type": {
                                "type": "string",
                                "const": "Interface",
                                "description": "元素类型，固定为 Interface",
                            },
                            "name": {
                                "type": "string",
                                "description": "接口的名称",
                            },
                            "operationIds": {
                                "type": ["array", "null"],
                                "description": "接口的操作 ID 列表",
                                "items": {"type": "string"},
                            },
                            "signalIds": {
                                "type": ["array", "null"],
                                "description": "接口的信号 ID 列表",
                                "items": {"type": "string"},
                            },
                            "attributeIds": {
                                "type": ["array", "null"],
                                "description": "接口的属性 ID 列表",
                                "items": {"type": "string"},
                            },
                        },
                        "additionalProperties": False,
                        "required": [
                            "id",
                            "type",
                            "name",
                            "operationIds",
                            "signalIds",
                            "attributeIds",
                        ],
                    },
                    "Port": {
                        "type": "object",
                        "description": "端口 (Port) 的定义",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "端口的唯一标识符",
                            },
                            "type": {
                                "type": "string",
                                "const": "Port",
                                "description": "元素类型，固定为 Port",
                            },
                            "name": {
                                "type": "string",
                                "description": "端口的名称",
                            },
                            "portType": {
                                "type": ["string", "null"],
                                "enum": ["proxy", "full", "flow"],
                                "description": "端口类型 (proxy, full, flow)",
                            },
                            "isConjugated": {
                                "type": ["boolean", "null"],
                                "description": "端口是否共轭",
                            },
                            "blockId": {
                                "type": "string",
                                "description": "端口所属的块的 ID",
                            },
                            "providedInterfaceIds": {
                                "type": ["array", "null"],
                                "description": "端口提供的接口 ID 列表",
                                "items": {"type": "string"},
                            },
                            "requiredInterfaceIds": {
                                "type": ["array", "null"],
                                "description": "端口需要的接口 ID 列表",
                                "items": {"type": "string"},
                            },
                            "flowSpecificationId": {
                                "type": ["string", "null"],
                                "description": "端口关联的流规范 ID (FlowPort)",
                            },
                            "attributeIds": {
                                "type": ["array", "null"],
                                "description": "端口的属性 ID 列表",
                                "items": {"type": "string"},
                            },
                        },
                        "additionalProperties": False,
                        "required": [
                            "id",
                            "type",
                            "name",
                            "blockId",
                            "portType",
                            "isConjugated",
                            "providedInterfaceIds",
                            "requiredInterfaceIds",
                            "flowSpecificationId",
                            "attributeIds",
                        ],
                    },
                    "ProxyPort": {
                        "type": "object",
                        "description": "代理端口 (Proxy Port) 的定义 -  Port 的子类型，为了区分类型",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "代理端口的唯一标识符",
                            },
                            "type": {
                                "type": "string",
                                "const": "ProxyPort",
                                "description": "元素类型，固定为 ProxyPort",
                            },
                            "name": {
                                "type": "string",
                                "description": "代理端口的名称",
                            },
                            "isConjugated": {
                                "type": ["boolean", "null"],
                                "description": "端口是否共轭",
                            },
                            "blockId": {
                                "type": "string",
                                "description": "端口所属的块的 ID",
                            },
                            "providedInterfaceIds": {
                                "type": ["array", "null"],
                                "description": "端口提供的接口 ID 列表",
                                "items": {"type": "string"},
                            },
                            "requiredInterfaceIds": {
                                "type": ["array", "null"],
                                "description": "端口需要的接口 ID 列表",
                                "items": {"type": "string"},
                            },
                            "attributeIds": {
                                "type": ["array", "null"],
                                "description": "代理端口的属性 ID 列表",
                                "items": {"type": "string"},
                            },
                        },
                        "additionalProperties": False,
                        "required": [
                            "id",
                            "type",
                            "name",
                            "blockId",
                            "isConjugated",
                            "providedInterfaceIds",
                            "requiredInterfaceIds",
                            "attributeIds",
                        ],
                    },
                    "FullPort": {
                        "type": "object",
                        "description": "完整端口 (Full Port) 的定义 - Port 的子类型，为了区分类型",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "完整端口的唯一标识符",
                            },
                            "type": {
                                "type": "string",
                                "const": "FullPort",
                                "description": "元素类型，固定为 FullPort",
                            },
                            "name": {
                                "type": "string",
                                "description": "完整端口的名称",
                            },
                            "isConjugated": {
                                "type": ["boolean", "null"],
                                "description": "端口是否共轭",
                            },
                            "blockId": {
                                "type": "string",
                                "description": "端口所属的块的 ID",
                            },
                            "providedInterfaceIds": {
                                "type": ["array", "null"],
                                "description": "端口提供的接口 ID 列表",
                                "items": {"type": "string"},
                            },
                            "requiredInterfaceIds": {
                                "type": ["array", "null"],
                                "description": "端口需要的接口 ID 列表",
                                "items": {"type": "string"},
                            },
                            "attributeIds": {
                                "type": ["array", "null"],
                                "description": "完整端口的属性 ID 列表",
                                "items": {"type": "string"},
                            },
                        },
                        "additionalProperties": False,
                        "required": [
                            "id",
                            "type",
                            "name",
                            "blockId",
                            "isConjugated",
                            "providedInterfaceIds",
                            "requiredInterfaceIds",
                            "attributeIds",
                        ],
                    },
                    "FlowPort": {
                        "type": "object",
                        "description": "流端口 (Flow Port) 的定义 - Port 的子类型，为了区分类型",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "流端口的唯一标识符",
                            },
                            "type": {
                                "type": "string",
                                "const": "FlowPort",
                                "description": "元素类型，固定为 FlowPort",
                            },
                            "name": {
                                "type": "string",
                                "description": "流端口的名称",
                            },
                            "isConjugated": {
                                "type": ["boolean", "null"],
                                "description": "端口是否共轭",
                            },
                            "blockId": {
                                "type": "string",
                                "description": "端口所属的块的 ID",
                            },
                            "flowSpecificationId": {
                                "type": "string",
                                "description": "端口关联的流规范 ID",
                            },
                            "attributeIds": {
                                "type": ["array", "null"],
                                "description": "流端口的属性 ID 列表",
                                "items": {"type": "string"},
                            },
                        },
                        "additionalProperties": False,
                        "required": [
                            "id",
                            "type",
                            "name",
                            "blockId",
                            "isConjugated",
                            "flowSpecificationId",
                            "attributeIds",
                        ],
                    },
                    "InterfaceRealization": {
                        "type": "object",
                        "description": "接口实现 (Interface Realization) 的定义",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "接口实现的唯一标识符",
                            },
                            "type": {
                                "type": "string",
                                "const": "InterfaceRealization",
                                "description": "元素类型，固定为 InterfaceRealization",
                            },
                            "name": {
                                "type": "string",
                                "description": "接口实现的名称",
                            },
                            "sourceId": {
                                "type": "string",
                                "description": "实现接口的元素 (Block, InterfaceBlock) 的 ID",
                            },
                            "targetId": {
                                "type": "string",
                                "description": "被实现的接口 (Interface, InterfaceBlock) 的 ID",
                            },
                        },
                        "additionalProperties": False,
                        "required": [
                            "id",
                            "type",
                            "name",
                            "sourceId",
                            "targetId",
                        ],
                    },
                    "Link": {
                        "type": "object",
                        "description": "连接 (Link) 的定义",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "连接的唯一标识符",
                            },
                            "type": {
                                "type": "string",
                                "const": "Link",
                                "description": "元素类型，固定为 Link",
                            },
                            "name": {
                                "type": "string",
                                "description": "连接的名称",
                            },
                            "instance1Id": {
                                "type": "string",
                                "description": "连接的实例 1 的 ID",
                            },
                            "instance2Id": {
                                "type": "string",
                                "description": "连接的实例 2 的 ID",
                            },
                            "associationId": {
                                "type": ["string", "null"],
                                "description": "连接对应的关联关系 (Association) 的 ID (如果适用)",
                            },
                        },
                        "additionalProperties": False,
                        "required": [
                            "id",
                            "type",
                            "name",
                            "instance1Id",
                            "instance2Id",
                            "associationId",
                        ],
                    },
                    "AssociationBlock": {
                        "type": "object",
                        "description": "关联块 (Association Block) 的定义",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "关联块的唯一标识符",
                            },
                            "type": {
                                "type": "string",
                                "const": "AssociationBlock",
                                "description": "元素类型，固定为 AssociationBlock",
                            },
                            "name": {
                                "type": "string",
                                "description": "关联块的名称",
                            },
                            "end1Id": {
                                "type": "string",
                                "description": "关联块的端点 1 连接的 Block 的 ID",
                            },
                            "end2Id": {
                                "type": "string",
                                "description": "关联块的端点 2 连接的 Block 的 ID",
                            },
                            "attributeIds": {
                                "type": ["array", "null"],
                                "description": "关联块的属性 ID 列表",
                                "items": {"type": "string"},
                            },
                            "operationIds": {
                                "type": ["array", "null"],
                                "description": "关联块的操作 ID 列表",
                                "items": {"type": "string"},
                            },
                            "constraintIds": {
                                "type": ["array", "null"],
                                "description": "关联块的约束 ID 列表",
                                "items": {"type": "string"},
                            },
                        },
                        "additionalProperties": False,
                        "required": [
                            "id",
                            "type",
                            "name",
                            "end1Id",
                            "end2Id",
                            "attributeIds",
                            "operationIds",
                            "constraintIds",
                        ],
                    },
                    "AssociationBlockWithOwnedEnds": {
                        "type": "object",
                        "description": "带拥有端的关联块 (Association Block with Owned Ends) 的定义 - AssociationBlock 的子类型，为了区分类型",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "带拥有端的关联块的唯一标识符",
                            },
                            "type": {
                                "type": "string",
                                "const": "AssociationBlockWithOwnedEnds",
                                "description": "元素类型，固定为 AssociationBlockWithOwnedEnds",
                            },
                            "name": {
                                "type": "string",
                                "description": "带拥有端的关联块的名称",
                            },
                            "end1Id": {
                                "type": "string",
                                "description": "关联块的端点 1 连接的 Block 的 ID",
                            },
                            "end2Id": {
                                "type": "string",
                                "description": "关联块的端点 2 连接的 Block 的 ID",
                            },
                            "attributeIds": {
                                "type": ["array", "null"],
                                "description": "带拥有端的关联块的属性 ID 列表",
                                "items": {"type": "string"},
                            },
                            "operationIds": {
                                "type": ["array", "null"],
                                "description": "带拥有端的关联块的操作 ID 列表",
                                "items": {"type": "string"},
                            },
                            "constraintIds": {
                                "type": ["array", "null"],
                                "description": "带拥有端的关联块的约束 ID 列表",
                                "items": {"type": "string"},
                            },
                        },
                        "additionalProperties": False,
                        "required": [
                            "id",
                            "type",
                            "name",
                            "end1Id",
                            "end2Id",
                            "attributeIds",
                            "operationIds",
                            "constraintIds",
                        ],
                    },
                    "Association": {
                        "type": "object",
                        "description": "关联 (Association) 的定义",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "关联的唯一标识符",
                            },
                            "type": {
                                "type": "string",
                                "const": "Association",
                                "description": "元素类型，固定为 Association",
                            },
                            "name": {
                                "type": ["string", "null"],
                                "description": "关联的名称",
                            },
                            "sourceId": {
                                "type": "string",
                                "description": "关联关系起始端的元素 ID",
                            },
                            "targetId": {
                                "type": "string",
                                "description": "关联关系目标端的元素 ID",
                            },
                            "sourceMultiplicity": {
                                "type": ["string", "null"],
                                "description": "关联关系起始端的多重性",
                            },
                            "targetMultiplicity": {
                                "type": ["string", "null"],
                                "description": "关联关系目标端的多重性",
                            },
                            "memberEndIds": {
                                "type": ["array", "null"],
                                "description": "关联关系两端的属性 ID 列表",
                                "items": {"type": "string"},
                            },
                            "ownedEndIds": {
                                "type": ["array", "null"],
                                "description": "关联关系拥有端的属性 ID 列表",
                                "items": {"type": "string"},
                            },
                        },
                        "additionalProperties": False,
                        "required": [
                            "id",
                            "type",
                            "name",
                            "sourceId",
                            "targetId",
                            "sourceMultiplicity",
                            "targetMultiplicity",
                            "memberEndIds",
                            "ownedEndIds",
                        ],
                    },
                    "DirectedAssociation": {
                        "type": "object",
                        "description": "有向关联 (Directed Association) 的定义 - Association 的子类型，为了区分类型",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "有向关联的唯一标识符",
                            },
                            "type": {
                                "type": "string",
                                "const": "DirectedAssociation",
                                "description": "元素类型，固定为 DirectedAssociation",
                            },
                            "name": {
                                "type": ["string", "null"],
                                "description": "有向关联的名称",
                            },
                            "sourceId": {
                                "type": "string",
                                "description": "关联关系起始端的元素 ID",
                            },
                            "targetId": {
                                "type": "string",
                                "description": "关联关系目标端的元素 ID",
                            },
                            "sourceMultiplicity": {
                                "type": ["string", "null"],
                                "description": "关联关系起始端的多重性",
                            },
                            "targetMultiplicity": {
                                "type": ["string", "null"],
                                "description": "关联关系目标端的多重性",
                            },
                            "memberEndIds": {
                                "type": ["array", "null"],
                                "description": "关联关系两端的属性 ID 列表",
                                "items": {"type": "string"},
                            },
                            "ownedEndIds": {
                                "type": ["array", "null"],
                                "description": "关联关系拥有端的属性 ID 列表",
                                "items": {"type": "string"},
                            },
                        },
                        "additionalProperties": False,
                        "required": [
                            "id",
                            "type",
                            "name",
                            "sourceId",
                            "targetId",
                            "sourceMultiplicity",
                            "targetMultiplicity",
                            "memberEndIds",
                            "ownedEndIds",
                        ],
                    },
                    "Aggregation": {
                        "type": "object",
                        "description": "聚合 (Aggregation) 的定义 - Association 的子类型，为了区分类型",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "聚合的唯一标识符",
                            },
                            "type": {
                                "type": "string",
                                "const": "Aggregation",
                                "description": "元素类型，固定为 Aggregation",
                            },
                            "name": {
                                "type": ["string", "null"],
                                "description": "聚合的名称",
                            },
                            "sourceId": {
                                "type": "string",
                                "description": "聚合关系起始端的元素 ID (整体)",
                            },
                            "targetId": {
                                "type": "string",
                                "description": "聚合关系目标端的元素 ID (部分)",
                            },
                            "sourceMultiplicity": {
                                "type": ["string", "null"],
                                "description": "聚合关系起始端的多重性",
                            },
                            "targetMultiplicity": {
                                "type": ["string", "null"],
                                "description": "聚合关系目标端的多重性",
                            },
                            "memberEndIds": {
                                "type": ["array", "null"],
                                "description": "聚合关系两端的属性 ID 列表",
                                "items": {"type": "string"},
                            },
                            "ownedEndIds": {
                                "type": ["array", "null"],
                                "description": "聚合关系拥有端的属性 ID 列表",
                                "items": {"type": "string"},
                            },
                        },
                        "additionalProperties": False,
                        "required": [
                            "id",
                            "type",
                            "name",
                            "sourceId",
                            "targetId",
                            "sourceMultiplicity",
                            "targetMultiplicity",
                            "memberEndIds",
                            "ownedEndIds",
                        ],
                    },
                    "DirectedAggregation": {
                        "type": "object",
                        "description": "有向聚合 (Directed Aggregation) 的定义 - Aggregation 的子类型，为了区分类型",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "有向聚合的唯一标识符",
                            },
                            "type": {
                                "type": "string",
                                "const": "DirectedAggregation",
                                "description": "元素类型，固定为 DirectedAggregation",
                            },
                            "name": {
                                "type": ["string", "null"],
                                "description": "有向聚合的名称",
                            },
                            "sourceId": {
                                "type": "string",
                                "description": "聚合关系起始端的元素 ID (整体)",
                            },
                            "targetId": {
                                "type": "string",
                                "description": "聚合关系目标端的元素 ID (部分)",
                            },
                            "sourceMultiplicity": {
                                "type": ["string", "null"],
                                "description": "聚合关系起始端的多重性",
                            },
                            "targetMultiplicity": {
                                "type": ["string", "null"],
                                "description": "聚合关系目标端的多重性",
                            },
                            "memberEndIds": {
                                "type": ["array", "null"],
                                "description": "聚合关系两端的属性 ID 列表",
                                "items": {"type": "string"},
                            },
                            "ownedEndIds": {
                                "type": ["array", "null"],
                                "description": "聚合关系拥有端的属性 ID 列表",
                                "items": {"type": "string"},
                            },
                        },
                        "additionalProperties": False,
                        "required": [
                            "id",
                            "type",
                            "name",
                            "sourceId",
                            "targetId",
                            "sourceMultiplicity",
                            "targetMultiplicity",
                            "memberEndIds",
                            "ownedEndIds",
                        ],
                    },
                    "Composition": {
                        "type": "object",
                        "description": "组合 (Composition) 的定义 - Association 的子类型，为了区分类型",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "组合的唯一标识符",
                            },
                            "type": {
                                "type": "string",
                                "const": "Composition",
                                "description": "元素类型，固定为 Composition",
                            },
                            "name": {
                                "type": ["string", "null"],
                                "description": "组合的名称",
                            },
                            "sourceId": {
                                "type": "string",
                                "description": "组合关系起始端的元素 ID (整体)",
                            },
                            "targetId": {
                                "type": "string",
                                "description": "组合关系目标端的元素 ID (部分)",
                            },
                            "sourceMultiplicity": {
                                "type": ["string", "null"],
                                "description": "组合关系起始端的多重性",
                            },
                            "targetMultiplicity": {
                                "type": ["string", "null"],
                                "description": "组合关系目标端的多重性",
                            },
                            "memberEndIds": {
                                "type": ["array", "null"],
                                "description": "组合关系两端的属性 ID 列表",
                                "items": {"type": "string"},
                            },
                            "ownedEndIds": {
                                "type": ["array", "null"],
                                "description": "组合关系拥有端的属性 ID 列表",
                                "items": {"type": "string"},
                            },
                        },
                        "additionalProperties": False,
                        "required": [
                            "id",
                            "type",
                            "name",
                            "sourceId",
                            "targetId",
                            "sourceMultiplicity",
                            "targetMultiplicity",
                            "memberEndIds",
                            "ownedEndIds",
                        ],
                    },
                    "DirectedComposition": {
                        "type": "object",
                        "description": "有向组合 (Directed Composition) 的定义 - Composition 的子类型，为了区分类型",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "有向组合的唯一标识符",
                            },
                            "type": {
                                "type": "string",
                                "const": "DirectedComposition",
                                "description": "元素类型，固定为 DirectedComposition",
                            },
                            "name": {
                                "type": ["string", "null"],
                                "description": "有向组合的名称",
                            },
                            "sourceId": {
                                "type": "string",
                                "description": "组合关系起始端的元素 ID (整体)",
                            },
                            "targetId": {
                                "type": "string",
                                "description": "组合关系目标端的元素 ID (部分)",
                            },
                            "sourceMultiplicity": {
                                "type": ["string", "null"],
                                "description": "组合关系起始端的多重性",
                            },
                            "targetMultiplicity": {
                                "type": ["string", "null"],
                                "description": "组合关系目标端的多重性",
                            },
                            "memberEndIds": {
                                "type": ["array", "null"],
                                "description": "组合关系两端的属性 ID 列表",
                                "items": {"type": "string"},
                            },
                            "ownedEndIds": {
                                "type": ["array", "null"],
                                "description": "组合关系拥有端的属性 ID 列表",
                                "items": {"type": "string"},
                            },
                        },
                        "additionalProperties": False,
                        "required": [
                            "id",
                            "type",
                            "name",
                            "sourceId",
                            "targetId",
                            "sourceMultiplicity",
                            "targetMultiplicity",
                            "memberEndIds",
                            "ownedEndIds",
                        ],
                    },
                    "Generalization": {
                        "type": "object",
                        "description": "泛化 (Generalization) 的定义",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "泛化的唯一标识符",
                            },
                            "type": {
                                "type": "string",
                                "const": "Generalization",
                                "description": "元素类型，固定为 Generalization",
                            },
                            "name": {
                                "type": "string",
                                "description": "泛化的名称",
                            },
                            "sourceId": {
                                "type": "string",
                                "description": "泛化关系起始端的元素 ID (子类)",
                            },
                            "targetId": {
                                "type": "string",
                                "description": "泛化关系目标端的元素 ID (父类)",
                            },
                            "isSubstitutable": {
                                "type": ["boolean", "null"],
                                "description": "是否可替代",
                            },
                        },
                        "additionalProperties": False,
                        "required": [
                            "id",
                            "type",
                            "name",
                            "sourceId",
                            "targetId",
                            "isSubstitutable",
                        ],
                    },
                    "Usage": {
                        "type": "object",
                        "description": "使用 (Usage) 关系的定义",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "使用关系的唯一标识符",
                            },
                            "type": {
                                "type": "string",
                                "const": "Usage",
                                "description": "元素类型，固定为 Usage",
                            },
                            "name": {
                                "type": ["string", "null"],
                                "description": "使用关系的名称",
                            },
                            "sourceId": {
                                "type": "string",
                                "description": "使用关系起始端的元素 ID (使用者)",
                            },
                            "targetId": {
                                "type": "string",
                                "description": "使用关系目标端的元素 ID (被使用者)",
                            },
                        },
                        "additionalProperties": False,
                        "required": [
                            "id",
                            "type",
                            "name",
                            "sourceId",
                            "targetId",
                        ],
                    },
                    "ItemFlow": {
                        "type": "object",
                        "description": "项流 (Item Flow) 的定义",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "项流的唯一标识符",
                            },
                            "type": {
                                "type": "string",
                                "const": "ItemFlow",
                                "description": "元素类型，固定为 ItemFlow",
                            },
                            "name": {
                                "type": ["string", "null"],
                                "description": "项流的名称",
                            },
                            "sourceId": {
                                "type": "string",
                                "description": "项流起始端的元素 ID",
                            },
                            "targetId": {
                                "type": "string",
                                "description": "项流目标端的元素 ID",
                            },
                            "flowSpecificationId": {
                                "type": "string",
                                "description": "项流关联的流规范 ID",
                            },
                            "itemPropertyIds": {
                                "type": ["array", "null"],
                                "description": "项流的项目属性 ID 列表",
                                "items": {"type": "string"},
                            },
                        },
                        "additionalProperties": False,
                        "required": [
                            "id",
                            "type",
                            "name",
                            "sourceId",
                            "targetId",
                            "flowSpecificationId",
                            "itemPropertyIds",
                        ],
                    },
                    "Comment": {
                        "type": "object",
                        "description": "注释 (Comment) 的定义",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "注释的唯一标识符",
                            },
                            "type": {
                                "type": "string",
                                "const": "Comment",
                                "description": "元素类型，固定为 Comment",
                            },
                            "body": {
                                "type": "string",
                                "description": "注释内容",
                            },
                            "annotatedElementId": {
                                "type": "string",
                                "description": "注释所关联的元素的ID",
                            },
                        },
                        "additionalProperties": False,
                        "required": [
                            "id",
                            "type",
                            "body",
                            "annotatedElementId",
                        ],
                    },
                    "InternalBlock": {
                        "type": "object",
                        "description": "内部块 (Internal Block) 的定义",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "内部块的唯一标识符",
                            },
                            "type": {
                                "type": "string",
                                "const": "InternalBlock",
                                "description": "元素类型，固定为 InternalBlock",
                            },
                            "name": {
                                "type": "string",
                                "description": "内部块的名称",
                            },
                            "attributeIds": {
                                "type": ["array", "null"],
                                "description": "内部块的属性 ID 列表",
                                "items": {"type": "string"},
                            },
                            "partIds": {
                                "type": ["array", "null"],
                                "description": "内部块的部件 ID 列表",
                                "items": {"type": "string"},
                            },
                            "of": {
                                "type": "string",
                                "description": "引用的 BDD 中的块的 ID",
                            },
                        },
                        "additionalProperties": False,
                        "required": [
                            "id",
                            "type",
                            "name",
                            "attributeIds",
                            "partIds",
                            "of",
                        ],
                    },
                    "Requirement": {
                        "type": "object",
                        "description": "需求 (Requirement) 的定义",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "需求的唯一标识符",
                            },
                            "type": {
                                "type": "string",
                                "const": "Requirement",
                                "description": "元素类型，固定为 Requirement",
                            },
                            "name": {
                                "type": "string",
                                "description": "需求的名称",
                            },
                            "text": {
                                "type": "string",
                                "description": "需求的文本描述",
                            },
                            "attributeIds": {
                                "type": ["array", "null"],
                                "description": "需求的属性 ID 列表",
                                "items": {"type": "string"},
                            },
                            "reqId": {
                                "type": ["string", "null"],
                                "description": "需求ID, 对应xmi文件中的reqId属性",
                            },
                        },
                        "additionalProperties": False,
                        "required": [
                            "id",
                            "type",
                            "name",
                            "text",
                            "attributeIds",
                            "reqId",
                        ],
                    },
                    "Actor": {
                        "type": "object",
                        "description": "参与者 (Actor) 的定义",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "参与者的唯一标识符",
                            },
                            "type": {
                                "type": "string",
                                "const": "Actor",
                                "description": "元素类型，固定为 Actor",
                            },
                            "name": {
                                "type": "string",
                                "description": "参与者的名称",
                            },
                            "attributeIds": {
                                "type": ["array", "null"],
                                "description": "参与者的属性 ID 列表",
                                "items": {"type": "string"},
                            },
                        },
                        "additionalProperties": False,
                        "required": ["id", "type", "name", "attributeIds"],
                    },
                    "UseCase": {
                        "type": "object",
                        "description": "用例 (UseCase) 的定义",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "用例的唯一标识符",
                            },
                            "type": {
                                "type": "string",
                                "const": "UseCase",
                                "description": "元素类型，固定为 UseCase",
                            },
                            "name": {
                                "type": "string",
                                "description": "用例的名称",
                            },
                            "attributeIds": {
                                "type": ["array", "null"],
                                "description": "用例的属性 ID 列表",
                                "items": {"type": "string"},
                            },
                        },
                        "additionalProperties": False,
                        "required": ["id", "type", "name", "attributeIds"],
                    },
                    "Activity": {
                        "type": "object",
                        "description": "活动 (Activity) 的定义",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "活动的唯一标识符",
                            },
                            "type": {
                                "type": "string",
                                "const": "Activity",
                                "description": "元素类型，固定为 Activity",
                            },
                            "name": {
                                "type": "string",
                                "description": "活动的名称",
                            },
                            "attributeIds": {
                                "type": ["array", "null"],
                                "description": "活动的属性 ID 列表",
                                "items": {"type": "string"},
                            },
                        },
                        "additionalProperties": False,
                        "required": ["id", "type", "name", "attributeIds"],
                    },
                    "State": {
                        "type": "object",
                        "description": "状态 (State) 的定义",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "状态的唯一标识符",
                            },
                            "type": {
                                "type": "string",
                                "const": "State",
                                "description": "元素类型，固定为 State",
                            },
                            "name": {
                                "type": "string",
                                "description": "状态的名称",
                            },
                            "attributeIds": {
                                "type": ["array", "null"],
                                "description": "状态的属性 ID 列表",
                                "items": {"type": "string"},
                            },
                        },
                        "additionalProperties": False,
                        "required": ["id", "type", "name", "attributeIds"],
                    },
                    "Lifeline": {
                        "type": "object",
                        "description": "生命线 (Lifeline) 的定义",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "生命线的唯一标识符",
                            },
                            "type": {
                                "type": "string",
                                "const": "Lifeline",
                                "description": "元素类型，固定为 Lifeline",
                            },
                            "name": {
                                "type": "string",
                                "description": "生命线的名称",
                            },
                            "represents": {
                                "type": ["string", "null"],
                                "description": "生命线所代表的元素的 ID",
                            },
                        },
                        "additionalProperties": False,
                        "required": ["id", "type", "name", "represents"],
                    },
                    "Message": {
                        "type": "object",
                        "description": "消息 (Message) 的定义",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "消息的唯一标识符",
                            },
                            "type": {
                                "type": "string",
                                "const": "Message",
                                "description": "元素类型，固定为 Message",
                            },
                            "name": {
                                "type": "string",
                                "description": "消息的名称",
                            },
                            "source": {
                                "type": "string",
                                "description": "消息的起始生命线 ID",
                            },
                            "target": {
                                "type": "string",
                                "description": "消息的目标生命线 ID",
                            },
                            "messageType": {
                                "type": ["string", "null"],
                                "description": "消息的类型",
                                "enum": [
                                    "synchronous",
                                    "asynchronous",
                                    "reply",
                                ],
                            },
                            "signature": {
                                "type": ["string", "null"],
                                "description": "消息所关联的操作的 ID",
                            },
                        },
                        "additionalProperties": False,
                        "required": [
                            "id",
                            "type",
                            "name",
                            "source",
                            "target",
                            "messageType",
                            "signature",
                        ],
                    },
                    "Dependency": {
                        "type": "object",
                        "description": "依赖关系 (Dependency) 的定义",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "依赖关系的唯一标识符",
                            },
                            "type": {
                                "type": "string",
                                "const": "Dependency",
                                "description": "元素类型，固定为 Dependency",
                            },
                            "name": {
                                "type": ["string", "null"],
                                "description": "依赖关系的名称",
                            },
                            "sourceId": {
                                "type": "string",
                                "description": "依赖关系起始端的元素 ID",
                            },
                            "targetId": {
                                "type": "string",
                                "description": "依赖关系目标端的元素 ID",
                            },
                            "sourceMultiplicity": {
                                "type": ["string", "null"],
                                "description": "依赖关系起始端的多重性",
                            },
                            "targetMultiplicity": {
                                "type": ["string", "null"],
                                "description": "依赖关系目标端的多重性",
                            },
                        },
                        "additionalProperties": False,
                        "required": [
                            "id",
                            "type",
                            "name",
                            "sourceId",
                            "targetId",
                            "sourceMultiplicity",
                            "targetMultiplicity",
                        ],
                    },
                    "Realization": {
                        "type": "object",
                        "description": "实现关系 (Realization) 的定义",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "实现关系的唯一标识符",
                            },
                            "type": {
                                "type": "string",
                                "const": "Realization",
                                "description": "元素类型，固定为 Realization",
                            },
                            "name": {
                                "type": ["string", "null"],
                                "description": "实现关系的名称",
                            },
                            "sourceId": {
                                "type": "string",
                                "description": "实现关系起始端的元素 ID",
                            },
                            "targetId": {
                                "type": "string",
                                "description": "实现关系目标端的元素 ID",
                            },
                            "sourceMultiplicity": {
                                "type": ["string", "null"],
                                "description": "实现关系起始端的多重性",
                            },
                            "targetMultiplicity": {
                                "type": ["string", "null"],
                                "description": "实现关系目标端的多重性",
                            },
                        },
                        "additionalProperties": False,
                        "required": [
                            "id",
                            "type",
                            "name",
                            "sourceId",
                            "targetId",
                            "sourceMultiplicity",
                            "targetMultiplicity",
                        ],
                    },
                    "Abstraction": {
                        "type": "object",
                        "description": "抽象关系 (Abstraction) 的定义",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "抽象关系的唯一标识符",
                            },
                            "type": {
                                "type": "string",
                                "const": "Abstraction",
                                "description": "元素类型，固定为 Abstraction",
                            },
                            "name": {
                                "type": ["string", "null"],
                                "description": "抽象关系的名称",
                            },
                            "sourceId": {
                                "type": "string",
                                "description": "抽象关系起始端的元素 ID",
                            },
                            "targetId": {
                                "type": "string",
                                "description": "抽象关系目标端的元素 ID",
                            },
                            "sourceMultiplicity": {
                                "type": ["string", "null"],
                                "description": "抽象关系起始端的多重性",
                            },
                            "targetMultiplicity": {
                                "type": ["string", "null"],
                                "description": "抽象关系目标端的多重性",
                            },
                        },
                        "additionalProperties": False,
                        "required": [
                            "id",
                            "type",
                            "name",
                            "sourceId",
                            "targetId",
                            "sourceMultiplicity",
                            "targetMultiplicity",
                        ],
                    },
                    "Include": {
                        "type": "object",
                        "description": "包含关系 (Include) 的定义",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "包含关系的唯一标识符",
                            },
                            "type": {
                                "type": "string",
                                "const": "Include",
                                "description": "元素类型，固定为 Include",
                            },
                            "name": {
                                "type": ["string", "null"],
                                "description": "包含关系的名称",
                            },
                            "sourceId": {
                                "type": "string",
                                "description": "包含关系起始端的元素 ID (通常是用例)",
                            },
                            "targetId": {
                                "type": "string",
                                "description": "包含关系目标端的元素 ID (通常是用例)",
                            },
                            "sourceMultiplicity": {
                                "type": ["string", "null"],
                                "description": "包含关系起始端的多重性",
                            },
                            "targetMultiplicity": {
                                "type": ["string", "null"],
                                "description": "包含关系目标端的多重性",
                            },
                        },
                        "additionalProperties": False,
                        "required": [
                            "id",
                            "type",
                            "name",
                            "sourceId",
                            "targetId",
                            "sourceMultiplicity",
                            "targetMultiplicity",
                        ],
                    },
                    "Extend": {
                        "type": "object",
                        "description": "扩展关系 (Extend) 的定义",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "扩展关系的唯一标识符",
                            },
                            "type": {
                                "type": "string",
                                "const": "Extend",
                                "description": "元素类型，固定为 Extend",
                            },
                            "name": {
                                "type": ["string", "null"],
                                "description": "扩展关系的名称",
                            },
                            "sourceId": {
                                "type": "string",
                                "description": "扩展关系起始端的元素 ID (通常是用例)",
                            },
                            "targetId": {
                                "type": "string",
                                "description": "扩展关系目标端的元素 ID (通常是用例)",
                            },
                            "sourceMultiplicity": {
                                "type": ["string", "null"],
                                "description": "扩展关系起始端的多重性",
                            },
                            "targetMultiplicity": {
                                "type": ["string", "null"],
                                "description": "扩展关系目标端的多重性",
                            },
                        },
                        "additionalProperties": False,
                        "required": [
                            "id",
                            "type",
                            "name",
                            "sourceId",
                            "targetId",
                            "sourceMultiplicity",
                            "targetMultiplicity",
                        ],
                    },
                    "ControlFlow": {
                        "type": "object",
                        "description": "控制流 (ControlFlow) 的定义",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "控制流的唯一标识符",
                            },
                            "type": {
                                "type": "string",
                                "const": "ControlFlow",
                                "description": "元素类型，固定为 ControlFlow",
                            },
                            "name": {
                                "type": ["string", "null"],
                                "description": "控制流的名称",
                            },
                            "sourceId": {
                                "type": "string",
                                "description": "控制流起始端的元素 ID (通常是活动)",
                            },
                            "targetId": {
                                "type": "string",
                                "description": "控制流目标端的元素 ID (通常是活动)",
                            },
                            "guard": {
                                "type": ["string", "null"],
                                "description": "控制流的守卫条件",
                            },
                        },
                        "additionalProperties": False,
                        "required": [
                            "id",
                            "type",
                            "name",
                            "sourceId",
                            "targetId",
                            "guard",
                        ],
                    },
                    "ObjectFlow": {
                        "type": "object",
                        "description": "对象流 (ObjectFlow) 的定义",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "对象流的唯一标识符",
                            },
                            "type": {
                                "type": "string",
                                "const": "ObjectFlow",
                                "description": "元素类型，固定为 ObjectFlow",
                            },
                            "name": {
                                "type": ["string", "null"],
                                "description": "对象流的名称",
                            },
                            "sourceId": {
                                "type": "string",
                                "description": "对象流起始端的元素 ID (通常是活动)",
                            },
                            "targetId": {
                                "type": "string",
                                "description": "对象流目标端的元素 ID (通常是活动)",
                            },
                            "guard": {
                                "type": ["string", "null"],
                                "description": "对象流的守卫条件",
                            },
                        },
                        "additionalProperties": False,
                        "required": [
                            "id",
                            "type",
                            "name",
                            "sourceId",
                            "targetId",
                            "guard",
                        ],
                    },
                    "Transition": {
                        "type": "object",
                        "description": "状态转换 (Transition) 的定义",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "状态转换的唯一标识符",
                            },
                            "type": {
                                "type": "string",
                                "const": "Transition",
                                "description": "元素类型，固定为 Transition",
                            },
                            "name": {
                                "type": ["string", "null"],
                                "description": "状态转换的名称",
                            },
                            "sourceId": {
                                "type": "string",
                                "description": "状态转换起始端的状态 ID",
                            },
                            "targetId": {
                                "type": "string",
                                "description": "状态转换目标端的状态 ID",
                            },
                            "trigger": {
                                "type": ["string", "null"],
                                "description": "触发状态转换的事件",
                            },
                            "guard": {
                                "type": ["string", "null"],
                                "description": "状态转换的守卫条件",
                            },
                            "effect": {
                                "type": ["string", "null"],
                                "description": "状态转换发生时执行的动作",
                            },
                        },
                        "additionalProperties": False,
                        "required": [
                            "id",
                            "type",
                            "name",
                            "sourceId",
                            "targetId",
                            "trigger",
                            "guard",
                            "effect",
                        ],
                    },
                    "Part": {
                        "type": "object",
                        "description": "部件 (Part) 的定义",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "部件的唯一标识符",
                            },
                            "type": {
                                "type": "string",
                                "const": "Part",
                                "description": "元素类型，固定为 Part",
                            },
                            "name": {
                                "type": "string",
                                "description": "部件的名称",
                            },
                            "of": {
                                "type": "string",
                                "description": "部件所属的块的 ID",
                            },
                        },
                        "additionalProperties": False,
                        "required": ["id", "type", "name", "of"],
                    },
                    "Connector": {
                        "type": "object",
                        "description": "连接器 (Connector) 的定义",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "连接器的唯一标识符",
                            },
                            "type": {
                                "type": "string",
                                "const": "Connector",
                                "description": "元素类型，固定为 Connector",
                            },
                            "name": {
                                "type": ["string", "null"],
                                "description": "连接器的名称",
                            },
                            "source": {
                                "type": "string",
                                "description": "连接器起始端的部件或端口 ID",
                            },
                            "target": {
                                "type": "string",
                                "description": "连接器目标端的部件或端口 ID",
                            },
                            "kind": {
                                "type": "string",
                                "enum": ["assembly", "delegation"],
                                "description": "连接器的类型",
                            },
                        },
                        "additionalProperties": False,
                        "required": [
                            "id",
                            "type",
                            "name",
                            "source",
                            "target",
                            "kind",
                        ],
                    },
                    "Constraint": {
                        "type": "object",
                        "description": "约束 (Constraint) 的定义",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "约束的唯一标识符",
                            },
                            "type": {
                                "type": "string",
                                "const": "Constraint",
                                "description": "元素类型，固定为 Constraint",
                            },
                            "name": {
                                "type": "string",
                                "description": "约束的名称",
                            },
                            "specification": {
                                "type": "string",
                                "description": "约束的表达式",
                            },
                            "constrainedElementIds": {
                                "type": ["array", "null"],
                                "description": "受约束的元素 ID 列表",
                                "items": {"type": "string"},
                            },
                        },
                        "additionalProperties": False,
                        "required": [
                            "id",
                            "type",
                            "name",
                            "specification",
                            "constrainedElementIds",
                        ],
                    },
                    "Parameter": {
                        "type": "object",
                        "description": "参数 (Parameter) 的定义",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "参数的唯一标识符",
                            },
                            "type": {
                                "type": "string",
                                "const": "Parameter",
                                "description": "元素类型，固定为 Parameter",
                            },
                            "name": {
                                "type": "string",
                                "description": "参数的名称",
                            },
                            "parameterType": {
                                "type": "string",
                                "description": "参数的类型",
                            },
                            "defaultValue": {
                                "type": ["string", "null"],
                                "description": "参数的默认值",
                            },
                        },
                        "additionalProperties": False,
                        "required": [
                            "id",
                            "type",
                            "name",
                            "parameterType",
                            "defaultValue",
                        ],
                    },
                    "Attribute": {
                        "type": "object",
                        "description": "属性 (Attribute/Property) 的定义",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "属性的唯一标识符",
                            },
                            "type": {
                                "type": "string",
                                "const": "Property",
                                "description": "元素类型，固定为 Property",
                            },
                            "name": {
                                "type": "string",
                                "description": "属性的名称",
                            },
                            "propertyType": {
                                "type": "string",
                                "description": "属性的类型",
                                "enum": [
                                    "String",
                                    "Integer",
                                    "Double",
                                    "Boolean",
                                    "Operation",
                                    "Real",
                                ],
                            },
                            "value": {
                                "type": ["string", "null"],
                                "description": "属性的值",
                            },
                            "visibility": {
                                "type": ["string", "null"],
                                "description": "属性的可见性",
                                "enum": [
                                    "public",
                                    "private",
                                    "protected",
                                    "package",
                                ],
                            },
                            "aggregation": {
                                "type": ["string", "null"],
                                "description": "属性的聚合类型",
                                "enum": ["none", "shared", "composite"],
                            },
                            "lowerValue": {
                                "type": ["string", "null"],
                                "description": "属性的多重性下限",
                            },
                            "upperValue": {
                                "type": ["string", "null"],
                                "description": "属性的多重性上限",
                            },
                            "defaultValue": {
                                "type": ["string", "null"],
                                "description": "属性的默认值",
                            },
                            "isReadOnly": {
                                "type": ["boolean", "null"],
                                "description": "属性是否为只读",
                            },
                            "isStatic": {
                                "type": ["boolean", "null"],
                                "description": "属性是否为静态",
                            },
                            "isDerived": {
                                "type": ["boolean", "null"],
                                "description": "属性是否为派生",
                            },
                            "isDerivedUnion": {
                                "type": ["boolean", "null"],
                                "description": "属性是否为派生联合",
                            },
                            "isOrdered": {
                                "type": ["boolean", "null"],
                                "description": "属性是否为有序",
                            },
                            "isUnique": {
                                "type": ["boolean", "null"],
                                "description": "属性是否为唯一",
                            },
                            "isID": {
                                "type": ["boolean", "null"],
                                "description": "属性是否为ID",
                            },
                        },
                        "additionalProperties": False,
                        "required": [
                            "id",
                            "type",
                            "name",
                            "propertyType",
                            "value",
                            "visibility",
                            "aggregation",
                            "lowerValue",
                            "upperValue",
                            "defaultValue",
                            "isReadOnly",
                            "isStatic",
                            "isDerived",
                            "isDerivedUnion",
                            "isOrdered",
                            "isUnique",
                            "isID",
                        ],
                    },
                },
                "additionalProperties": False,
                "required": ["diagramType", "elements"],
            },
        },
    }


spec_json_schema = {
        "type": "json_schema",
        "json_schema": {
            "name": "System_Design_Schema",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "designScenario": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "The name of the designed system",
                            },
                            "description": {
                                "type": "string",
                                "description": "A description of the design scenario",
                            },
                            "requirements": {
                                "type": "array",
                                "description": "List of requirements for the system",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "title": {
                                            "type": "string",
                                            "description": "Title of the requirement",
                                        },
                                        "type": {
                                            "type": "string",
                                            "enum": [
                                                "functional",
                                                "performance",
                                                "safety",
                                                "nonFunctional",
                                            ],
                                            "description": "The type of the requirement",
                                        },
                                        "details": {
                                            "type": "array",
                                            "description": "Details for the requirement",
                                            "items": {
                                                "type": "object",
                                                "properties": {
                                                    "description": {
                                                        "type": "string",
                                                        "description": "A description of the specific detail",
                                                    }
                                                },
                                                "additionalProperties": False,
                                                "required": ["description"],
                                            },
                                        },
                                    },
                                    "additionalProperties": False,
                                    "required": [
                                        "title",
                                        "type",
                                        "details",
                                    ],
                                },
                            },
                        },
                        "additionalProperties": False,
                        "required": ["name", "description", "requirements"],
                    },
                    "systemComponents": {
                        "type": "array",
                        "description": "List of system components",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {
                                    "type": "string",
                                    "description": "Name of the system component",
                                },
                                "description": {
                                    "type": "string",
                                    "description": "Description of the system component",
                                },
                                "type": {
                                    "type": "string",
                                    "description": "Type of the system component",
                                },
                                "subComponents": {
                                    "type": ["array", "null"],
                                    "description": "Subcomponents within the system component",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "name": {
                                                "type": "string",
                                                "description": "Name of the subcomponent",
                                            },
                                            "description": {
                                                "type": "string",
                                                "description": "Description of the subcomponent",
                                            },
                                            "type": {
                                                "type": "string",
                                                "description": "Type of the subcomponent",
                                            },
                                        },
                                        "additionalProperties": False,
                                        "required": [
                                            "name",
                                            "description",
                                            "type",
                                        ],
                                    },
                                },
                            },
                            "additionalProperties": False,
                            "required": [
                                "name",
                                "type",
                                "description",
                                "subComponents",
                            ],
                        },
                    },
                    "relationships": {
                        "type": "array",
                        "description": "List of relationships between system components",
                        "items": {
                            "type": "object",
                            "properties": {
                                "source": {
                                    "type": "string",
                                    "description": "ID of the source component in the relationship",
                                },
                                "target": {
                                    "type": "string",
                                    "description": "ID of the target component in the relationship",
                                },
                                "relationshipType": {
                                    "type": "string",
                                    "enum": [
                                        "association",
                                        "aggregation",
                                        "dependency",
                                        "composition",
                                    ],
                                    "description": "Type of relationship",
                                },
                                "description": {
                                    "type": "string",
                                    "description": "Description of the relationship",
                                },
                            },
                            "additionalProperties": False,
                            "required": [
                                "source",
                                "target",
                                "relationshipType",
                                "description",
                            ],
                        },
                    },
                    "attributes": {
                        "type": "array",
                        "description": "Attributes of the system components",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {
                                    "type": "string",
                                    "description": "Name of the attribute",
                                },
                                "type": {
                                    "type": "string",
                                    "description": "Type of the attribute",
                                },
                                "value": {
                                    "type": "string",
                                    "description": "Value of the attribute",
                                },
                                "description": {
                                    "type": "string",
                                    "description": "Description of the attribute",
                                },
                            },
                            "additionalProperties": False,
                            "required": [
                                "name",
                                "type",
                                "description",
                                "value",
                            ],
                        },
                    },
                },
                "additionalProperties": False,
                "required": [
                    "designScenario",
                    "systemComponents",
                    "relationships",
                    "attributes",
                ],
            },
        },
    }
