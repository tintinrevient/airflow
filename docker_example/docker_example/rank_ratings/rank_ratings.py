#!/usr/bin/env python

import click
import pandas as pd
from pathlib import Path


@click.command()
@click.option( "--input_path", type=click.Path(dir_okay=False, exists=True, readable=True), required=True)
@click.option( "--output_path", type=click.Path(dir_okay=False, writable=True), required=True)
@click.option("--min_ratings", type=int, default=2)
def main(input_path, output_path, min_ratings):
    output_path = Path(output_path)

    ratings = pd.read_json(input_path)
    rankings = _rank_ratings(ratings, min_ratings)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    rankings.to_csv(output_path, index=True)


def _rank_ratings(ratings, min_ratings=2):

    ratings = (ratings.groupby("movieId").agg(
        avg_rating=pd.NamedAgg(column="rating", aggfunc="mean"),
        num_ratings=pd.NamedAgg(column="userId", aggfunc="nunique")
    ).loc[lambda df: df["num_ratings"] > min_ratings].sort_values(by=["avg_rating", "num_ratings"], ascending=False))

    return ratings


if __name__ == "__main__":
    main()
