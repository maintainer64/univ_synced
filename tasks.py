import argparse
import asyncio
import logging
import os

from infrastructure.command import tasks
from infrastructure.command.utils import get_inject_dependency

logging.basicConfig(level=os.environ.get("LOGLEVEL"))
logger = logging.getLogger(__name__)


async def main():
    choices = {
        "full": tasks.full_migrate,
        "from_multy": tasks.many_to_one_full_migrate,
        "from_single": tasks.one_to_many_full_migrate,
    }
    _ = get_inject_dependency()
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("starter", nargs="+", choices=list(choices.keys()))
    args = arg_parser.parse_args()
    for x in args.starter:
        logger.info(f"Running command: {x}")
        await choices[x]()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
