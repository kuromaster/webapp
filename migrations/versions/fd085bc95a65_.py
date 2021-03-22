"""empty message

Revision ID: fd085bc95a65
Revises: 29dd38fd1958
Create Date: 2021-03-21 15:09:45.427105

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fd085bc95a65'
down_revision = '29dd38fd1958'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('group',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('slug', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('lastname', sa.String(length=50), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('login', sa.String(length=20), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('status', sa.String(length=15), nullable=True),
    sa.Column('lastsession', sa.DateTime(), nullable=True),
    sa.Column('pkey', sa.String(length=250), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('group_membership',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('group_membership')
    op.drop_table('user')
    op.drop_table('group')
    # ### end Alembic commands ###
