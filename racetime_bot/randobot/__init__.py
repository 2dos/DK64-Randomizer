"""Loader function for the RandoBot package."""

import argparse
import logging
import sys
import os

from bot import RandoBot


def main():
    """Initialize and run the bot."""
    parser = argparse.ArgumentParser(
        description="RandoBot, because Zootr seeds weren't scary enough already.",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="verbose output")
    parser.add_argument("--host", type=str, nargs="?", help="change the ractime.gg host (debug only!")
    parser.add_argument("--insecure", action="store_true", help="don't use HTTPS (debug only!)")

    args = parser.parse_args()

    logger = logging.getLogger()
    handler = logging.StreamHandler(sys.stdout)

    if args.verbose:
        logger.setLevel(logging.DEBUG)
        handler.setLevel(logging.DEBUG)

    handler.setFormatter(logging.Formatter("[%(asctime)s] %(name)s (%(levelname)s) :: %(message)s"))
    logger.addHandler(handler)

    if args.host:
        RandoBot.racetime_host = args.host
    if args.insecure:
        RandoBot.racetime_secure = False

    inst = RandoBot(
        category_slug=os.environ.get("CATEGORY_SLUG"),
        client_id=os.environ.get("RGG_CLIENT_ID"),
        client_secret=os.environ.get("RGG_CLIENT_SECRET"),
        logger=logger,
    )
    inst.run()


if __name__ == "__main__":
    main()
