-- create dummy users
INSERT INTO stronk_user (id, name, username, email, current_program)
VALUES('user_id_1', 'max b wavy', 'mxwvy', 'max.wavy@gmail.com', NULL);

INSERT INTO stronk_user (id, name, username, email, current_program)
VALUES('user_id_2', 'jason cheung', 'kakit', 'ka.kit@gmail.com', NULL);

INSERT INTO stronk_user (id, name, username, email, current_program)
VALUES('user_id_3', 'richard wei', 'chengchu','richard.wei@gmail.com', NULL);

-- create dummy programs
INSERT INTO program (id, author, name, duration, description)
VALUES(0, 'user_id_1', 'max''s program', 10, 'dummy description 3');

INSERT INTO program (id, author, name, duration, description)
VALUES(1, 'user_id_2', 'jason''s program', 10, 'dummy description 2');

INSERT INTO program (id, author, name, duration, description)
VALUES(2, 'user_id_3', 'richard''s program', 10, 'dummy description 1');

-- create dummy exercises
INSERT INTO EXERCISE (id, name, description)
VALUES(0, 'bicep curls', 'bicep curls description');
INSERT INTO EXERCISE (id, name, description)
VALUES(1, 'squats', 'squats description');
INSERT INTO EXERCISE (id, name, description)
VALUES(2, 'pullups', 'pullups curls description');

-- update users with new program
UPDATE stronk_user SET current_program = 0 WHERE id = 'user_id_1';
UPDATE stronk_user SET current_program = 1 WHERE id = 'user_id_2';
UPDATE stronk_user SET current_program = 2 WHERE id = 'user_id_3';