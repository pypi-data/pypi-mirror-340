"""
CLI命令定义
"""

import os
import sys
import asyncio
import click
from rich.console import Console
from rich.table import Table

from ..core.grader import grade_task, grade_task_criterion
from ..llm.bailian import grade_task_bailian
from ..mcp.server import start_mcp_server
from ..utils.env import test_environment

console = Console()

@click.group()
def main():
    """LLM任务难度评分工具，支持百炼、OpenRouter和Gemini等大模型"""
    pass

@main.command()
@click.argument("task_description")
@click.option("--context", "-c", help="任务上下文")
@click.option("--provider", "-p", type=click.Choice(["rule", "bailian"]), 
              default="rule", help="评分提供商")
def grade(task_description, context, provider):
    """评估任务难度"""
    console.print(f"[bold]评估任务:[/bold] {task_description}")
    
    if provider == "rule":
        result = grade_task(task_description, context)
    elif provider == "bailian":
        result = grade_task_bailian(task_description, context)
    
    # 显示结果
    console.print(f"[bold green]整体难度:[/bold green] {result.overall_difficulty}")
    console.print(f"[bold green]整体分数:[/bold green] {result.overall_score:.2f}/5.0")
    
    # 创建表格显示各标准分数
    table = Table(title="评分详情")
    table.add_column("标准", style="cyan")
    table.add_column("分数", justify="right", style="green")
    table.add_column("理由", style="yellow")
    
    for criterion, score in result.criteria_scores.items():
        table.add_row(criterion, f"{score.score:.1f}", score.justification)
    
    console.print(table)
    console.print(f"[bold]摘要:[/bold] {result.summary}")

@main.command()
@click.option("--file", "-f", help="MCP服务文件路径")
@click.option("--host", default="127.0.0.1", help="服务器主机")
@click.option("--port", default=8000, help="服务器端口")
@click.option("--transport", type=click.Choice(["stdio", "sse", "ws"]), 
              default="stdio", help="传输协议")
def serve(file, host, port, transport):
    """启动MCP服务器"""
    console.print(f"[bold]启动MCP服务器[/bold] (传输协议: {transport})")
    asyncio.run(start_mcp_server(file, host, port, transport))

@main.command()
def test():
    """测试环境配置"""
    asyncio.run(test_environment())

if __name__ == "__main__":
    main()
