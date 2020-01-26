"""create program and user table

Revision ID: 5a2a4aec69c5
Revises: 
Create Date: 2020-01-25 20:59:02.251829

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a2a4aec69c5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('program',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('author', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('duration', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=256), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_program_author'), 'program', ['author'], unique=False)
    op.create_index(op.f('ix_program_name'), 'program', ['name'], unique=True)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('current_program', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )

    # Create foreign keys
    op.create_foreign_key("author_id", "program", "user", ["author"], ["id"], ondelete='CASCADE')
    op.create_foreign_key("current_program_id", "user", "program", ["current_program"], ["id"], ondelete='CASCADE')

    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_name'), 'user', ['name'], unique=False)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("current_program_id", "user")
    op.drop_constraint("author_id", "program")
    op.drop_table('user')
    op.drop_table('program')
    # ### end Alembic commands ###
