"""empty message

Revision ID: 0382a9ebbc85
Revises: 9365c53dabd4
Create Date: 2021-03-11 20:16:45.943476

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0382a9ebbc85'
down_revision = '9365c53dabd4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'tag', ['name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tag', type_='unique')
    # ### end Alembic commands ###