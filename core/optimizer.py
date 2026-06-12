"""优化器 - 协调生成、评估、迭代"""
import json, os, time
from typing import List, Dict
from core.prompt_generator import PromptGenerator
from core.evaluator import Evaluator

HISTORY_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "history.json")


class PromptOptimizer:
    def __init__(self):
        self.generator = PromptGenerator()
        self.evaluator = Evaluator()
        self.history = self._load_history()

    def _load_history(self):
        if os.path.exists(HISTORY_PATH):
            with open(HISTORY_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def _save_history(self):
        os.makedirs(os.path.dirname(HISTORY_PATH), exist_ok=True)
        with open(HISTORY_PATH, "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def optimize(self, task: str, test_cases: List[Dict], max_iter: int = 2) -> Dict:
        start = time.time()
        variants = self.generator.generate_variants(task, test_cases)
        ranking = self.evaluator.compare_prompts(variants, test_cases)

        if max_iter > 1:
            top3 = sorted(ranking, key=lambda x: x["avg_score"], reverse=True)[:3]
            for it in range(2, max_iter + 1):
                refined = [{"strategy": f"{r['strategy']}_r{it}", "name": f"{r['name']} (优化v{it})",
                           "prompt": self.generator.refine(r["prompt"], r.get("feedback",""))} for r in top3]
                new_ranking = self.evaluator.compare_prompts(refined, test_cases)
                ranking = sorted(ranking + new_ranking, key=lambda x: x["avg_score"], reverse=True)[:6]
                top3 = new_ranking[:3]

        best = max(ranking, key=lambda x: x["avg_score"]) if ranking else None
        result = {"task": task, "test_cases": len(test_cases), "iterations": max_iter,
                  "elapsed_seconds": round(time.time() - start, 1),
                  "ranking": sorted(ranking, key=lambda x: x["avg_score"], reverse=True), "best": best}

        self.history.append({"timestamp": time.strftime("%Y-%m-%d %H:%M:%S"), "task": task[:100],
                             "best_score": best["avg_score"] if best else 0,
                             "best_strategy": best["strategy"] if best else "", "iterations": max_iter})
        self._save_history()
        return result

    def get_history(self): return self.history

    def get_strategies(self):
        return [
            {"id":"zero_shot","name":"零样本","desc":"不提供示例，直接指令","best_for":"简单任务"},
            {"id":"few_shot","name":"少样本","desc":"提供输入输出示例","best_for":"格式敏感任务"},
            {"id":"chain_of_thought","name":"思维链","desc":"引导分步推理","best_for":"逻辑推理任务"},
            {"id":"role_based","name":"角色扮演","desc":"赋予专家角色","best_for":"专业领域任务"},
            {"id":"structured","name":"结构化输出","desc":"要求JSON/Markdown格式","best_for":"数据提取任务"},
            {"id":"combined","name":"组合优化","desc":"综合多种策略","best_for":"复杂任务"},
        ]
