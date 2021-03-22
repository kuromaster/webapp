"""empty message

Revision ID: 49c3b9a26d68
Revises: 03d636bbc8b5
Create Date: 2021-03-22 12:37:36.977757

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '49c3b9a26d68'
down_revision = '03d636bbc8b5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password1', sa.String(length=255), nullable=True))
    op.drop_column('user', 'password')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password', mysql.VARCHAR(length=255), nullable=True))
    op.drop_column('user', 'password1')
    # ### end Alembic commands ###
