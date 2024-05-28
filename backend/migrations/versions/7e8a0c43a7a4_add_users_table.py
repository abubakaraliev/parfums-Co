"""add users table

Revision ID: 7e8a0c43a7a4
Revises: 
Create Date: 2024-05-27 11:29:17.381935

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e8a0c43a7a4'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('user',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('username', sa.Unicode(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('email_verified', sa.Boolean(), nullable=True, server_default=sa.sql.expression.true()),
        sa.Column('salt', sa.Unicode(length=255), nullable=False),
        sa.Column('password', sa.Unicode(length=255), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.sql.expression.true()),
        sa.Column('is_superuser', sa.Boolean(), nullable=False, server_default=sa.sql.expression.false()),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username'),
        sa.UniqueConstraint('email')
    )

def downgrade():
    op.drop_table('user')
