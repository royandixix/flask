"""buat table mahasiswa

Revision ID: 7253dc95f49b
Revises: e4f9a9d960ee
Create Date: 2025-03-25 12:06:02.312305

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7253dc95f49b'
down_revision = 'e4f9a9d960ee'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mahasiswa',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('nim', sa.String(length=300), nullable=False),
    sa.Column('nama', sa.String(length=399), nullable=False),
    sa.Column('phone', sa.String(length=13), nullable=False),
    sa.Column('alamat', sa.String(length=100), nullable=False),
    sa.Column('dosen_satu', sa.BigInteger(), nullable=True),
    sa.Column('dosen_dua', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['dosen_dua'], ['dosen.id'], ),
    sa.ForeignKeyConstraint(['dosen_satu'], ['dosen.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('mahasiswa')
    # ### end Alembic commands ###
