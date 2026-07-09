"""Add user_id to tasks

Revision ID: d1787cf38187
Revises: 49976e582815
Create Date: 2026-07-09 23:28:05.910938

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd1787cf38187'
down_revision: Union[str, Sequence[str], None] = '49976e582815'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    with op.batch_alter_table("tasks") as batch_op:

        batch_op.add_column(
            sa.Column(
                "user_id",
                sa.Integer(),
                nullable=True
            )
        )

        batch_op.create_index(
            "ix_tasks_user_id",
            ["user_id"],
            unique=False
        )

        batch_op.create_foreign_key(
            "fk_tasks_user_id_users",
            "users",
            ["user_id"],
            ["id"]
        )


def downgrade() -> None:
    """Downgrade schema."""

    with op.batch_alter_table("tasks") as batch_op:

        batch_op.drop_constraint(
            "fk_tasks_user_id_users",
            type_="foreignkey"
        )

        batch_op.drop_index(
            "ix_tasks_user_id"
        )

        batch_op.drop_column(
            "user_id"
        )
