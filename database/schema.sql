CREATE TABLE IF NOT EXISTS `temperature_readings` (
    id SERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    temp_c FLOAT NOT NULL,
    timestamp TIMESTAMP NOT NULL
)