"""
环境变量处理
"""

import os
import sys
import json
import asyncio
import subprocess
from typing import Dict, Any, Optional
from rich.console import Console

console = Console()

def set_api_keys(bailian_key: Optional[str] = None, openrouter_key: Optional[str] = None, gemini_key: Optional[str] = None):
    """设置API密钥环境变量"""
    if bailian_key:
        os.environ["BAILIAN_API_KEY"] = bailian_key
        console.print("[green]已设置百炼API密钥[/green]")
    
    if openrouter_key:
        os.environ["OPENROUTER_API_KEY"] = openrouter_key
        console.print("[green]已设置OpenRouter API密钥[/green]")
    
    if gemini_key:
        os.environ["GEMINI_API_KEY"] = gemini_key
        console.print("[green]已设置Gemini API密钥[/green]")

async def test_environment():
    """测试环境配置"""
    console.print("[bold]===== LLM任务评分器环境测试 =====\n[/bold]")
    
    # 测试环境变量
    console.print("[bold]测试环境变量...[/bold]")
    
    env_vars = {
        "BAILIAN_API_KEY": os.environ.get("BAILIAN_API_KEY"),
        "OPENROUTER_API_KEY": os.environ.get("OPENROUTER_API_KEY"),
        "GEMINI_API_KEY": os.environ.get("GEMINI_API_KEY")
    }
    
    for var_name, var_value in env_vars.items():
        if var_value:
            console.print(f"[green]✓ {var_name} 已设置[/green]")
        else:
            console.print(f"[yellow]✗ {var_name} 未设置[/yellow]")
    
    console.print()
    
    # 测试依赖项
    console.print("[bold]测试Python依赖项...[/bold]")
    
    dependencies = ["httpx", "asyncio", "json", "rich", "click"]
    
    for dep in dependencies:
        try:
            __import__(dep)
            console.print(f"[green]✓ {dep} 已安装[/green]")
        except ImportError:
            console.print(f"[red]✗ {dep} 未安装[/red]")
    
    console.print()
    
    # 测试基于规则的评分功能
    console.print("[bold]测试基于规则的评分功能...[/bold]")
    
    try:
        from ..core.grader import grade_task
        
        task = {
            "description": "用Python编写一个简单的'Hello, World!'程序。",
            "context": "这是为初学者编程课程准备的。"
        }
        
        result = grade_task(task["description"], task["context"])
        
        console.print(f"[green]✓ 基于规则的评分成功[/green]")
        console.print(f"  - 任务: {task['description']}")
        console.print(f"  - 难度: {result.overall_difficulty}")
        console.print(f"  - 分数: {result.overall_score:.2f}/5.0")
    except Exception as e:
        console.print(f"[red]✗ 基于规则的评分测试失败: {str(e)}[/red]")
    
    console.print()
    
    # 测试MCP服务
    console.print("[bold]测试MCP服务启动...[/bold]")
    
    try:
        from ..mcp.server import create_default_server
        
        server = create_default_server()
        console.print(f"[green]✓ MCP服务创建成功: {server.name} (版本 {server.version})[/green]")
        console.print(f"  - 工具数量: {len(server.tools)}")
        console.print(f"  - 资源数量: {len(server.resources)}")
    except Exception as e:
        console.print(f"[red]✗ MCP服务测试失败: {str(e)}[/red]")
    
    console.print()
    
    # 测试大模型评分功能（如果有API密钥）
    if any(env_vars.values()):
        console.print("[bold]测试大模型评分功能...[/bold]")
        
        if os.environ.get("BAILIAN_API_KEY"):
            try:
                from ..llm.bailian import grade_task_bailian
                
                task = {
                    "description": "用Python编写一个简单的'Hello, World!'程序。",
                    "context": "这是为初学者编程课程准备的。"
                }
                
                console.print("使用百炼API进行评分测试...")
                console.print("[yellow]注意: 这将调用实际的API，可能会产生费用[/yellow]")
                console.print("按Enter继续，或Ctrl+C取消")
                input()
                
                result = grade_task_bailian(task["description"], task["context"])
                
                console.print(f"[green]✓ 使用百炼的评分成功[/green]")
                console.print(f"  - 任务: {task['description']}")
                console.print(f"  - 难度: {result.overall_difficulty}")
                console.print(f"  - 分数: {result.overall_score:.2f}/5.0")
            except Exception as e:
                console.print(f"[red]✗ 使用百炼的评分失败: {str(e)}[/red]")
        else:
            console.print("[yellow]⚠ 未设置百炼API密钥，跳过百炼评分测试[/yellow]")
    else:
        console.print("[yellow]⚠ 未设置任何API密钥，跳过大模型评分测试[/yellow]")
    
    console.print()
    console.print("[bold]===== 测试完成 =====\n[/bold]")

if __name__ == "__main__":
    asyncio.run(test_environment())
