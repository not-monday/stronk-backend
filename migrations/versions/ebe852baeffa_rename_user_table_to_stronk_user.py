"""rename user table to stronk_user

Revision ID: ebe852baeffa
Revises: 61e88a08d5ae
Create Date: 2020-05-05 13:07:00.078988

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ebe852baeffa'
down_revision = '61e88a08d5ae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stronk_user',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('current_program', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['current_program'], ['program.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_stronk_user_email'), 'stronk_user', ['email'], unique=True)
    op.create_index(op.f('ix_stronk_user_name'), 'stronk_user', ['name'], unique=False)
    op.create_index(op.f('ix_stronk_user_username'), 'stronk_user', ['username'], unique=True)
    op.drop_index('ix_user_email', table_name='user')
    op.drop_index('ix_user_name', table_name='user')
    op.drop_index('ix_user_username', table_name='user')
    op.drop_constraint('author_id', 'program', type_='foreignkey')
    op.create_foreign_key('author_id', 'program', 'stronk_user', ['author'], ['id'])
    op.drop_constraint('program_reviews_reviewer_id_fkey', 'program_reviews', type_='foreignkey')
    op.create_foreign_key('program_reviews_reviewer_id_fkey', 'program_reviews', 'stronk_user', ['reviewer_id'], ['id'])
    op.drop_constraint('weight_user_id_fkey', 'weight', type_='foreignkey')
    op.create_foreign_key('weight_user_id_fkey', 'weight', 'stronk_user', ['user_id'], ['id'])
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(length=64), autoincrement=False, nullable=False),
    sa.Column('username', sa.VARCHAR(length=64), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('current_program', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['current_program'], ['program.id'], name='current_program_id', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='user_pkey')
    )
    op.drop_constraint('weight_user_id_fkey', 'weight', type_='foreignkey')
    op.create_foreign_key('weight_user_id_fkey', 'weight', 'user', ['user_id'], ['id'])
    op.drop_constraint('program_reviews_reviewer_id_fkey', 'program_reviews', type_='foreignkey')
    op.create_foreign_key('program_reviews_reviewer_id_fkey', 'program_reviews', 'user', ['reviewer_id'], ['id'])
    op.drop_constraint('author_id', 'program', type_='foreignkey')
    op.create_foreign_key('author_id', 'program', 'user', ['author'], ['id'], ondelete='CASCADE')
    op.create_index('ix_user_username', 'user', ['username'], unique=True)
    op.create_index('ix_user_name', 'user', ['name'], unique=False)
    op.create_index('ix_user_email', 'user', ['email'], unique=True)
    op.drop_index(op.f('ix_stronk_user_username'), table_name='stronk_user')
    op.drop_index(op.f('ix_stronk_user_name'), table_name='stronk_user')
    op.drop_index(op.f('ix_stronk_user_email'), table_name='stronk_user')
    op.drop_table('stronk_user')
    # ### end Alembic commands ###
