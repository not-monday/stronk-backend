"""creates weight model

Revision ID: 49f02f844cb6
Revises: 81afd06c3578
Create Date: 2020-04-25 20:05:36.748809

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49f02f844cb6'
down_revision = '81afd06c3578'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('weight',
                    sa.Column('user_id', sa.String(), nullable=False),
                    sa.Column('weight', sa.Float(), nullable=False),
                    sa.Column('measured_at', sa.DateTime(
                        timezone=True), nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('user_id', 'measured_at')
                    )
    op.create_index(op.f('ix_weight_user_id'),
                    'weight', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_weight_user_id'), table_name='weight')
    op.drop_table('weight')
    # ### end Alembic commands ###
