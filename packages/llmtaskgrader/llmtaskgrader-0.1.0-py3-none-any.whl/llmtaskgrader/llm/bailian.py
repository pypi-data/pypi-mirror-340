"""
百炼API集成
"""

import os
import json
import asyncio
import logging
from typing import Dict, Optional

import httpx

from ..core.models import TaskGradingResult
from ..core.grader import grade_task
from .prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE

# 配置日志
logger = logging.getLogger(__name__)

# 百炼API配置 (DashScope)
BAILIAN_API_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
BAILIAN_API_KEY = os.environ.get("BAILIAN_API_KEY", "")

async def call_bailian_api(prompt: str) -> str:
    """
    调用百炼API进行任务难度评估
    
    参数:
        prompt: 发送给模型的提示词
        
    返回:
        模型的响应
    """
    if not BAILIAN_API_KEY:
        raise ValueError("百炼API密钥未设置。请设置BAILIAN_API_KEY环境变量。")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {BAILIAN_API_KEY}"
    }
    
    # DashScope API请求格式
    data = {
        "model": "qwen-max",
        "input": {
            "prompt": prompt,
            "system": SYSTEM_PROMPT
        },
        "parameters": {
            "temperature": 0.2,
            "top_p": 0.8,
            "result_format": "text"
        }
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(BAILIAN_API_URL, json=data, headers=headers)
            response.raise_for_status()
            result = response.json()
            # DashScope API响应格式
            return result["output"]["text"]
        except Exception as e:
            logger.error(f"调用百炼API时出错: {str(e)}")
            raise

async def grade_task_bailian_async(task_description: str, task_context: Optional[str] = None) -> TaskGradingResult:
    """
    使用百炼API对LLM任务进行前置难度评估（异步版本）
    
    参数:
        task_description: 要评估的任务描述
        task_context: 任务上下文（可选）
        
    返回:
        包含评估结果的TaskGradingResult对象
    """
    # 准备提示词
    prompt = USER_PROMPT_TEMPLATE.format(
        task_description=task_description,
        task_context=task_context or "无"
    )
    
    try:
        # 调用百炼API
        response_text = await call_bailian_api(prompt)
        
        # 解析JSON响应
        # 尝试提取JSON部分（以防模型返回了额外的文本）
        try:
            # 尝试直接解析整个响应
            result = json.loads(response_text)
        except json.JSONDecodeError:
            # 如果失败，尝试从响应中提取JSON部分
            import re
            json_match = re.search(r'```json\s*([\s\S]*?)\s*```', response_text)
            if json_match:
                result = json.loads(json_match.group(1))
            else:
                # 如果仍然失败，尝试查找任何看起来像JSON的部分
                json_match = re.search(r'({[\s\S]*})', response_text)
                if json_match:
                    result = json.loads(json_match.group(1))
                else:
                    raise ValueError("无法从模型响应中提取JSON数据")
        
        # 处理结果并返回TaskGradingResult对象
        from ..core.criteria import GRADING_CRITERIA
        from ..core.models import CriterionScore
        from ..core.grader import determine_difficulty_level, generate_grading_summary
        
        # 提取评分和理由
        criteria_scores = {}
        for criterion in GRADING_CRITERIA.keys():
            if criterion in result:
                score = float(result[criterion]["score"])
                justification = result[criterion]["justification"]
                criteria_scores[criterion] = CriterionScore(score=score, justification=justification)
        
        # 如果模型没有返回某些标准的评分，使用默认值
        for criterion in GRADING_CRITERIA.keys():
            if criterion not in criteria_scores:
                criteria_scores[criterion] = CriterionScore(
                    score=1.0,
                    justification=f"模型未提供{criterion}的评分，使用默认值。"
                )
        
        # 计算整体分数
        overall_score = sum(score.score for score in criteria_scores.values()) / len(criteria_scores)
        
        # 确定难度级别
        difficulty_level = determine_difficulty_level(overall_score)
        
        # 生成摘要
        summary = generate_grading_summary(task_description, overall_score, difficulty_level, criteria_scores)
        
        return TaskGradingResult(
            overall_difficulty=difficulty_level,
            overall_score=overall_score,
            criteria_scores=criteria_scores,
            summary=summary
        )
    
    except Exception as e:
        logger.error(f"使用百炼评估任务时出错: {str(e)}")
        # 如果API调用失败，回退到基于规则的评估
        logger.info("回退到基于规则的评估方法")
        return grade_task(task_description, task_context)

def grade_task_bailian(task_description: str, task_context: Optional[str] = None) -> TaskGradingResult:
    """
    使用百炼API对LLM任务进行前置难度评估（同步版本）
    
    参数:
        task_description: 要评估的任务描述
        task_context: 任务上下文（可选）
        
    返回:
        包含评估结果的TaskGradingResult对象
    """
    return asyncio.run(grade_task_bailian_async(task_description, task_context))
