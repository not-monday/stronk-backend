"""create program reviews table

Revision ID: 81afd06c3578
Revises: e2b92f1dd2c3
Create Date: 2020-04-25 19:28:59.656695

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81afd06c3578'
down_revision = 'e2b92f1dd2c3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('program_reviews',
                    sa.Column('program_id', sa.Integer(), nullable=False),
                    sa.Column('reviewer_id', sa.String(), nullable=False),
                    sa.Column('rating', sa.Integer(), nullable=False),
                    sa.Column('comments', sa.String(
                        length=250), nullable=False),
                    sa.CheckConstraint('rating <= 5 AND rating > 0'),
                    sa.ForeignKeyConstraint(['program_id'], ['program.id'], ),
                    sa.ForeignKeyConstraint(['reviewer_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('program_id', 'reviewer_id')
                    )
    op.create_index(op.f('ix_program_reviews_program_id'),
                    'program_reviews', ['program_id'], unique=False)
    op.create_index(op.f('ix_program_reviews_reviewer_id'),
                    'program_reviews', ['reviewer_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_program_reviews_reviewer_id'),
                  table_name='program_reviews')
    op.drop_index(op.f('ix_program_reviews_program_id'),
                  table_name='program_reviews')
    op.drop_table('program_reviews')
    # ### end Alembic commands ###
