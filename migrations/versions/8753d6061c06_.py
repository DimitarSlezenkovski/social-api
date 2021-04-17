"""empty message

Revision ID: 8753d6061c06
Revises: fe6e99fd5abf
Create Date: 2021-04-16 19:39:11.802672

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8753d6061c06'
down_revision = 'fe6e99fd5abf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comments', 'createdOn')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('createdOn', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###