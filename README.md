# SysML BDD Auto Expansion Tool / SysML BDD 自动建模工具

[English](#english) | [中文](#chinese)

<a id="english"></a>
## English

### Introduction

SysML Auto Expansion Tool is a system modeling tool based on Large Language Models (LLMs). It can automatically model systems, expand subsystems, and maintain the relationships between them. The tool supports multiple LLM providers including GPT, Claude, DPSK, and Qwen.

Data are in dataset/. Experimental results are in result/.
### Installation

1. Clone the repository:
```
git clone <repository-url>
cd auto-expansion-sysml
```

2. Initialize the database:
```
python -m auto_expansion_sysml --init-db
```

### Usage

#### Command Line Interface

The tool provides a command line interface with various options:

```
python -m auto_expansion_sysml [OPTIONS]
```

#### Options

| Option | Description |
|--------|-------------|
| `--init-db` | Initialize the database |
| `--start-api` | Start the API server |
| `--model SYSTEM_NAME` | Model a system by name |
| `--auto-expand` | Automatically expand subsystems when modeling |
| `--global-modeling` | Start global auto modeling to traverse all systems in the database |
| `--include-root` | Include the root node (airplane) in global modeling |
| `--single-model SYSTEM_NAME` | Perform a single modeling of a system without storing in the database |
| `--output-dir DIR` | Specify the output directory for single model results (default: "single_model_results") |
| `--provider PROVIDER` | Specify the LLM provider to use (gpt, claude, dpsk, or qwen) (default: "gpt") |

#### Examples

2. Model a specific system:
```
python -m auto_expansion_sysml --model "Engine System" --provider gpt
```

3. Model a system and automatically expand its subsystems:
```
python -m auto_expansion_sysml --model "Aircraft Electrical System" --auto-expand --provider claude
```

4. Perform global modeling of all systems in the database:
```
python -m auto_expansion_sysml --global-modeling --provider qwen
```

5. Model a system without storing in the database:
```
python -m auto_expansion_sysml --single-model "Fuel System" --provider dpsk
```

6. Model a system with a specific output directory:
```
python -m auto_expansion_sysml --single-model "Navigation System" --output-dir "nav_results" --provider gpt
```

### Configuration

The configuration is stored in `auto_expansion_sysml/.envexample`, deleting 'example' and modify to your configuration. You can modify this file to change API, port, database connections, etc.

---

<a id="chinese"></a>
## 中文

### 简介

SysML自动展开工具是一个基于大语言模型(LLM)的系统建模工具。它可以自动建模系统，展开子系统，并维护它们之间的关系。该工具支持多种LLM提供商，包括GPT、Claude、DPSK和Qwen。


### 安装

1. 克隆仓库：
```
git clone <仓库地址>
cd auto-expansion-sysml
```

3. 初始化数据库：
```
python -m auto_expansion_sysml --init-db
```

### 使用方法

#### 命令行界面

该工具提供命令行界面，具有多种选项：

```
python -m auto_expansion_sysml [选项]
```

#### 选项

| 选项 | 描述 |
|------|------|
| `--init-db` | 初始化数据库 |
| `--start-api` | 启动API服务器 |
| `--model 系统名称` | 按名称建模系统 |
| `--auto-expand` | 建模时自动扩展子系统 |
| `--global-modeling` | 启动全局自动建模功能，遍历数据库中所有系统并建模 |
| `--include-root` | 全局建模时包含根节点(airplane) |
| `--single-model 系统名称` | 单次建模系统，无论是否存在系统都生成新模型（不存入数据库） |
| `--output-dir 目录` | 指定单次建模结果的输出目录（默认："single_model_results"） |
| `--provider 提供商` | 指定要使用的LLM提供商 (gpt, claude, dpsk, 或 qwen)（默认："gpt"） |

#### 示例

2. 建模特定系统：
```
python -m auto_expansion_sysml --model "发动机系统" --provider gpt
```

3. 建模系统并自动扩展其子系统：
```
python -m auto_expansion_sysml --model "飞机电气系统" --auto-expand --provider claude
```

4. 执行数据库中所有系统的全局建模：
```
python -m auto_expansion_sysml --global-modeling --provider qwen
```

5. 不存入数据库的单次系统建模：
```
python -m auto_expansion_sysml --single-model "燃油系统" --provider dpsk
```

6. 使用特定输出目录的系统建模：
```
python -m auto_expansion_sysml --single-model "导航系统" --output-dir "导航结果" --provider gpt
```

### 配置

配置存储在`auto_expansion_sysml/.envexample`中，删除example并修改其中的配置。您可以修改此文件以更改API、端口、数据库连接等。 