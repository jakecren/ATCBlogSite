"""Adding surname to User table

Revision ID: 7ecb5eb6f7fd
Revises: fa07a4bdfef1
Create Date: 2019-08-23 20:56:22.384898

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ecb5eb6f7fd'
down_revision = 'fa07a4bdfef1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('User', sa.Column('surname', sa.String(50), nullable=True))


def downgrade():
    op.drop_column('User', 'surname')
