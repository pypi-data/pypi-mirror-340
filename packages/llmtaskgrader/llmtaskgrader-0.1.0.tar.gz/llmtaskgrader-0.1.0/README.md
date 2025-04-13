# LLM任务评分器

LLM任务评分器是一个用于评估大型语言模型（LLM）应用任务难度的工具，支持使用百炼、OpenRouter和Gemini等大模型进行前置难度评估。

## 功能特点

- 基于多种标准对LLM任务进行全面评估
- 支持使用百炼、OpenRouter和Gemini等大模型进行前置难度评估
- 提供MCP服务，可以像uvx那样轻松启动
- 支持命令行界面，方便使用

## 安装

```bash
pip install llmtaskgrader
```

## 使用方法

### 命令行使用

```bash
# 评估任务难度
llmtaskgrader grade "实现一个分布式一致性算法" --provider bailian

# 启动MCP服务
llmtaskgrader serve --transport sse --port 8080

# 使用简化命令
llmtg serve my_mcp_service.py --transport sse
```

### 作为Python库使用

```python
from llmtaskgrader.core.grader import grade_task
from llmtaskgrader.llm.bailian import grade_task_bailian

# 基于规则的评估
result = grade_task("实现一个分布式一致性算法")
print(f"难度: {result.overall_difficulty}")
print(f"分数: {result.overall_score}")

# 使用百炼进行评估
result = grade_task_bailian("实现一个分布式一致性算法")
print(f"难度: {result.overall_difficulty}")
print(f"分数: {result.overall_score}")
```

## API密钥配置

如果您想使用大模型进行前置难度评估，需要设置以下环境变量之一：

- `BAILIAN_API_KEY`：阿里云百炼API密钥
- `OPENROUTER_API_KEY`：OpenRouter API密钥
- `GEMINI_API_KEY`：Google Gemini API密钥

## 许可证

本项目采用MIT许可证。
