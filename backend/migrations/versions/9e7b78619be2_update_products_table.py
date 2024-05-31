"""update products table

Revision ID: 9e7b78619be2
Revises: 8c59b483b379
Create Date: 2024-05-31 11:12:07.357440

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '9e7b78619be2'
down_revision: Union[str, None] = '8c59b483b379'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('image', sa.String(length=255), nullable=True))
    op.add_column('product', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.add_column('product', sa.Column('updated_at', sa.DateTime(), nullable=False))
    op.drop_column('product', 'date_added')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('date_added', mysql.DATETIME(), nullable=False))
    op.drop_column('product', 'updated_at')
    op.drop_column('product', 'created_at')
    op.drop_column('product', 'image')
    # ### end Alembic commands ###