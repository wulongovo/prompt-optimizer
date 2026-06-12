"""Prompt生成器 - 生成多种策略的Prompt变体"""
from typing import List, Dict
from core.llm_client import generate

STRATEGIES = {
    "zero_shot": "零样本", "few_shot": "少样本",
    "chain_of_thought": "思维链", "role_based": "角色扮演",
    "structured": "结构化输出", "combined": "组合优化"
}

GEN_SYS = "你是Prompt Engineering专家。根据任务描述生成高质量Prompt。直接输出Prompt内容，不要加解释。"
REFINE_SYS = "你是Prompt优化专家。根据反馈改进Prompt。直接输出改进后的Prompt。"


class PromptGenerator:
    def generate_variants(self, task: str, test_cases: List[Dict] = None) -> List[Dict]:
        variants = [
            {"strategy": "zero_shot", "name": "零样本 (Zero-shot)", "prompt": self._gen(task, "零样本")},
            {"strategy": "chain_of_thought", "name": "思维链 (CoT)", "prompt": self._gen(task, "思维链，引导分步推理")},
            {"strategy": "role_based", "name": "角色扮演 (Role-based)", "prompt": self._gen(task, "角色扮演，赋予专家角色")},
            {"strategy": "structured", "name": "结构化输出 (Structured)", "prompt": self._gen(task, "结构化输出，要求JSON格式")},
            {"strategy": "combined", "name": "组合优化 (Combined)", "prompt": self._gen(task, "综合多种策略")},
        ]
        if test_cases:
            ex = "\n".join([f"输入:{e.get('input','')} → 期望:{e.get('expected','')}" for e in test_cases[:3]])
            variants.insert(1, {"strategy": "few_shot", "name": "少样本 (Few-shot)",
                               "prompt": generate(f"为以下任务生成带示例的Few-shot Prompt：\n任务：{task}\n\n示例：\n{ex}", system=GEN_SYS, temperature=0.5)})
        return variants

    def _gen(self, task, strategy_desc):
        return generate(f"用{strategy_desc}策略，为以下任务生成Prompt：\n{task}", system=GEN_SYS, temperature=0.5)

    def refine(self, prompt, feedback):
        return generate(f"现有Prompt：\n{prompt}\n\n反馈：\n{feedback}\n\n生成改进版本：", system=REFINE_SYS, temperature=0.5)
