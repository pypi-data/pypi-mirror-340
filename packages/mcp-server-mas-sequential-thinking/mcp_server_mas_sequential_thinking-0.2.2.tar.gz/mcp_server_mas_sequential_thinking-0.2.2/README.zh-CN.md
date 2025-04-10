# 序列化思考多智能体系统 (MAS) ![](https://img.shields.io/badge/A%20FRAD%20PRODUCT-WIP-yellow)

[![Twitter Follow](https://img.shields.io/twitter/follow/FradSer?style=social)](https://twitter.com/FradSer) [![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/) [![Framework](https://img.shields.io/badge/Framework-Agno-orange.svg)](https://github.com/cognitivecomputations/agno) 

[English](README.md) | 简体中文

本项目使用基于 **Agno** 框架构建并通过 **MCP** 提供服务的**多智能体系统 (MAS)**，实现了一个先进的序列化思考过程。它代表了从简单的状态跟踪方法的重大演进，利用协调的专门化智能体进行更深入的分析和问题分解。

## 概述

该服务器提供了一个用于复杂问题解决的复杂 `sequentialthinking` 工具。与[其前身]([https://github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking)不同，此版本利用了多智能体系统 (MAS) 架构，其中：

  * **一个协调智能体** (`coordinate` 模式下的 `Team` 对象) 管理工作流程。
  * **专门化智能体** (规划器、研究员、分析器、评论家、合成器) 根据其定义的角色和专业知识处理特定的子任务。
  * 传入的思考被智能体团队主动**处理、分析和综合**，而不仅仅是记录。
  * 系统支持复杂的思考模式，包括对先前步骤的**修订**和探索替代路径的**分支**。
  * 与外部工具（如通过研究员智能体使用的 **Exa**）集成，允许动态信息收集。
  * 强大的 **Pydantic** 验证确保了思考步骤的数据完整性。
  * 详细的**日志记录**跟踪整个过程，包括智能体交互（由协调器处理）。

目标是通过利用协同工作的专门化角色的力量，实现比单个智能体或简单状态跟踪更高质量的分析和更细致的思考过程。

## 与原始版本 (TypeScript) 的主要区别

这个 Python/Agno 实现标志着与原始 TypeScript 版本的根本性转变：

| 功能/方面        | Python/Agno 版本 (当前)                               | TypeScript 版本 (原始)                    |
| :--------------- | :---------------------------------------------------- | :---------------------------------------- |
| **架构** | **多智能体系统 (MAS)**；由智能体团队进行主动处理。        | **单一类状态跟踪器**；简单的日志记录/存储。   |
| **智能** | **分布式智能体逻辑**；嵌入在专门化智能体和协调器中。      | **仅外部 LLM**；无内部智能。               |
| **处理** | **主动分析与综合**；智能体对思考 *采取行动*。            | **被动日志记录**；仅记录思考。              |
| **框架** | **Agno (MAS) + FastMCP (服务器)**；使用专门的 MAS 库。 | **仅 MCP SDK**。                          |
| **协调** | **显式的团队协调逻辑** (`coordinate` 模式下的 `Team`)。 | **无**；没有协调概念。                     |
| **验证** | **Pydantic Schema 验证**；强大的数据验证。             | **基本类型检查**；可靠性较低。             |
| **外部工具** | **集成 (通过研究员使用 Exa)**；可以执行研究任务。         | **无**。                                  |
| **日志记录** | **结构化 Python 日志记录 (文件 + 控制台)**；可配置。    | **使用 Chalk 的控制台日志记录**；基础。      |
| **语言与生态** | **Python**；利用 Python AI/ML 生态系统。                 | **TypeScript/Node.js**。                  |

本质上，该系统从一个被动的思考*记录器*演变成了一个由 AI 智能体协作团队驱动的主动思考*处理器*。

## 工作原理 (Coordinate 模式)

1.  **启动：** 外部 LLM 使用 `sequential-thinking-starter` 提示来定义问题并启动过程。
2.  **工具调用：** LLM 使用根据 `ThoughtData` 模型结构的第一个（或后续）思考调用 `sequentialthinking` 工具。
3.  **验证与记录：** 工具接收调用，使用 Pydantic 验证输入，记录传入的思考，并通过 `AppContext` 更新历史/分支状态。
4.  **协调器调用：** 核心思考内容（以及关于修订/分支的上下文）被传递给 `SequentialThinkingTeam` 的 `arun` 方法。
5.  **协调器分析与委派：** `Team`（作为协调器）分析输入的思考，将其分解为子任务，并将这些子任务委派给*最相关*的专家智能体（例如，分析任务给分析器，信息需求给研究员）。
6.  **专家执行：** 被委派的智能体使用它们的指令、模型和工具（如 `ThinkingTools` 或 `ExaTools`）执行其特定的子任务。
7.  **响应收集：** 专家将其结果返回给协调器。
8.  **综合与指导：** 协调器将专家的响应综合成一个单一、连贯的输出。它可能包含基于专家发现（尤其是评论家和分析器）的修订或分支建议。它还为 LLM 如何构思下一个思考添加指导。
9.  **返回值：** 工具返回一个包含协调器综合响应、状态和更新上下文（分支、历史长度）的 JSON 字符串。
10. **迭代：** 调用 LLM 使用协调器的响应和指导来构思下一次 `sequentialthinking` 工具调用，可能会根据建议触发修订或分支。

## Token 消耗警告

⚠️ **高 Token 使用量：** 由于采用了多智能体系统架构，此工具比单智能体替代方案或之前的 TypeScript 版本消耗**显著更多**的 Token。每次 `sequentialthinking` 调用会触发：

  * 协调器智能体（即 `Team` 本身）。
  * 多个专家智能体（可能包括规划器、研究员、分析器、评论家、合成器，具体取决于协调器的委派）。

这种并行处理导致 Token 使用量（每个思考步骤可能增加 3-6 倍或更多）远高于单智能体或状态跟踪方法。请相应地进行预算和规划。此工具优先考虑**分析深度和质量**而非 Token 效率。

## 先决条件

  * Python 3.10+
  * 访问兼容的 LLM API（为 `agno` 配置）。系统现在支持：
      * **Groq:** 需要 `GROQ_API_KEY`。
      * **DeepSeek:** 需要 `DEEPSEEK_API_KEY`。
      * **OpenRouter:** 需要 `OPENROUTER_API_KEY`。
      * 使用 `LLM_PROVIDER` 环境变量配置所需的提供商（默认为 `deepseek`）。
  * Exa API 密钥（如果使用研究员智能体的功能）
      * `EXA_API_KEY` 环境变量。
  * `uv` 包管理器（推荐）或 `pip`。

## MCP 服务器配置 (客户端)

此服务器作为标准可执行脚本运行，通过 stdio 进行通信，符合 MCP 的预期。确切的配置方法取决于您具体的 MCP 客户端实现。请查阅您客户端的文档以获取详细信息。

`env` 部分应包含您选择的 `LLM_PROVIDER` 对应的 API 密钥。

```json
{
  "mcpServers": {
      "mas-sequential-thinking": {
      "command": "uvx",
      "args": [
        "mcp-server-mas-sequential-thinking"
      ],
      "env": {
        "LLM_PROVIDER": "deepseek", // 或 "groq", "openrouter"
        // "GROQ_API_KEY": "你的_groq_api_密钥", // 仅当 LLM_PROVIDER="groq" 时需要
        "DEEPSEEK_API_KEY": "你的_deepseek_api_密钥", // 默认提供商
        // "OPENROUTER_API_KEY": "你的_openrouter_api_密钥", // 仅当 LLM_PROVIDER="openrouter" 时需要
        "DEEPSEEK_BASE_URL": "你的_base_url_如果需要", // 可选：如果为 DeepSeek 使用自定义端点
        "EXA_API_KEY": "你的_exa_api_密钥" // 仅当使用 Exa 时需要
      }
    }
  }
}
```

## 安装与设置

1.  **克隆仓库：**

    ```bash
    git clone git@github.com:FradSer/mcp-server-mas-sequential-thinking.git
    cd mcp-server-mas-sequential-thinking
    ```

2.  **设置环境变量：**
    在根目录创建一个 `.env` 文件或导出变量：

    ```dotenv
    # --- LLM 配置 ---
    # 选择 LLM 提供商: "deepseek" (默认), "groq", 或 "openrouter"
    LLM_PROVIDER="deepseek"

    # 提供所选提供商的 API 密钥:
    # GROQ_API_KEY="你的_groq_api_密钥"
    DEEPSEEK_API_KEY="你的_deepseek_api_密钥"
    # OPENROUTER_API_KEY="你的_openrouter_api_密钥"

    # 可选: 基础 URL 覆盖 (例如, 用于自定义 DeepSeek 端点)
    DEEPSEEK_BASE_URL="你的_base_url_如果需要"

    # 可选: 为团队协调器和专家智能体指定不同的模型
    # 如果未设置这些变量，则代码会根据提供商设置默认值。
    # Groq 示例:
    # GROQ_TEAM_MODEL_ID="llama3-70b-8192"
    # GROQ_AGENT_MODEL_ID="llama3-8b-8192"
    # DeepSeek 示例:
    # DEEPSEEK_TEAM_MODEL_ID="deepseek-chat"  # 注意：不推荐使用 `deepseek-reasoner`，因为它不支持函数调用
    # DEEPSEEK_AGENT_MODEL_ID="deepseek-chat"  # 推荐用于专家智能体
    # OpenRouter 示例:
    # OPENROUTER_TEAM_MODEL_ID="deepseek/deepseek-r1"
    # OPENROUTER_AGENT_MODEL_ID="deepseek/deepseek-chat-v3-0324"

    # --- 外部工具 ---
    # 仅当研究员智能体被使用且需要 Exa 时才必需
    EXA_API_KEY="你的_exa_api_密钥"
    ```

    **关于模型选择的说明:**

    *   `TEAM_MODEL_ID` 由协调器（`Team` 对象本身）使用。该角色需要强大的推理、综合和委派能力。使用更强大的模型（如 `deepseek-r1`、`claude-3-opus` 或 `gpt-4-turbo`）通常更有益，即使它可能更慢或更昂贵。
    *   `AGENT_MODEL_ID` 由专家智能体（规划器、研究员等）使用。这些智能体处理更集中的子任务。您可以为专家选择更快或更具成本效益的模型（如 `deepseek-v3`、`claude-3-sonnet`、`llama3-70b`），具体取决于它们通常处理的任务复杂性以及您的预算/性能要求。
    *   `main.py` 中提供的默认值（例如，使用 DeepSeek 时的 `deepseek-chat`）是起点。鼓励进行实验，以找到适合您特定用例的最佳平衡点。

3.  **安装依赖：**

      * **使用 `uv` (推荐):**
        ```bash
        # 如果没有安装 uv，请先安装:
        # curl -LsSf https://astral.sh/uv/install.sh | sh
        # source $HOME/.cargo/env # 或者重启你的 shell

        uv pip install -r requirements.txt
        # 或者如果存在包含依赖的 pyproject.toml 文件:
        # uv pip install .
        ```
      * **使用 `pip`:**
        ```bash
        pip install -r requirements.txt
        # 或者如果存在包含依赖的 pyproject.toml 文件:
        # pip install .
        ```

## 使用方法

运行服务器脚本（假设主脚本名为 `main.py` 或基于您的文件结构命名的类似文件）：

```bash
python 你的主脚本名称.py
```

服务器将启动并通过 stdio 监听请求，使 `sequentialthinking` 工具可用于兼容的 MCP 客户端（如某些 LLM 或测试框架）。

### `sequentialthinking` 工具参数

该工具期望的参数与 `ThoughtData` Pydantic 模型匹配：

```python
# 简化表示
{
    "thought": str,              # 当前思考/步骤的内容
    "thoughtNumber": int,        # 序列号 (>=1)
    "totalThoughts": int,        # 预估总步骤数 (>=1, 建议 >=5)
    "nextThoughtNeeded": bool,   # 此步骤后是否需要另一步？
    "isRevision": bool = False,  # 这是否在修订之前的思考？
    "revisesThought": Optional[int] = None, # 如果是修订，修订哪个思考编号？
    "branchFromThought": Optional[int] = None, # 如果是分支，从哪个思考编号开始？
    "branchId": Optional[str] = None, # 分支的唯一 ID
    "needsMoreThoughts": bool = False # 在最后一步之前，如果预估过低则发出信号
}
```

### 与工具交互 (概念示例)

LLM 会迭代地与此工具交互：

1.  **LLM:** 使用 `sequential-thinking-starter` 提示和问题。
2.  **LLM:** 使用 `thoughtNumber: 1`、初始 `thought`（例如，"规划分析..."）、`totalThoughts` 预估、`nextThoughtNeeded: True` 调用 `sequentialthinking` 工具。
3.  **服务器:** MAS 处理思考 -\> 协调器综合响应并提供指导（例如，"分析计划完成。建议下一步研究 X。暂不推荐修订。"）。
4.  **LLM:** 接收包含 `coordinatorResponse` 的 JSON 响应。
5.  **LLM:** 根据 `coordinatorResponse` 构思下一个思考（例如，"使用 Exa 研究 X..."）。
6.  **LLM:** 使用 `thoughtNumber: 2`、新的 `thought`、更新的 `totalThoughts`（如果需要）、`