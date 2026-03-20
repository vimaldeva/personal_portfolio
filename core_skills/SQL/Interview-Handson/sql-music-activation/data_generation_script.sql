CREATE TABLE users
(
    user_id   INTEGER,
    name      VARCHAR(20),
    join_date DATE
);

INSERT INTO users VALUES 
(1, 'Jon',    '2020-02-14'), 
(2, 'Jane',   '2020-02-14'), 
(3, 'Jill',   '2020-02-15'), 
(4, 'Josh',   '2020-02-15'), 
(5, 'Jean',   '2020-02-16'), 
(6, 'Justin', '2020-02-17'),
(7, 'Jeremy', '2020-02-18');

CREATE TABLE events
(
    user_id     INTEGER,
    type        VARCHAR(10),
    access_date DATE
);

INSERT INTO events VALUES
(1, 'Pay',   '2020-03-01'), 
(2, 'Music', '2020-03-02'), 
(2, 'P',     '2020-03-12'),
(3, 'Music', '2020-03-15'), 
(4, 'Music', '2020-03-15'), 
(1, 'P',     '2020-03-16'), 
(3, 'P',     '2020-03-22');
