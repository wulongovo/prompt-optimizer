import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from core.prompt_generator import STRATEGIES
from core.optimizer import PromptOptimizer

def test():
    assert len(STRATEGIES) == 6
    opt = PromptOptimizer()
    assert isinstance(opt.get_history(), list)
    assert len(opt.get_strategies()) == 6
    print("✓ 所有测试通过")

if __name__ == "__main__":
    test()
