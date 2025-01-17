#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import wandb
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(project="nyc_airbnb", job_type="basic_cleaning", save_code=True)
    run.config.update(args)

    logger.info(f"Downloading {args.input_artifact}")
    data_path = run.use_artifact(args.input_artifact).file()
    df = pd.read_csv(data_path, low_memory=False)

    # Drop outliers
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()

    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])

    # Set boundary limits
    idx = df['longitude'].between(-74.25, -73.50) & df['latitude'].between(40.5, 41.2)
    df = df[idx].copy()

    # Save updated DataFrame
    df.to_csv("clean_sample.csv", index=False)

    # Upload cleaned DataFrame to W&B
    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file("clean_sample.csv")
    run.log_artifact(artifact)

    logger.info(f"Logging {artifact}")


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
