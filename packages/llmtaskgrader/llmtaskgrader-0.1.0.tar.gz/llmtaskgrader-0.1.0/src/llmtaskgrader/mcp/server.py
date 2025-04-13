"""
MCP服务器实现
"""

import os
import sys
import json
import asyncio
import importlib.util
import logging
from typing import Dict, List, Optional, Any, Callable
from pathlib import Path

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MCPServer:
    """MCP服务器类"""
    
    def __init__(self, name: str, description: str = "", version: str = "1.0.0"):
        self.name = name
        self.description = description
        self.version = version
        self.tools = {}
        self.resources = {}
    
    def register_tool(self, name: str, func: Callable, description: str, parameters: Dict = None, returns: Dict = None):
        """注册工具"""
        self.tools[name] = {
            "func": func,
            "description": description,
            "parameters": parameters or {},
            "returns": returns or {}
        }
    
    def register_resource(self, uri: str, func: Callable, description: str):
        """注册资源"""
        self.resources[uri] = {
            "func": func,
            "description": description
        }
    
    async def handle_request(self, request_json: str) -> str:
        """处理MCP请求"""
        try:
            request = json.loads(request_json)
            
            if request["type"] == "ping":
                return json.dumps({"type": "pong"})
            
            elif request["type"] == "list_tools":
                tools_list = []
                for name, tool in self.tools.items():
                    tools_list.append({
                        "name": name,
                        "description": tool["description"],
                        "parameters": tool["parameters"],
                        "returns": tool["returns"]
                    })
                return json.dumps({
                    "type": "tools",
                    "tools": tools_list
                })
            
            elif request["type"] == "list_resources":
                resources_list = []
                for uri, resource in self.resources.items():
                    resources_list.append({
                        "uri": uri,
                        "description": resource["description"]
                    })
                return json.dumps({
                    "type": "resources",
                    "resources": resources_list
                })
            
            elif request["type"] == "call_tool":
                tool_name = request["name"]
                parameters = request["parameters"]
                
                if tool_name not in self.tools:
                    return json.dumps({
                        "type": "error",
                        "error": f"未知工具: {tool_name}"
                    })
                
                try:
                    # 调用工具函数
                    result = await self.tools[tool_name]["func"](**parameters)
                    
                    # 处理结果
                    if hasattr(result, "to_dict"):
                        result_dict = result.to_dict()
                    else:
                        result_dict = result
                    
                    return json.dumps({
                        "type": "tool_result",
                        "request_id": request.get("request_id", ""),
                        "content": [
                            {
                                "type": "text",
                                "text": result_dict
                            }
                        ]
                    }, ensure_ascii=False)
                
                except Exception as e:
                    logger.error(f"调用工具 {tool_name} 时出错: {str(e)}")
                    return json.dumps({
                        "type": "error",
                        "error": f"调用工具时出错: {str(e)}"
                    })
            
            elif request["type"] == "read_resource":
                uri = request["uri"]
                
                if uri not in self.resources:
                    return json.dumps({
                        "type": "error",
                        "error": f"未知资源: {uri}"
                    })
                
                try:
                    # 调用资源函数
                    result = self.resources[uri]["func"]()
                    
                    return json.dumps({
                        "type": "resource_content",
                        "request_id": request.get("request_id", ""),
                        "content": [
                            {
                                "type": "text",
                                "text": result
                            }
                        ]
                    }, ensure_ascii=False)
                
                except Exception as e:
                    logger.error(f"读取资源 {uri} 时出错: {str(e)}")
                    return json.dumps({
                        "type": "error",
                        "error": f"读取资源时出错: {str(e)}"
                    })
            
            else:
                return json.dumps({
                    "type": "error",
                    "error": f"未知请求类型: {request['type']}"
                })
        
        except json.JSONDecodeError:
            return json.dumps({
                "type": "error",
                "error": "无效的JSON请求"
            })
        
        except Exception as e:
            logger.error(f"处理请求时出错: {str(e)}")
            return json.dumps({
                "type": "error",
                "error": f"处理请求时出错: {str(e)}"
            })
    
    async def start_stdio(self):
        """通过标准输入输出启动服务器"""
        # 发送服务器信息
        print(json.dumps({
            "type": "server_info",
            "name": self.name,
            "description": self.description,
            "version": self.version
        }, ensure_ascii=False), flush=True)
        
        # 处理请求
        while True:
            try:
                # 从标准输入读取请求
                request_json = input()
                
                # 处理请求
                response_json = await self.handle_request(request_json)
                
                # 发送响应
                print(response_json, flush=True)
            
            except EOFError:
                # 输入结束，退出
                break
            
            except Exception as e:
                # 处理错误
                error_response = json.dumps({
                    "type": "error",
                    "error": str(e)
                }, ensure_ascii=False)
                print(error_response, flush=True)
    
    async def start_sse(self, host: str = "127.0.0.1", port: int = 8000):
        """通过SSE启动服务器"""
        # 这里需要实现SSE服务器
        # 由于实现较为复杂，这里只提供一个简单的占位符
        logger.info(f"SSE服务器启动在 {host}:{port}")
        logger.warning("SSE服务器尚未实现")
    
    async def start_ws(self, host: str = "127.0.0.1", port: int = 8000):
        """通过WebSocket启动服务器"""
        # 这里需要实现WebSocket服务器
        # 由于实现较为复杂，这里只提供一个简单的占位符
        logger.info(f"WebSocket服务器启动在 {host}:{port}")
        logger.warning("WebSocket服务器尚未实现")

def load_mcp_module(file_path: str):
    """加载MCP模块"""
    try:
        # 获取绝对路径
        abs_path = Path(file_path).resolve()
        
        # 加载模块
        spec = importlib.util.spec_from_file_location("mcp_module", abs_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        return module
    except Exception as e:
        logger.error(f"加载MCP模块时出错: {str(e)}")
        raise

def create_default_server():
    """创建默认服务器"""
    from ..core.criteria import GRADING_CRITERIA, DIFFICULTY_LEVELS
    from ..core.grader import grade_task, grade_task_criterion
    from ..llm.bailian import grade_task_bailian
    
    # 创建服务器
    server = MCPServer(
        name="LLM任务评分器",
        description="用于评估LLM应用任务难度的服务",
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
    
    return server

async def start_mcp_server(file_path: Optional[str] = None, host: str = "127.0.0.1", port: int = 8000, transport: str = "stdio"):
    """启动MCP服务器"""
    try:
        if file_path:
            # 加载用户提供的MCP模块
            module = load_mcp_module(file_path)
            
            # 检查模块是否有server属性
            if hasattr(module, "server") and isinstance(module.server, MCPServer):
                server = module.server
            else:
                logger.warning(f"模块 {file_path} 没有有效的server属性，使用默认服务器")
                server = create_default_server()
        else:
            # 使用默认服务器
            server = create_default_server()
        
        # 根据传输协议启动服务器
        if transport == "stdio":
            await server.start_stdio()
        elif transport == "sse":
            await server.start_sse(host, port)
        elif transport == "ws":
            await server.start_ws(host, port)
        else:
            logger.error(f"不支持的传输协议: {transport}")
            sys.exit(1)
    
    except Exception as e:
        logger.error(f"启动MCP服务器时出错: {str(e)}")
        sys.exit(1)

def main():
    """命令行入口点"""
    import argparse
    
    parser = argparse.ArgumentParser(description="启动MCP服务器")
    parser.add_argument("--file", help="MCP服务文件路径")
    parser.add_argument("--host", default="127.0.0.1", help="服务器主机")
    parser.add_argument("--port", type=int, default=8000, help="服务器端口")
    parser.add_argument("--transport", choices=["stdio", "sse", "ws"], default="stdio", help="传输协议")
    
    args = parser.parse_args()
    
    asyncio.run(start_mcp_server(args.file, args.host, args.port, args.transport))

if __name__ == "__main__":
    main()
