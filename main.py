import argparse
from pathlib import Path

from src.reporting.analyzer import ReportingEngine


def main():
    parser = argparse.ArgumentParser(description="Weak-Driven Prompt Optimization CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # The report command
    report_parser = subparsers.add_parser(
        "report", help="Generate an experiment report"
    )
    report_parser.add_argument(
        "--experiment-id", required=True, help="ID of the experiment to report on"
    )
    report_parser.add_argument(
        "--output", help="Optional path to output the markdown report"
    )

    args = parser.parse_args()

    if args.command == "report":
        engine = ReportingEngine(experiment_id=args.experiment_id)
        report_md = engine.generate_report()

        if args.output:
            out_path = Path(args.output)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(report_md)
            print(f"Report saved to {out_path}")
        else:
            print(report_md)
    else:
        # If no command, just print the help. Or do whatever the base main should do.
        if not args.command:
            parser.print_help()


if __name__ == "__main__":
    main()
