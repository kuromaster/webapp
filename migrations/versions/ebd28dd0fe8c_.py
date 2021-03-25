"""empty message

Revision ID: ebd28dd0fe8c
Revises: 9189075e5c56
Create Date: 2021-03-23 15:31:12.766009

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ebd28dd0fe8c'
down_revision = '9189075e5c56'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('l1ogin_count', sa.Integer(), nullable=True))
    op.drop_column('user', 'login_count')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('login_count', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('user', 'l1ogin_count')
    # ### end Alembic commands ###