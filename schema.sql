DROP TABLE IF EXISTS logs;
CREATE TABLE logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    log_date DATE NOT NULL,
    category TEXT NOT NULL,
    duration_minutes INTEGER,
    notes TEXT
);