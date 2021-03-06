"""adds created at field for program reviews

Revision ID: 61e88a08d5ae
Revises: 49f02f844cb6
Create Date: 2020-04-25 21:31:01.425232

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61e88a08d5ae'
down_revision = '49f02f844cb6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('program_reviews', sa.Column('created_at', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('program_reviews', 'created_at')
    # ### end Alembic commands ###
