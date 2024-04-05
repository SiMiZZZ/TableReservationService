"""add relationship from restaurant to user

Revision ID: 763c36193ffc
Revises: b280edff7d35
Create Date: 2024-03-31 01:28:29.743456

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '763c36193ffc'
down_revision = 'b280edff7d35'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('restaurants',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('latitude', sa.LargeBinary(), nullable=True),
    sa.Column('longitude', sa.LargeBinary(), nullable=True),
    sa.Column('account_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['account_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_restaurants_id'), 'restaurants', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_restaurants_id'), table_name='restaurants')
    op.drop_table('restaurants')
    # ### end Alembic commands ###