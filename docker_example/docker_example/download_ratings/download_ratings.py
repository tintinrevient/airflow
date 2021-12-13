#!/usr/bin/env python

import logging
import click
import tempfile
from pathlib import Path
from urllib.request import urlretrieve
import zipfile
import pandas as pd


logging.basicConfig(level=logging.INFO)

@click.command()
@click.option("--start_date", default="2019-01-01", type=click.DateTime())
@click.option("--end_date", default="2020-01-01", type=click.DateTime())
@click.option("--output_path", required=True)
def main(start_date, end_date, output_path):
    """CLI interface to download and parse ratings from the given URL."""

    logging.info("Download the data of ratings...")
    ratings = _download_ratings()

    logging.info(f"Filtering for dates {start_date} - {end_date}...")
    col_timestamp_parsed = pd.to_datetime(ratings["timestamp"], unit="s")
    ratings = ratings.loc[(col_timestamp_parsed >= start_date) & (col_timestamp_parsed < end_date)]

    logging.info(f"Writing ratings to '{output_path}'...")
    ratings.to_csv(output_path, index=False)

def _download_ratings():
    """Download ratings from the given URL."""

    url = "http://files.grouplens.org/datasets/movielens/ml-25m.zip"

    with tempfile.TemporaryDirectory() as tmp_dir:
        zipfile_path = Path(tmp_dir, "ratings.zip")
        logging.info(f"Downloading zip file from {url}")
        urlretrieve(url, zipfile_path)

        with zipfile.ZipFile(zipfile_path) as _zipfile:
            logging.info(f"Downloaded zip file with contents: {_zipfile.namelist()}")
            logging.info("Reading ml-25m/ratings.csv from zip file")

            with _zipfile.open("ml-25m/ratings.csv") as _csvfile:
                ratings = pd.read_csv(_csvfile)

    return ratings


if __name__ == "__main__":
    main()
