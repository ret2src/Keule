import logging
import sys

from lib.config import KeuleConfig

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    with open("keule.yaml") as cfg:
        config = KeuleConfig(cfg)

    for context in config.contexts:
        context.build()
