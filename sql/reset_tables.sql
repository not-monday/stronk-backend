 TRUNCATE alembic_version CASCADE;
 TRUNCATE program CASCADE;
 TRUNCATE workout_exercise CASCADE;
 TRUNCATE exercise CASCADE;
 TRUNCATE workout CASCADE;
 TRUNCATE program_workouts CASCADE;
 TRUNCATE weight CASCADE;
 TRUNCATE program_reviews CASCADE;
 TRUNCATE stronk_user CASCADE;

ALTER SEQUENCE exercise_id_seq RESTART;
ALTER SEQUENCE program_id_seq RESTART;
ALTER SEQUENCE workout_id_seq RESTART;
