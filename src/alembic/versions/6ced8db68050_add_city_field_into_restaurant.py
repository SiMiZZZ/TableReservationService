"""add city field into restaurant

Revision ID: 6ced8db68050
Revises: dea678593881
Create Date: 2024-03-31 03:00:00.843795

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6ced8db68050'
down_revision = 'dea678593881'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('restaurants', sa.Column('city', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('restaurants', 'city')
    # ### end Alembic commands ###