import argparse
import asyncio
import getpass
import sys

from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError

from src.staff.enums import Role
from src.staff.models import Staff
from src.core.security import hash_password
from src.core.database import session_maker


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Создание учётной записи персонала")
    parser.add_argument("-u", "--username", required=True, help="логин")
    parser.add_argument("-p", "--password", help="пароль; спросим, если не указан")
    parser.add_argument(
        "-r",
        "--role",
        choices=[r.name for r in Role],
        default=Role.MANAGER.name,
        help="роль (по умолчанию MANAGER)",
    )
    return parser.parse_args()


async def create_staff(username: str, password: str, role: str) -> None:
    async with session_maker() as session:
        query = insert(Staff).values(
            username=username,
            password=hash_password(password),
            role=role,
        )
        await session.execute(query)
        await session.commit()


def main() -> int:
    args = parse_args()

    password = args.password or getpass.getpass("Пароль: ")

    if not password:
        print("Пароль не может быть пустым", file=sys.stderr)
        return 1

    try:
        asyncio.run(create_staff(args.username, password, args.role))
    except IntegrityError:
        print(f"Учётная запись {args.username!r} уже существует", file=sys.stderr)
        return 1

    print(f"Создана учётная запись {args.username!r} с ролью {args.role}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
