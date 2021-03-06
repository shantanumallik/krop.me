"""empty message

Revision ID: 3b5092f3129c
Revises: 
Create Date: 2020-05-03 22:34:14.524835

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b5092f3129c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('url_map',
    sa.Column('short_url', sa.String(length=50), nullable=False),
    sa.Column('long_url', sa.String(length=200), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('expiry', sa.Integer(), nullable=True),
    sa.Column('visit_count', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('short_url')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('url_map')
    # ### end Alembic commands ###
