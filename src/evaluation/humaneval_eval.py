import traceback
from typing import Dict, Any

from datasets import load_dataset

from src.core.agent import DevAgent


def build_humaneval_task(example: Dict[str, Any]) -> str:
    """
    Convert a HumanEval example to a task string for DevAgent.
    """
    return f"""
You are a professional Python developer.

Please implement the following function according to the specification.
Only provide the Python code.

{example["prompt"]}
"""


def run_humaneval(agent: DevAgent, max_samples: int = None):
    dataset = load_dataset("openai_humaneval")["test"]

    total = 0
    passed = 0
    failed_cases = []

    for idx, example in enumerate(dataset):
        if max_samples is not None and total >= max_samples:
            break

        print(f"\n{'=' * 60}")
        print(f"[HumanEval] Problem {idx}: {example['entry_point']}")
        print(f"{'=' * 60}")

        task = build_humaneval_task(example)

        try:
            # === Agent solve ===
            code = agent.solve(task)

            # === Execute generated code + official tests ===
            exec_globals = {}
            exec(code, exec_globals)
            exec(example["test"], exec_globals)

            print("✅ PASSED")
            passed += 1

        except Exception as e:
            print("❌ FAILED")
            traceback.print_exc()

            failed_cases.append({
                "task_id": example["task_id"],
                "entry_point": example["entry_point"],
                "error": str(e),
            })

        total += 1

    pass_at_1 = passed / total if total > 0 else 0.0

    print("\n" + "=" * 60)
    print("HumanEval Evaluation Summary")
    print("=" * 60)
    print(f"Total Samples : {total}")
    print(f"Passed        : {passed}")
    print(f"Pass@1        : {pass_at_1:.4f}")
    print("=" * 60)

    return {
        "total": total,
        "passed": passed,
        "pass@1": pass_at_1,
        "failed_cases": failed_cases,
    }


def main():

    max_iter = 1
    max_samples = None

    agent = DevAgent(max_iter=max_iter)

    run_humaneval(agent, max_samples=max_samples)


if __name__ == "__main__":
    main()
