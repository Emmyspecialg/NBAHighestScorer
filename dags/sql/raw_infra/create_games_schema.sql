create table
    if not exists scoresheets_raw (
        id VARCHAR(25),
        first_name VARCHAR(100),
        last_name VARCHAR(100),
        points INTEGER
    )