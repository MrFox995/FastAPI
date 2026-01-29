"""create posts table

Revision ID: 881a985d663d
Revises: 
Create Date: 2026-01-28 11:57:57.852736

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '881a985d663d'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts_test', 
                        sa.Column('ID', sa.Integer(), nullable = False, primary_key = True),
                        sa.Column('title', sa.String(), nullable = False)
                    )
    pass


def downgrade() -> None:
    op.drop_table('posts_test')
    pass
