from argparse import ArgumentParser, ArgumentTypeError, Namespace
from pathlib import Path
import html, re

from .logger import logger
from .consts import COOKIE_FILE, FILE_TEMPLATE, IARG_EMPTY

type Iarg = int | tuple[int, int]


def valid_iarg(value) -> Iarg:
    if value.isdigit():
        return int(value)
    if value == "all":
        return IARG_EMPTY
    if (
        "-" in value
        and len(parts := value.split("-")) == 2
        and all(map(str.isdigit, parts))
    ):
        return tuple(map(int, parts))  # type: ignore
    raise ArgumentTypeError(
        f"Invalid value: {value}. Must be a positive integer,"
        " two dash-separated positive integers, or 'all'."
    )

def parse_cmd() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("-d", "--day", type=valid_iarg, default=None, help="The day")
    parser.add_argument("-y", "--year", type=valid_iarg, default=None, help="The year")
    parser.add_argument(
        "-c", "--cookie", type=Path, default=COOKIE_FILE, help="The cookie file"
    )
    parser.add_argument(
        "-p",
        "--pattern",
        type=str,
        default=None,
        help="The pattern to use for the folder name",
    )
    parser.add_argument(
        "-m",
        "--match",
        type=str,
        default=None,
        help="Match folder structure and fill days that have no data",
    )
    parser.add_argument(
        "--write-cookie",
        type=str,
        default=None,
        help="Write a new cookie string to the cookie file",
    )
    parser.add_argument(
        "-f",
        "--files",
        type=str,
        nargs="+",
        default=("p1.py", "p2.py"),
        help="Specify filenames",
    )
    parser.add_argument(
        "-t",
        "--template",
        type=str,
        default=FILE_TEMPLATE,
        help="The template to use for new problem files",
    )
    
    return parser.parse_args()


def pat_to_regex(pattern) -> re.Pattern:
    escaped_pattern = re.escape(pattern).replace(r"\*", ".*")
    logger.debug(f"Escaped pattern: {pattern} -> {escaped_pattern}")
    named_regex_pattern = re.sub(
        r"\\\{(\w+).*\\\}", r"(?P<\1>\\d+)", escaped_pattern
    )
    logger.debug(f"Converted pattern: {pattern} -> {named_regex_pattern}")
    return re.compile(named_regex_pattern)


def clean_data(data: str) -> str:
    return html.unescape(data.removesuffix("\n"))
