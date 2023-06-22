## SQL commands for */tictactoe* route:

```bash
CREATE DATABASE tictactoe;

USE tictactoe;

CREATE TABLE rooms ( 
    room_code INT PRIMARY KEY, 
    start_time DATETIME,
    end_time DATETIME,
    occupied BOOLEAN DEFAULT FALSE,
    token CHAR(20)
);

INSERT IGNORE INTO
rooms (room_code, start_time, end_time)
VALUES (1000, NOW(), NOW());

COMMIT;
```