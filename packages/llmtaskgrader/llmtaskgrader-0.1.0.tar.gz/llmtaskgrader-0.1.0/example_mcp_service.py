"""
示例MCP服务

这是一个使用llmtaskgrader包创建的示例MCP服务。
"""

from llmtaskgrader.mcp.server import MCPServer
from llmtaskgrader.core.grader import grade_task, grade_task_criterion
from llmtaskgrader.llm.bailian import grade_task_bailian
from llmtaskgrader.core.criteria import GRADING_CRITERIA, DIFFICULTY_LEVELS

# 创建MCP服务器
server = MCPServer(
    name="示例任务评分服务",
    description="用于评估LLM应用任务难度的示例服务",
    version="0.1.0"
)

# 注册工具
server.register_tool(
    name="grade_task",
    func=lambda task_description, task_context=None: grade_task(task_description, task_context),
    description="基于多个标准对LLM任务进行评分，并提供整体难度评估。",
    parameters={
        "type": "object",
        "properties": {
            "task_description": {
                "type": "string",
                "description": "要评分的任务描述"
            },
            "task_context": {
                "type": "string",
                "description": "关于任务的额外上下文"
            }
        },
        "required": ["task_description"]
    },
    returns={
        "type": "object",
        "description": "包含整体难度和每个标准分数的评分结果"
    }
)

server.register_tool(
    name="grade_task_criterion",
    func=lambda task_description, criterion, task_context=None: grade_task_criterion(task_description, criterion, task_context),
    description="对LLM任务的特定标准进行评分。",
    parameters={
        "type": "object",
        "properties": {
            "task_description": {
                "type": "string",
                "description": "要评分的任务描述"
            },
            "criterion": {
                "type": "string",
                "description": "要评估的特定标准"
            },
            "task_context": {
                "type": "string",
                "description": "关于任务的额外上下文"
            }
        },
        "required": ["task_description", "criterion"]
    },
    returns={
        "type": "object",
        "description": "指定标准的分数和理由"
    }
)

server.register_tool(
    name="grade_task_bailian",
    func=lambda task_description, task_context=None: grade_task_bailian(task_description, task_context),
    description="使用百炼API对LLM任务进行前置难度评估。",
    parameters={
        "type": "object",
        "properties": {
            "task_description": {
                "type": "string",
                "description": "要评分的任务描述"
            },
            "task_context": {
                "type": "string",
                "description": "关于任务的额外上下文"
            }
        },
        "required": ["task_description"]
    },
    returns={
        "type": "object",
        "description": "包含整体难度和每个标准分数的评分结果"
    }
)

# 注册资源
server.register_resource(
    uri="grading://criteria",
    func=lambda: GRADING_CRITERIA,
    description="返回用于评分LLM任务的标准"
)

server.register_resource(
    uri="grading://difficulty-levels",
    func=lambda: DIFFICULTY_LEVELS,
    description="返回可用的难度级别及其描述"
)

server.register_resource(
    uri="grading://llm-providers",
    func=lambda: {
        "bailian": "阿里云百炼大模型",
        "openrouter": "OpenRouter API (支持多种模型)",
        "gemini": "Google Gemini"
    },
    description="返回可用的大模型提供商"
)

# 如果直接运行此文件，启动MCP服务
if __name__ == "__main__":
    import asyncio
    from llmtaskgrader.mcp.server import start_mcp_server
    
    asyncio.run(start_mcp_server())
