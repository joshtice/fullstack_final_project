"""empty message

Revision ID: 61fb62f47d4f
Revises: 6cd88c1bfec4
Create Date: 2020-04-25 11:40:51.745704

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61fb62f47d4f'
down_revision = '6cd88c1bfec4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contacts_instruments',
    sa.Column('contact_id', sa.Integer(), nullable=False),
    sa.Column('instrument_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['contact_id'], ['contact.id'], ),
    sa.ForeignKeyConstraint(['instrument_id'], ['instrument.id'], ),
    sa.PrimaryKeyConstraint('contact_id', 'instrument_id')
    )
    op.alter_column('contact', 'first_name',
               existing_type=sa.VARCHAR(length=32),
               nullable=False)
    op.alter_column('contact', 'last_name',
               existing_type=sa.VARCHAR(length=32),
               nullable=False)
    op.alter_column('error', 'description',
               existing_type=sa.VARCHAR(length=256),
               nullable=False)
    op.alter_column('instrument', 'serial_number',
               existing_type=sa.VARCHAR(length=32),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('instrument', 'serial_number',
               existing_type=sa.VARCHAR(length=32),
               nullable=True)
    op.alter_column('error', 'description',
               existing_type=sa.VARCHAR(length=256),
               nullable=True)
    op.alter_column('contact', 'last_name',
               existing_type=sa.VARCHAR(length=32),
               nullable=True)
    op.alter_column('contact', 'first_name',
               existing_type=sa.VARCHAR(length=32),
               nullable=True)
    op.drop_table('contacts_instruments')
    # ### end Alembic commands ###
