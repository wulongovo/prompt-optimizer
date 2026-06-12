"""评估器 - LLM-as-Judge"""
import json, re
from typing import List, Dict
from core.llm_client import generate

JUDGE_SYS = """你是Prompt质量评估专家。评分维度(每项1-10): accuracy, completeness, format, conciseness。
严格输出JSON: {"accuracy":N,"completeness":N,"format":N,"conciseness":N,"total":N,"feedback":"建议"}"""


class Evaluator:
    def evaluate_prompt(self, prompt: str, test_cases: List[Dict]) -> Dict:
        results, total = [], 0
        for case in test_cases:
            actual = generate(f"{prompt}\n\n输入: {case.get('input','')}", temperature=0.3)
            score = self._judge(prompt, case.get('input',''), case.get('expected',''), actual)
            results.append({"input": case.get('input',''), "expected": case.get('expected',''), "actual": actual, "score": score})
            total += score.get("total", 0)
        avg = round(total / len(test_cases), 1) if test_cases else 0
        return {"avg_score": avg, "max_score": 40, "test_cases": len(test_cases), "details": results,
                "feedback": " | ".join(set(r["score"].get("feedback","") for r in results if r["score"].get("feedback"))) or "暂无"}

    def _judge(self, prompt, inp, expected, actual):
        result = generate(f"评估Prompt效果:\nPrompt:{prompt[:500]}\n输入:{inp}\n期望:{expected}\n实际:{actual}\n\nJSON评分:", system=JUDGE_SYS, temperature=0.1)
        try:
            m = re.search(r'\{.*\}', result, re.DOTALL)
            if m:
                s = json.loads(m.group())
                s["total"] = sum(s.get(d,0) for d in ["accuracy","completeness","format","conciseness"])
                return s
        except: pass
        return {"accuracy":5,"completeness":5,"format":5,"conciseness":5,"total":20,"feedback":"评估解析失败"}

    def compare_prompts(self, prompts: List[Dict], test_cases: List[Dict]) -> List[Dict]:
        results = []
        for p in prompts:
            ev = self.evaluate_prompt(p["prompt"], test_cases)
            results.append({"strategy": p.get("strategy",""), "name": p.get("name",""), "prompt": p["prompt"][:200]+"...",
                           "avg_score": ev["avg_score"], "feedback": ev["feedback"]})
        results.sort(key=lambda x: x["avg_score"], reverse=True)
        for i, r in enumerate(results):
            r["rank"] = i + 1
        return results
