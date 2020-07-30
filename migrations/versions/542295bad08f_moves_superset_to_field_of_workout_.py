"""moves superset to field of workout exercise

Revision ID: 542295bad08f
Revises: d873ed5a113c
Create Date: 2020-07-30 17:00:57.044501

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '542295bad08f'
down_revision = 'd873ed5a113c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_workout_exercise_super_sets_src_exercise_id', table_name='workout_exercise_super_sets')
    op.drop_index('ix_workout_exercise_super_sets_src_workout_id', table_name='workout_exercise_super_sets')
    op.drop_index('ix_workout_exercise_super_sets_super_set_exercise_id', table_name='workout_exercise_super_sets')
    op.drop_table('workout_exercise_super_sets')
    op.add_column('workout_exercise', sa.Column('superset_exercise_id', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_workout_exercise_superset_exercise_id'), 'workout_exercise', ['superset_exercise_id'], unique=False)
    op.create_foreign_key('superset_exercise_id_fk', 'workout_exercise', 'exercise', ['superset_exercise_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('superset_exercise_id_fk', 'workout_exercise', type_='foreignkey')
    op.drop_index(op.f('ix_workout_exercise_superset_exercise_id'), table_name='workout_exercise')
    op.drop_column('workout_exercise', 'superset_exercise_id')
    op.create_table('workout_exercise_super_sets',
    sa.Column('src_workout_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('src_exercise_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('super_set_exercise_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['src_exercise_id'], ['exercise.id'], name='workout_exercise_super_sets_src_exercise_id_fkey'),
    sa.ForeignKeyConstraint(['src_workout_id'], ['workout.id'], name='workout_exercise_super_sets_src_workout_id_fkey'),
    sa.ForeignKeyConstraint(['super_set_exercise_id'], ['exercise.id'], name='workout_exercise_super_sets_super_set_exercise_id_fkey'),
    sa.PrimaryKeyConstraint('src_workout_id', 'src_exercise_id', 'super_set_exercise_id', name='workout_exercise_super_sets_pkey')
    )
    op.create_index('ix_workout_exercise_super_sets_super_set_exercise_id', 'workout_exercise_super_sets', ['super_set_exercise_id'], unique=False)
    op.create_index('ix_workout_exercise_super_sets_src_workout_id', 'workout_exercise_super_sets', ['src_workout_id'], unique=False)
    op.create_index('ix_workout_exercise_super_sets_src_exercise_id', 'workout_exercise_super_sets', ['src_exercise_id'], unique=False)
    # ### end Alembic commands ###
