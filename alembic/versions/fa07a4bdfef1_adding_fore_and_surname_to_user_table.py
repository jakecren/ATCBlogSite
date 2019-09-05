"""Adding fore and surname to User table

Revision ID: fa07a4bdfef1
Revises: 07a127a5df58
Create Date: 2019-08-23 20:36:40.210157

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa07a4bdfef1'
down_revision = '07a127a5df58'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('User', sa.Column('surname', sa.String(50), nullable=True))


def downgrade():
    op.drop_column('User', 'surname')
