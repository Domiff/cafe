"""rename users to staff

Revision ID: 3b714ca7df67
Revises: cc0f07874517
Create Date: 2026-08-19 18:49:06.770729

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import src.core.types

# revision identifiers, used by Alembic.
revision: str = "3b714ca7df67"
down_revision: Union[str, Sequence[str], None] = "cc0f07874517"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.rename_table("users", "staff")


def downgrade() -> None:
    """Downgrade schema."""
    op.rename_table("staff", "users")
