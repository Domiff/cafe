import argparse
import asyncio
import sys

from sqlalchemy import insert

from src.cafe.models import Employee


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Загрузка данных в базу данных")
    parser.add_argument("-f", "--filename", required=True, help="имя файла")

    return parser.parse_args()


async def load_employees() -> None:
    ...
