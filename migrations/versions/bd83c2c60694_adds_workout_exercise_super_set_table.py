"""adds workout exercise super set table

Revision ID: bd83c2c60694
Revises: 211a741538ed
Create Date: 2020-03-17 02:31:46.576805

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bd83c2c60694'
down_revision = '211a741538ed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('workout_exercise_super_sets',
    sa.Column('src_workout_id', sa.Integer(), nullable=False),
    sa.Column('src_exercise_id', sa.Integer(), nullable=False),
    sa.Column('super_set_exercise_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['src_exercise_id'], ['exercise.id'], ),
    sa.ForeignKeyConstraint(['src_workout_id'], ['workout.id'], ),
    sa.ForeignKeyConstraint(['super_set_exercise_id'], ['exercise.id'], ),
    sa.PrimaryKeyConstraint('src_workout_id', 'src_exercise_id', 'super_set_exercise_id')
    )
    op.create_index(op.f('ix_workout_exercise_super_sets_src_exercise_id'), 'workout_exercise_super_sets', ['src_exercise_id'], unique=False)
    op.create_index(op.f('ix_workout_exercise_super_sets_src_workout_id'), 'workout_exercise_super_sets', ['src_workout_id'], unique=False)
    op.create_index(op.f('ix_workout_exercise_super_sets_super_set_exercise_id'), 'workout_exercise_super_sets', ['super_set_exercise_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_workout_exercise_super_sets_super_set_exercise_id'), table_name='workout_exercise_super_sets')
    op.drop_index(op.f('ix_workout_exercise_super_sets_src_workout_id'), table_name='workout_exercise_super_sets')
    op.drop_index(op.f('ix_workout_exercise_super_sets_src_exercise_id'), table_name='workout_exercise_super_sets')
    op.drop_table('workout_exercise_super_sets')
    # ### end Alembic commands ###
