"""empty message

Revision ID: ab3cd959f553
Revises: b98edd768afd
Create Date: 2021-03-22 12:38:44.407837

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ab3cd959f553'
down_revision = 'b98edd768afd'
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