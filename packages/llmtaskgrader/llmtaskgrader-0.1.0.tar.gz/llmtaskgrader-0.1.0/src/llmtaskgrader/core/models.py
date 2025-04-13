"""
数据模型定义
"""

from enum import Enum
from typing import Dict, Optional
import json

class DifficultyLevel(str, Enum):
    """难度级别枚举"""
    VERY_EASY = "非常简单"
    EASY = "简单"
    MEDIUM = "中等"
    HARD = "困难"
    VERY_HARD = "非常困难"

class CriterionScore:
    """标准评分"""
    def __init__(self, score: float, justification: str):
        self.score = score
        self.justification = justification
    
    def to_dict(self):
        return {
            "score": self.score,
            "justification": self.justification
        }

class TaskGradingResult:
    """任务评分结果"""
    def __init__(self, overall_difficulty: DifficultyLevel, overall_score: float, 
                 criteria_scores: Dict[str, CriterionScore], summary: str):
        self.overall_difficulty = overall_difficulty
        self.overall_score = overall_score
        self.criteria_scores = criteria_scores
        self.summary = summary
    
    def to_dict(self):
        return {
            "overall_difficulty": self.overall_difficulty,
            "overall_score": self.overall_score,
            "criteria_scores": {k: v.to_dict() for k, v in self.criteria_scores.items()},
            "summary": self.summary
        }
    
    def to_json(self):
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)
