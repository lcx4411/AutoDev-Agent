import csv
import os
import argparse
import difflib
import traceback
from typing import Dict, Any

from datasets import load_dataset

from src.core.bugfix_agent import BugFixAgent


def normalize_patch(text: str) -> str:
    """
    Normalize patch text for comparison.
    """
    lines = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith(("+", "-", "@@", "diff", "index")):
            lines.append(line)
        else:
            lines.append(line)
    return "\n".join(lines)


def patch_similarity(pred: str, ref: str) -> float:
    """
    Compute similarity between predicted patch and reference patch.
    """
    pred = normalize_patch(pred)
    ref = normalize_patch(ref)

    return difflib.SequenceMatcher(
        None, pred, ref
    ).ratio()


def build_swebench_task(example):
    return f"""
You are a senior software engineer.

Below is a real-world software bug reported in a repository.

Issue description:
{example["problem_statement"]}

Please provide a patch or corrected code that fixes the bug.
Only output the patch or the corrected code.
"""


def run_swebench_fix(
    agent: BugFixAgent,
    max_samples: int = None,
    similarity_threshold: float = 0.3,
    verbose: bool = False,
    csv_path: str = "swebench_patch_similarity.csv",
):
    write_header = not os.path.exists(csv_path)

    csv_file = open(csv_path, "a", newline="", encoding="utf-8")
    csv_writer = csv.DictWriter(
        csv_file,
        fieldnames=["instance_id", "similarity", "matched", "error"],
    )

    if write_header:
        csv_writer.writeheader()

    dataset = load_dataset("princeton-nlp/SWE-bench_Lite")["test"]

    total = 0
    matched = 0
    failed_cases = []

    for idx, example in enumerate(dataset):
        if max_samples is not None and total >= max_samples:
            break

        print(f"\n{'=' * 60}")
        print(f"[SWE-Bench Lite] Problem {idx}")
        print(f"{'=' * 60}")
        print(example["problem_statement"][:800], "...\n")

        task = build_swebench_task(example)

        try:
            # === Agent generates fix ===
            pred_patch = agent.solve(task)

            if verbose:
                print("\n[Predicted Patch]")
                print(pred_patch)

            # === Reference patch ===
            ref_patch = example.get("patch", "")

            if not ref_patch:
                raise RuntimeError("Reference patch not found")

            sim = patch_similarity(pred_patch, ref_patch)

            matched_flag = int(sim >= similarity_threshold)

            csv_writer.writerow({
                "instance_id": example["instance_id"],
                "similarity": round(sim, 4),
                "matched": matched_flag
            })

            print(f"Patch similarity: {sim:.3f}")

            if sim >= similarity_threshold:
                print("✅ MATCHED")
                matched += 1
            else:
                print("❌ NOT MATCHED")

                failed_cases.append({
                    "instance_id": example["instance_id"],
                    "similarity": sim,
                })

        except Exception as e:
            print("❌ FAILED")
            if verbose:
                traceback.print_exc()

            csv_writer.writerow({
                "instance_id": example.get("instance_id"),
                "similarity": "",
                "matched": 0
            })

            failed_cases.append({
                "instance_id": example.get("instance_id"),
                "error": str(e),
            })

        total += 1

    fix_rate = matched / total if total > 0 else 0.0

    print("\n" + "=" * 60)
    print("SWE-Bench Lite Bug Fix Evaluation Summary")
    print("=" * 60)
    print(f"Total Samples : {total}")
    print(f"Matched Fixes : {matched}")
    print(f"Fix Rate     : {fix_rate:.4f}")
    print("=" * 60)

    csv_file.close()

    return {
        "total": total,
        "matched": matched,
        "fix_rate": fix_rate,
        "failed_cases": failed_cases,
    }


def main():

    agent = BugFixAgent()

    run_swebench_fix(
        agent=agent,
        max_samples=None,
        similarity_threshold=0.2,
        verbose=False,
    )


if __name__ == "__main__":
    main()
