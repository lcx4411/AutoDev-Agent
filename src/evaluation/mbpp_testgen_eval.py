import traceback
import multiprocessing as mp
from typing import Dict, Any, List

from datasets import load_dataset

from src.core.tester import TestGenerator
from src.core.planner import TaskPlanner


# ===============================
# Subprocess execution
# ===============================

def _exec_tests_in_subprocess(code: str):
    """
    Execute generated test code in isolated process.
    Any exception will propagate via process exit.
    """
    exec_globals = {}
    exec(code, exec_globals)


def run_with_timeout(code: str, timeout: int = 2):
    """
    Run code in a separate process with timeout.
    """
    p = mp.Process(target=_exec_tests_in_subprocess, args=(code,))
    p.start()
    p.join(timeout)

    if p.is_alive():
        p.terminate()
        p.join()
        raise TimeoutError("Test execution timeout")


# ===============================
# MBPP TestGen Evaluation
# ===============================

def run_mbpp_testgen(
    max_samples: int = None,
    timeout: int = 2,
    verbose: bool = False,
):
    """
    Test Validity Rate:
    - A test is valid if it can be executed within time limit
    - Assertion failures are allowed
    """

    dataset = load_dataset("mbpp")["test"]

    planner = TaskPlanner()
    tester = TestGenerator()

    total = 0
    executable = 0
    timeout_cases = 0
    assertion_error = 0
    runtime_error_cases = 0

    failed_cases: List[Dict[str, Any]] = []

    for idx, example in enumerate(dataset):
        if max_samples is not None and total >= max_samples:
            break

        print(f"\n{'=' * 60}")
        print(f"[MBPP] Problem {idx}")
        print(f"{'=' * 60}")
        print(example["text"])

        try:
            # === Build Plan ===
            plan = planner.plan(example["text"])
            plan["constraints"] = "Generate executable Python assert-based tests."

            # === Generate Tests ===
            tests = tester.generate(plan)

            if verbose:
                print("\n[Plan]")
                print(plan)
                print("\n[Generated Tests]")
                print(tests)

            # === Execute with timeout ===
            try:
                run_with_timeout(tests, timeout=timeout)
                print("✅ Tests Executable")
                executable += 1

            except AssertionError:
                # Assertion failure is acceptable
                print("⚠️ Assertion failed, but tests are executable")
                executable += 1
                assertion_error += 1

            except TimeoutError:
                print("⏱️ Test execution timeout")
                timeout_cases += 1
                failed_cases.append({
                    "index": idx,
                    "text": example["text"],
                    "error": "timeout",
                })

            except Exception as e:
                print(f"❌ Runtime error: {e}")
                runtime_error_cases += 1
                failed_cases.append({
                    "index": idx,
                    "text": example["text"],
                    "error": str(e),
                })

        except Exception as e:
            print(f"❌ Test generation failed: {e}")
            if verbose:
                traceback.print_exc()
            runtime_error_cases += 1
            failed_cases.append({
                "index": idx,
                "text": example["text"],
                "error": f"generation error: {e}",
            })

        total += 1

    validity_rate = executable / total if total > 0 else 0.0

    # ===============================
    # Summary
    # ===============================
    print("\n" + "=" * 60)
    print("MBPP Test Generation Evaluation Summary")
    print("=" * 60)
    print(f"Total Samples        : {total}")
    print(f"Executable Tests     : {executable}")
    print(f"Assertion Error      : {assertion_error}")
    print(f"Timeout Cases        : {timeout_cases}")
    print(f"Runtime Error Cases  : {runtime_error_cases}")
    print(f"Test Validity Rate   : {validity_rate:.4f}")
    print("=" * 60)

    return {
        "total": total,
        "executable": executable,
        "assertion_error": assertion_error,
        "timeout_cases": timeout_cases,
        "runtime_error_cases": runtime_error_cases,
        "validity_rate": validity_rate,
        "failed_cases": failed_cases,
    }


# ===============================
# Entry
# ===============================

def main():
    results = run_mbpp_testgen(timeout=120)

    print("\n[Failed Cases]")
    for case in results["failed_cases"][:5]:
        print(case)


if __name__ == "__main__":
    mp.set_start_method("spawn", force=True)
    main()
