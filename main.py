import argparse
import logging
import sys
from pathlib import Path

import yaml

from src.models.domain import ExperimentConfig
from src.runner.orchestrator import ExperimentRunner


def setup_logging():
    """Sets up basic logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def run_experiment(config_path: str):
    """
    Parses the configuration YAML and executes the experiment runner.
    """
    logger = logging.getLogger(__name__)
    path = Path(config_path)

    if not path.exists():
        logger.error(f"Configuration file not found: {config_path}")
        sys.exit(1)

    try:
        with open(path, "r") as f:
            config_data = yaml.safe_load(f)

        if config_data is None:
            logger.error(f"Configuration file is empty: {config_path}")
            sys.exit(1)

        config = ExperimentConfig.model_validate(config_data)
        logger.info(f"Loaded configuration for experiment: {config.experiment_id}")

        runner = ExperimentRunner(config)
        runner.run()
        logger.info("Experiment run completed successfully.")

    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML configuration: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        # Re-raise for full traceback in development if needed,
        # but for CLI we usually want clean errors.
        if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
            raise
        sys.exit(1)


def main():
    setup_logging()
    parser = argparse.ArgumentParser(description="Weak-Driven Prompt Optimization CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # run-experiment command
    run_parser = subparsers.add_parser(
        "run-experiment", help="Execute an optimization experiment"
    )
    run_parser.add_argument(
        "--config",
        type=str,
        required=True,
        help="Path to the experiment YAML configuration file",
    )

    args = parser.parse_args()

    if args.command == "run-experiment":
        run_experiment(args.config)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
