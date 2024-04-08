"""empty message

Revision ID: 31c6f282c8ac
Revises: 9891ee6911a5
Create Date: 2024-04-04 18:01:38.703467

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31c6f282c8ac'
down_revision = '9891ee6911a5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('genre',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('music', schema=None) as batch_op:
        batch_op.add_column(sa.Column('genre_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'genre', ['genre_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('music', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('genre_id')

    op.drop_table('genre')
    # ### end Alembic commands ###