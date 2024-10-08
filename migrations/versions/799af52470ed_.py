"""empty message

Revision ID: 799af52470ed
Revises: 
Create Date: 2024-04-02 15:39:09.424443

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '799af52470ed'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('music', schema=None) as batch_op:
        batch_op.add_column(sa.Column('music_file', sa.String(length=100), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('music', schema=None) as batch_op:
        batch_op.drop_column('music_file')

    # ### end Alembic commands ###
