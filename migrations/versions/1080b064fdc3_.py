"""empty message

Revision ID: 1080b064fdc3
Revises: dec74dd0a07e
Create Date: 2023-11-03 20:45:00.180551

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1080b064fdc3'
down_revision = 'dec74dd0a07e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('confirmed', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('confirmed')

    # ### end Alembic commands ###
