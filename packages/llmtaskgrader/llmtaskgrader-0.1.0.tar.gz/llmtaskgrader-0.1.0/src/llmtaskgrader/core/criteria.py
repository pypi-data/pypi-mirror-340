"""
评分标准定义
"""

# 定义评分标准
GRADING_CRITERIA = {
    "steps_count": "解决问题所需的步骤数量",
    "token_count": "处理问题所需的 token 数量",
    "tool_usage": "是否需要调用外部工具",
    "recheck_needed": "解决方案是否需要重新检查或多次迭代",
    "semantic_ambiguity": "问题陈述的模糊程度",
    "domain_knowledge": "所需的领域知识深度",
    "logical_complexity": "所需的逻辑推理复杂性",
    "computational_complexity": "数学计算或算法的复杂性",
    "problem_type": "问题类型（生成式、判别式等）",
    "data_dependency": "对外部数据源的依赖性",
    "multimodal_info": "是否涉及多种模态",
    "problem_scale": "问题规模（数据量）"
}

# 定义难度级别描述
DIFFICULTY_LEVELS = {
    "非常简单": "可以用最少的努力和基本知识解决的任务",
    "简单": "需要一些努力但仍然直接的任务",
    "中等": "具有中等复杂性，需要良好理解的任务",
    "困难": "需要深入理解和多个步骤的复杂任务",
    "非常困难": "极其复杂，挑战当前 LLM 能力极限的任务"
}

# 标准关键词
CRITERION_KEYWORDS = {
    "recheck_needed": ["验证", "检查", "确认", "验证", "确保", "复查"],
    "semantic_ambiguity": ["模糊", "不清楚", "含糊", "解释", "含义", "上下文"],
    "domain_knowledge": ["专业", "专家", "领域", "技术", "专业"],
    "logical_complexity": ["逻辑", "推理", "推断", "推导", "结论", "分析"],
    "computational_complexity": ["计算", "算法", "公式", "方程", "数学"],
    "problem_type": ["生成", "创建", "分类", "识别", "确定"],
    "data_dependency": ["数据", "源", "输入", "数据集", "数据库", "信息"],
    "multimodal_info": ["图像", "音频", "视频", "文本", "视觉", "声音", "多模态"],
    "problem_scale": ["大", "海量", "巨大", "广泛", "众多", "多个"]
}

# 工具使用关键词
TOOL_KEYWORDS = ["计算", "搜索", "查找", "数据库", "api", "获取", "检索", 
                "外部", "工具", "查询", "计算", "调用", "请求"]
