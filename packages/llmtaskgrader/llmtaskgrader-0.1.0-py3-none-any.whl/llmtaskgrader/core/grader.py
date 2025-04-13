"""
基于规则的评分逻辑
"""

from typing import Dict, Optional

from .models import CriterionScore, TaskGradingResult, DifficultyLevel
from .criteria import GRADING_CRITERIA, CRITERION_KEYWORDS, TOOL_KEYWORDS

def evaluate_steps_count(task_description: str) -> CriterionScore:
    """评估解决任务所需的步骤数量"""
    # 简单启发式：计算句子数量并估计复杂性
    sentences = task_description.split('.')
    num_sentences = len([s for s in sentences if s.strip()])
    
    if num_sentences <= 2:
        score = 1.0
        justification = "根据其简短描述，任务似乎只需要很少的步骤。"
    elif num_sentences <= 5:
        score = 2.0
        justification = "任务可能需要几个简单的步骤。"
    elif num_sentences <= 10:
        score = 3.0
        justification = "任务涉及中等数量的步骤。"
    elif num_sentences <= 15:
        score = 4.0
        justification = "任务涉及许多步骤，看起来很复杂。"
    else:
        score = 5.0
        justification = "任务涉及大量步骤，非常复杂。"
    
    return CriterionScore(score=score, justification=justification)

def evaluate_token_count(task_description: str) -> CriterionScore:
    """评估处理任务所需的 token 数量"""
    # 简单近似：英文中 1 个 token ≈ 4 个字符
    char_count = len(task_description)
    token_estimate = char_count / 4
    
    if token_estimate < 50:
        score = 1.0
        justification = "token 数量很少，需要最少的处理。"
    elif token_estimate < 200:
        score = 2.0
        justification = "token 数量较少，需要有限的处理。"
    elif token_estimate < 500:
        score = 3.0
        justification = "token 数量中等，需要一般的处理。"
    elif token_estimate < 1000:
        score = 4.0
        justification = "token 数量较大，需要大量处理。"
    else:
        score = 5.0
        justification = "token 数量非常大，需要大量处理。"
    
    return CriterionScore(score=score, justification=justification)

def evaluate_tool_usage(task_description: str) -> CriterionScore:
    """评估任务是否需要外部工具"""
    # 寻找暗示工具使用的关键词
    matches = sum(1 for keyword in TOOL_KEYWORDS if keyword.lower() in task_description.lower())
    
    if matches == 0:
        score = 1.0
        justification = "没有迹象表明需要外部工具。"
    elif matches <= 2:
        score = 2.0
        justification = "略微迹象表明简单工具可能有帮助。"
    elif matches <= 4:
        score = 3.0
        justification = "中等迹象表明需要工具。"
    elif matches <= 6:
        score = 4.0
        justification = "强烈迹象表明需要多种工具。"
    else:
        score = 5.0
        justification = "非常强烈的迹象表明复杂工具使用是必不可少的。"
    
    return CriterionScore(score=score, justification=justification)

def evaluate_generic_criterion(criterion: str, task_description: str) -> CriterionScore:
    """其他标准的通用评估"""
    # 这是一个简化的占位符。在实际实现中，
    # 每个标准都应该有自己的专门评估逻辑。
    
    # 为了演示，我们将使用一个简单的基于关键词的方法
    keywords = CRITERION_KEYWORDS.get(criterion, [])
    matches = sum(1 for keyword in keywords if keyword.lower() in task_description.lower())
    
    if matches == 0:
        score = 1.0
        justification = f"没有迹象表明 {criterion} 的复杂性。"
    elif matches == 1:
        score = 2.0
        justification = f"略微迹象表明 {criterion} 的复杂性。"
    elif matches == 2:
        score = 3.0
        justification = f"中等迹象表明 {criterion} 的复杂性。"
    elif matches == 3:
        score = 4.0
        justification = f"高度迹象表明 {criterion} 的复杂性。"
    else:
        score = 5.0
        justification = f"非常高的迹象表明 {criterion} 的复杂性。"
    
    return CriterionScore(score=score, justification=justification)

def determine_difficulty_level(overall_score: float) -> DifficultyLevel:
    """将数值分数转换为难度级别"""
    if overall_score < 1.5:
        return DifficultyLevel.VERY_EASY
    elif overall_score < 2.5:
        return DifficultyLevel.EASY
    elif overall_score < 3.5:
        return DifficultyLevel.MEDIUM
    elif overall_score < 4.5:
        return DifficultyLevel.HARD
    else:
        return DifficultyLevel.VERY_HARD

def generate_grading_summary(
    task_description: str, 
    overall_score: float, 
    difficulty_level: DifficultyLevel, 
    criteria_scores: Dict[str, CriterionScore]
) -> str:
    """生成评分结果摘要"""
    # 找出得分最高和最低的标准
    highest_criterion = max(criteria_scores.items(), key=lambda x: x[1].score)
    lowest_criterion = min(criteria_scores.items(), key=lambda x: x[1].score)
    
    summary = f"任务 '{task_description[:50]}...' 的整体难度评分为 {overall_score:.2f}，"
    summary += f"难度级别为 '{difficulty_level}'。\n\n"
    summary += f"最具挑战性的方面是 '{highest_criterion[0]}' (分数: {highest_criterion[1].score})，"
    summary += f"因为{highest_criterion[1].justification}\n\n"
    summary += f"最不具挑战性的方面是 '{lowest_criterion[0]}' (分数: {lowest_criterion[1].score})，"
    summary += f"因为{lowest_criterion[1].justification}"
    
    return summary

def grade_task(task_description: str, task_context: Optional[str] = None) -> TaskGradingResult:
    """
    基于多个标准对 LLM 任务进行评分，并提供整体难度评估。
    
    参数:
        task_description: 要评分的任务描述
        task_context: 关于任务的额外上下文（可选）
        
    返回:
        包含评分结果的 TaskGradingResult 对象
    """
    # 初始化分数字典
    criteria_scores = {}
    
    # 评估每个标准
    # 步骤数量评估
    criteria_scores["steps_count"] = evaluate_steps_count(task_description)
    
    # Token 数量评估
    criteria_scores["token_count"] = evaluate_token_count(task_description)
    
    # 工具使用评估
    criteria_scores["tool_usage"] = evaluate_tool_usage(task_description)
    
    # 评估剩余标准
    for criterion in list(GRADING_CRITERIA.keys())[3:]:
        criteria_scores[criterion] = evaluate_generic_criterion(criterion, task_description)
    
    # 计算整体分数（所有标准的平均值）
    overall_score = sum(score.score for score in criteria_scores.values()) / len(criteria_scores)
    
    # 确定整体难度级别
    difficulty_level = determine_difficulty_level(overall_score)
    
    # 生成摘要
    summary = generate_grading_summary(task_description, overall_score, difficulty_level, criteria_scores)
    
    return TaskGradingResult(
        overall_difficulty=difficulty_level,
        overall_score=overall_score,
        criteria_scores=criteria_scores,
        summary=summary
    )

def grade_task_criterion(task_description: str, criterion: str, task_context: Optional[str] = None) -> CriterionScore:
    """
    对 LLM 任务的特定标准进行评分。
    
    参数:
        task_description: 要评分的任务描述
        criterion: 要评估的特定标准
        task_context: 关于任务的额外上下文（可选）
        
    返回:
        包含分数和理由的 CriterionScore 对象
    """
    if criterion not in GRADING_CRITERIA:
        raise ValueError(f"未知标准: {criterion}。可用标准: {list(GRADING_CRITERIA.keys())}")
    
    # 评估特定标准
    if criterion == "steps_count":
        return evaluate_steps_count(task_description)
    elif criterion == "token_count":
        return evaluate_token_count(task_description)
    elif criterion == "tool_usage":
        return evaluate_tool_usage(task_description)
    else:
        return evaluate_generic_criterion(criterion, task_description)
