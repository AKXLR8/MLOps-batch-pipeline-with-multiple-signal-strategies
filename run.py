import argparse
import time
import json
import traceback

from utils.data import load_config, load_and_clean_data
from utils.signals import generate_signals
from utils.metrics import compute_metrics
from utils.logger import setup_logger


def main(args):
    logger = setup_logger(args.log_file)
    start_time = time.time()

    try:
        logger.info("Job started")

        config = load_config(args.config)
        logger.info(f"Config loaded: {config}")

        df = load_and_clean_data(args.input)
        logger.info(f"Rows loaded: {len(df)}")

        df = generate_signals(df, config)
        logger.info("Signals generated")

        metrics = compute_metrics(df, config, start_time)
        logger.info(f"Metrics: {metrics}")

        with open(args.output, "w") as f:
            json.dump(metrics, f, indent=4)

        print(json.dumps(metrics, indent=4))
        logger.info("Job completed successfully")

    except Exception as e:
        error_output = {
            "version": "v1",
            "status": "error",
            "error_message": str(e)
        }

        with open(args.output, "w") as f:
            json.dump(error_output, f, indent=4)

        logger.error(traceback.format_exc())
        print(json.dumps(error_output, indent=4))
        exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--log-file", required=True)

    args = parser.parse_args()
    main(args)



