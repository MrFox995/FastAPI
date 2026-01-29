"""add content column to posts_test table

Revision ID: 84d66e6910e4
Revises: 881a985d663d
Create Date: 2026-01-28 14:34:06.390166

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '84d66e6910e4'
down_revision: Union[str, Sequence[str], None] = '881a985d663d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(column = sa.Column('content', sa.String(), nullable = False), table_name = 'posts_test')
    op.add_column(column = sa.Column('published', sa.Boolean(), nullable = False, server_default = 'TRUE'), table_name = 'posts_test')
    op.add_column(column = sa.Column('created_at', sa.TIMESTAMP(timezone = True), nullable = False, server_default = sa.text('NOW()')), table_name = 'posts_test')
    pass


def downgrade() -> None:
    op.drop_column(column_name = 'content', table_name = 'posts_test')
    op.drop_column(column_name = 'published', table_name = 'posts_test')
    op.drop_column(column_name = 'created_at', table_name = 'posts_test')
    pass
