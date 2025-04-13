import logging
import os
import subprocess
import sys
from pathlib import Path

import colorlog


def setup_logger():
    log_dir = Path.cwd()
    while log_dir.name != 'src' and log_dir != log_dir.parent:
        log_dir = log_dir.parent

    if log_dir.name == 'src':
        log_dir = log_dir.parent
    else:
        log_dir = Path.cwd()

    log_dir = log_dir / 'logs'
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, 'log.txt')

    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)

    if log.hasHandlers():
        log.handlers.clear()

    # Formatting
    msg_fmt = "%(asctime)s.%(msecs)03d | Line: %(lineno)3d %(module)s.%(funcName)-20s | %(levelname)-8s: %(message)s"
    date_fmt = "%Y-%m-%d %H:%M:%S"

    file_formatter = MultilineFormatter(fmt=msg_fmt, datefmt=date_fmt)
    file_handler = logging.FileHandler(log_file, 'a', encoding='utf-8', delay=False)
    file_handler.setFormatter(file_formatter)
    log.addHandler(file_handler)

    console_formatter = ColoredMultilineFormatter(
        "%(log_color)s" + msg_fmt,
        datefmt=date_fmt,
        log_colors={
            'DEBUG': 'green',
            'INFO': 'light_white',
            'WARNING': 'light_yellow',
            'ERROR': 'light_red',
            'CRITICAL': 'bold_light_red',
        }
    )
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    log.addHandler(console_handler)

    return log


def get_commit_hash():
    try:
        commit_hash = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], stderr=subprocess.STDOUT
        ).decode("utf-8").strip()
        return commit_hash
    except subprocess.CalledProcessError as e:
        logger.error(f"Error getting commit hash: {e.output.decode('utf-8')}")
        return "unknown"


def get_latest_tag():
    try:
        latest_tag = subprocess.check_output(
            ["git", "describe", "--tags", "--abbrev=0"], stderr=subprocess.STDOUT
        ).decode("utf-8").strip()
        return latest_tag
    except subprocess.CalledProcessError as e:
        logger.error(f"Error getting latest tag: {e.output.decode('utf-8')}")
        return "unknown"


class MultilineFormatter(logging.Formatter):
    def format(self, record):
        original = super().format(record)
        message = record.getMessage()
        prefix, _, _ = original.partition(message)
        return _format_multiline(record, original, message, prefix)


class ColoredMultilineFormatter(colorlog.ColoredFormatter):
    def format(self, record):
        original = super().format(record)
        message = record.getMessage()
        prefix, _, _ = original.partition(message)
        return _format_multiline(record, original, message, prefix, color_offset=5)


def _format_multiline(record, original, message, prefix, color_offset=0):
    indent = ' ' * (len(prefix) - color_offset)

    msg_break = getattr(record, 'msg_break', None)
    if msg_break is not None:
        msg_break = msg_break * (len(prefix) - color_offset)

    no_indent = getattr(record, 'no_indent', False)
    if no_indent or '\n' not in message:
        if msg_break is not None:
            return original + '\n' + msg_break
        return original

    if '\n' in message:
        lines = message.splitlines()
        indented_message = lines[0] + '\n' + '\n'.join(indent + line for line in lines[1:])
        formatted = prefix + indented_message

        if msg_break is not None:
            return formatted + '\n' + msg_break
        return formatted


logger = setup_logger()


def main():
    logger.info(f"Done.", extra={'msg_break': '*'})
    logger.info(f"Done.\n----------", extra={'no_indent': True})
    logger.info(f"Done.\nfffffffffff", extra={'msg_break': '/', 'no_indent': True})

    logger.debug('debug message')
    logger.info('hello world')
    logger.warning('Oh No')
    logger.error('Error')
    logger.critical('Critical')
    logger.info(f"Commit hash: {get_commit_hash()}\nLatest tag:")


def example():
    try:
        1 / 0
    except Exception as e:
        logger.exception(e)


if __name__ == "__main__":
    main()
    example()