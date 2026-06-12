#!/usr/bin/env python3
"""Prompt优化器 - 主入口"""
import argparse, sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
from core.optimizer import PromptOptimizer

def main():
    parser = argparse.ArgumentParser(description="Prompt优化器")
    sub = parser.add_subparsers(dest="cmd")

    p = sub.add_parser("optimize", help="优化Prompt")
    p.add_argument("--task", "-t", required=True)
    p.add_argument("--cases", "-c", help="测试用例JSON文件")
    p.add_argument("--iter", type=int, default=2)

    sub.add_parser("history", help="查看历史")
    sub.add_parser("strategies", help="查看策略")

    p = sub.add_parser("serve", help="启动Web服务")
    p.add_argument("--port", type=int, default=8001)

    args = parser.parse_args()
    opt = PromptOptimizer()

    if args.cmd == "optimize":
        cases = json.load(open(args.cases, encoding="utf-8")) if args.cases else json.loads(input("测试用例JSON: "))
        result = opt.optimize(args.task, cases, args.iter)
        print(f"\n{'='*50}\n  优化结果\n{'='*50}")
        for r in result["ranking"]:
            print(f"  #{r['rank']} {r['name']:25} {r['avg_score']}/40")
        if result["best"]:
            print(f"\n最优Prompt ({result['best']['name']}):\n{'─'*50}\n{result['best']['prompt']}")
    elif args.cmd == "history":
        for h in opt.get_history():
            print(f"  {h['timestamp']} | {h['best_score']}分 | {h['best_strategy']}")
    elif args.cmd == "strategies":
        for s in opt.get_strategies():
            print(f"  {s['name']:15} {s['desc']}")
    elif args.cmd == "serve":
        import uvicorn; from api.main import app
        uvicorn.run(app, host="0.0.0.0", port=args.port)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
