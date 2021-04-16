"""empty message

Revision ID: fe983dcb0055
Revises: abe3a7871807
Create Date: 2021-04-16 16:08:35.933576

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe983dcb0055'
down_revision = 'abe3a7871807'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('messages', 'text')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('messages', sa.Column('text', sa.VARCHAR(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
