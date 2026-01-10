import argparse
from pathlib import Path

from src.core.agent import DevAgent


def load_task(args) -> str:
    if args.task:
        return args.task
    if args.file:
        return Path(args.file).read_text(encoding="utf-8")
    raise ValueError("Must provide --task or --file")


def main():
    parser = argparse.ArgumentParser(
        prog="devagent",
        description="DevAgent: Plan → Code → Test → Fix loop"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # ========== solve ==========
    solve_parser = subparsers.add_parser("solve", help="Solve a coding task")
    solve_parser.add_argument("-t", "--task", type=str, help="Task description")
    solve_parser.add_argument("-f", "--file", type=str, help="Task file path")
    solve_parser.add_argument("--max-iter", type=int, default=None)
    solve_parser.add_argument("--save", type=str, help="Save final code to file")
    solve_parser.add_argument("--verbose", action="store_true")

    args = parser.parse_args()

    if args.command == "solve":
        task = load_task(args)

        agent = DevAgent(max_iter=args.max_iter)

        code = agent.solve(task)

        if args.save:
            Path(args.save).write_text(code, encoding="utf-8")
            print(f"\n📄 Code saved to {args.save}")

        else:
            print("\n===== FINAL CODE =====\n")
            print(code)


if __name__ == "__main__":
    main()
