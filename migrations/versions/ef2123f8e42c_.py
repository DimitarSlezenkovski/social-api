"""empty message

Revision ID: ef2123f8e42c
Revises: fe983dcb0055
Create Date: 2021-04-16 16:08:52.082953

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef2123f8e42c'
down_revision = 'fe983dcb0055'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('messages', sa.Column('text', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('messages', 'text')
    # ### end Alembic commands ###
