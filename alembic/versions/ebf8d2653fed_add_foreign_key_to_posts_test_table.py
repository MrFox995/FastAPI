"""add foreign key to posts_test table

Revision ID: ebf8d2653fed
Revises: f3121c33c23c
Create Date: 2026-01-28 14:54:36.683770

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ebf8d2653fed'
down_revision: Union[str, Sequence[str], None] = 'f3121c33c23c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts_test', sa.Column('owner_ID', sa.Integer(), sa.ForeignKey('users_test.ID', ondelete = 'CASCADE'), nullable = False))
    pass


def downgrade() -> None:
    op.drop_column('posts_test', 'owner_ID')
    pass
