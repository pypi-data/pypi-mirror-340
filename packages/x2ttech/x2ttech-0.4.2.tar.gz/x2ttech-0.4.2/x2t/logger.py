
# -*- coding: utf-8 -*-
import base64
import requests
import unidecode
import re
import platform
import os
import sys
from pathlib import Path
from loguru import logger
from threading import Thread


def set_file_path(filename):
    system = platform.system()
    if system == "Windows":
        log_dir = Path.home() / "AppData" / "Local" / "Odoo" / "logs"
    elif system == "Darwin":
        log_dir = Path.home() / "Library" / "Logs" / "Odoo"
    else:
        default_log_dir = Path("/var/log/odoo")
        if os.access(default_log_dir, os.W_OK):
            log_dir = default_log_dir
        else:
            log_dir = Path.home() / "odoo_logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir / filename


def configure(
    filename: str = "loguru.odoo.{time:DD-MM-YYYY}.log",
    level: str = "INFO",
    rotation: str = "10 MB",
    retention: str = "10 days",
    colorize: bool = False,
    enqueue: bool = True,
    backtrace: bool = True,
    diagnose: bool = True,
    file_format: str = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                       "<level>{level: <8}</level> | "
                       "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
                       "<level>{message}</level>",
    console_format: str = "<green>{time:HH:mm:ss}</green> | "
                          "<level>{level: <8}</level> | "
                          "<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
                          "<level>{message}</level>",
):
    """Configure the global logger with file and console outputs."""
    path = set_file_path(filename)
    logger.remove()
    logger.add(
        str(path),
        rotation=rotation,
        retention=retention,
        level=level,
        colorize=colorize,
        enqueue=enqueue,
        backtrace=backtrace,
        diagnose=diagnose,
        format=file_format,
    )
    logger.add(
        sys.stderr,
        level=level,
        colorize=True,
        enqueue=enqueue,
        backtrace=backtrace,
        diagnose=diagnose,
        format=console_format,
    )
    return logger


logger = configure()
