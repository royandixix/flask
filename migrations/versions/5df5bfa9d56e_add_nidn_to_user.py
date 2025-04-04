"""add nidn to user

Revision ID: 5df5bfa9d56e
Revises: d119693ac480
Create Date: 2025-04-01 19:14:38.694880

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5df5bfa9d56e'
down_revision = 'd119693ac480'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index('nidn')
        batch_op.drop_column('nidn')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('nidn', mysql.VARCHAR(length=60), nullable=True))
        batch_op.create_index('nidn', ['nidn'], unique=True)

    # ### end Alembic commands ###
