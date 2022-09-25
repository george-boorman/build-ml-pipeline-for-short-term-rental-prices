#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import wandb


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # YOUR CODE HERE     #
    ######################
    logger.info(f"Downloading {args.input_artifact}")



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Basic data cleaning")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="Link to the dataset from W&B",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="Name to save the updated dataset as",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="Type of output created by the step",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="Cleaned dataset",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help="Minimum price we'll pay for a NYC rental",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="Maximum price we'll pay for a NYC rental",
        required=True
    )


    args = parser.parse_args()

    go(args)
