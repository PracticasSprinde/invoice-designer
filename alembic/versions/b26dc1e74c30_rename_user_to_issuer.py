"""rename user to issuer

Revision ID: b26dc1e74c30
Revises: f000f4f2bc20
Create Date: 2026-11-16 10:06:26.036342

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b26dc1e74c30'
down_revision: Union[str, Sequence[str], None] = 'f000f4f2bc20'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.rename_table("product", "products")
    op.rename_table("users", "issuers")
    op.alter_column("issuers", "user_id", new_column_name="issuer_id")

    for table in ("clients", "templates", "invoices", "products"):
        op.alter_column(table, "user_id", new_column_name="issuer_id")


def downgrade() -> None:
    for table in ("clients", "templates", "invoices", "products"):
        op.alter_column(table, "issuer_id", new_column_name="user_id")

    op.alter_column("issuers", "issuer_id", new_column_name="user_id")
    op.rename_table("issuers", "users")
