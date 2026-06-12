#!/usr/bin/env python3
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from core.optimizer import PromptOptimizer

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", "-t", required=True)
    parser.add_argument("--cases", "-c", required=True)
    parser.add_argument("--iter", type=int, default=2)
    args = parser.parse_args()
    cases = json.load(open(args.cases, encoding="utf-8"))
    result = PromptOptimizer().optimize(args.task, cases, args.iter)
    print(f"\n最优: {result['best']['name']} | {result['best']['avg_score']}/40\n\n{result['best']['prompt']}")

if __name__ == "__main__":
    main()
