"""remove primary key program_id in program_workouts

Revision ID: a746f816802c
Revises: ebe852baeffa
Create Date: 2020-05-30 01:01:21.964897

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a746f816802c'
down_revision = 'ebe852baeffa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("program_workouts_pkey",
                       "program_workouts", type_="primary")
    op.create_primary_key("program_workouts_pkey",
                          "program_workouts", ["workout_id"])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("program_workouts_pkey",
                       "program_workouts", type_="primary")
    op.create_primary_key("program_workouts_pkey", "program_workouts", [
                          "program_id", "workout_id"])
    # ### end Alembic commands ###
