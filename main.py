import argparse
import logging
import sys

from lib.config import KeuleConfig

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser(
    description=(
        "Generate wordlists using some fancy pipelines"
    ))


    parser.add_argument(
        "-v",
        "--verbose",
        action="store_const",
        const=logging.DEBUG,
        default=logging.INFO,
        dest="loglevel",
        help="increase verbosity level",
        required=False
    )

    parser.add_argument('config', metavar='J', type=argparse.FileType('r'), default="keule.yaml")
    args = parser.parse_args()

    config = KeuleConfig(args.config)

    for context in config.contexts:
        context.build()
