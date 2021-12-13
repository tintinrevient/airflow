#!/usr/bin/env python

import click
import requests
import logging
from pathlib import Path
import json


logging.basicConfig(level=logging.INFO)

@click.command()
@click.option("--start_date", type=click.DateTime(formats=["%Y-%m-%d"]), required=True, help="Start date for ratings.")
@click.option("--end_date", type=click.DateTime(formats=["%Y-%m-%d"]), required=True, help="End date for ratings.")
@click.option("--output_path", type=click.Path(dir_okay=False), required=True, help="Output file path.")
@click.option("--host", type=str, default="http://localhost:5000", help="Ratings API.")
@click.option("--username", type=str, envvar="API_USER", required=True, help="API user.")
@click.option("--password", type=str, envvar="API_PASSWORD", required=True, help="API password.")
@click.option("--batch_size", type=int, default=100, help="Batch size for retrieving records.")
def main(start_date, end_date, output_path, host, username, password, batch_size):
    """CLI interface to get ratings from the server."""
    session = requests.Session()
    session.auth = (username, password)

    logging.info("Fetching ratings from %s (username: %s)", host, username)
    ratings = list(_get_ratings(session, host, start_date, end_date, batch_size))
    logging.info("Retrieved %d ratings!", len(ratings))

    output_path = Path(output_path)
    output_dir = output_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    logging.info("Writing to %s", output_path)
    with output_path.open("w") as _file:
        json.dump(ratings, _file)


def _get_ratings(session, host, start_date, end_date, batch_size=100):
    yield from _get_with_pagination(
        session,
        url=host+"/ratings",
        params={
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d")
        },
        batch_size=batch_size
    )


def _get_with_pagination(session, url, params, batch_size=100):
    """Get records using a get request with given url/params"""

    offset = 0
    total = None
    while total is None or offset < total:
        response = session.get(url, params={**params, **{"offset": offset, "limit": batch_size}})
        response.raise_for_status()
        response_json = response.json()

        yield from response_json["result"]

        offset += batch_size
        total = response_json["total"]


if __name__ == "__main__":
    main()
