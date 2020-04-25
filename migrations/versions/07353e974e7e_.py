"""empty message

Revision ID: 07353e974e7e
Revises: 22f6f07fc3e7
Create Date: 2020-04-25 14:11:27.917412

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07353e974e7e'
down_revision = '22f6f07fc3e7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('error', sa.Column('date', sa.DateTime(), nullable=False))
    op.alter_column('error', 'is_resolved',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('error', 'is_resolved',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.drop_column('error', 'date')
    # ### end Alembic commands ###