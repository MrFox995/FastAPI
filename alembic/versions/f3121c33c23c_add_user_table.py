"""add_user_table

Revision ID: f3121c33c23c
Revises: 84d66e6910e4
Create Date: 2026-01-28 14:45:18.791563

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f3121c33c23c'
down_revision: Union[str, Sequence[str], None] = '84d66e6910e4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users_test',
                        sa.Column('ID', sa.Integer(), nullable = False),
                        sa.Column('email', sa.String(), nullable = False),
                        sa.Column('password', sa.String(), nullable = False),
                        sa.Column('created_at', sa.TIMESTAMP(timezone = True), server_default = sa.text('now()'), nullable = False),
                        sa.PrimaryKeyConstraint('ID'),
                        sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    op.drop_table('users_test')
    pass
