-- create dummy users
INSERT INTO
    stronk_user (id, name, username, email, current_program)
VALUES
    (
        'user_id_1',
        'max b wavy',
        'mxwvy',
        'max.wavy@gmail.com',
        NULL
    ),
    (
        'user_id_2',
        'jason cheung',
        'kakit',
        'ka.kit@gmail.com',
        NULL
    ),
    (
        'user_id_3',
        'richard wei',
        'chengchu',
        'richard.wei@gmail.com',
        NULL
    ),
    (
        'user_id_4',
        'test name',
        'test username',
        'test@email.com',
        NULL
    );

-- create dummy programs
INSERT INTO
    program (author, name, duration, description)
VALUES
    (
        'user_id_1',
        'max''s program',
        10,
        'dummy description 3'
    ),
    (
        'user_id_2',
        'jason''s program',
        10,
        'dummy description 2'
    ),
    (
        'user_id_3',
        'richard''s program',
        10,
        'dummy description 1'
    );

-- disable integrity checks for exercise table
ALTER TABLE exercise DISABLE TRIGGER ALL;

-- create dummy exercises
INSERT INTO
    exercise (name, description, author)
VALUES
    ('bicep curls', 'bicep curls description', 'user_id_1'),
    ('squats', 'squats description', 'user_id_1'),
    ('pullups', 'pullups curls description', 'user_id_1');

-- enable integrity checks for exercise table
ALTER TABLE exercise ENABLE TRIGGER ALL;

-- create dummy workouts
INSERT INTO
    workout (name, author, description, projected_time, scheduled_time)
VALUES
    (
        'workout 1',
        'user_id_1',
        'workout 1 description',
        10,
        '2020-12-17 12:00:00'
    ),
    (
        'workout 2',
        'user_id_2',
        'workout 2 description',
        11,
        '2020-12-18 12:00:00'
    ),
    (
        'workout 3',
        'user_id_3',
        'workout 3 description',
        12,
        '2020-12-25 12:00:00'
    ),
    (
        'workout 4',
        'user_id_4',
        'has not exercises',
        12,
        '2020-7-17 12:00:00'
    );

-- create dummy program reviews
INSERT INTO
    program_reviews (program_id, reviewer_id, rating, comments, created_at)
VALUES
    (1, 'user_id_1', 5, 'Best program!', '2020-03-17 12:00:00'),
    (1, 'user_id_2', 4, 'Amazing!', '2020-03-18 13:00:00'),
    (2, 'user_id_2', 5, 'The best!', '2020-04-01 14:00:00'),
    (3, 'user_id_3', 4, 'Great!', '2020-04-02 15:00:00');

-- update program with new workouts
INSERT INTO
    program_workouts (program_id, workout_id)
VALUES
    (1, 1),
    (2, 2),
    (3, 3);

-- update users with new program
UPDATE
    stronk_user
SET
    current_program = 1
WHERE
    id = 'user_id_1';

UPDATE
    stronk_user
SET
    current_program = 2
WHERE
    id = 'user_id_2';

UPDATE
    stronk_user
SET
    current_program = 3
WHERE
    id = 'user_id_3';

-- assign workout exercises to workouts
INSERT INTO
    workout_exercise (
        workout_id,
        exercise_id,
        workout_weights,
        workout_reps,
        rest_time
    )
VALUES
    (1, 1, '{10.0, 10.0, 10.0}', '{10, 10, 10}', 10),
    (1, 2, '{10.0, 10.0, 10.0}', '{10, 10, 10}', 10),
    (1, 3, '{10.0, 10.0, 10.0}', '{10, 10, 10}', 10),
    (2, 1, '{10.0, 10.0, 10.0}', '{10, 10, 10}', 10),
    (2, 2, '{10.0, 10.0, 10.0}', '{10, 10, 10}', 10),
    (2, 3, '{10.0, 10.0, 10.0}', '{10, 10, 10}', 10),
    (3, 1, '{10.0, 10.0, 10.0}', '{10, 10, 10}', 10),
    (3, 2, '{10.0, 10.0, 10.0}', '{10, 10, 10}', 10),
    (3, 3, '{10.0, 10.0, 10.0}', '{10, 10, 10}', 10);