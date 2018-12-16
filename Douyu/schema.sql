drop table if exists Lottery;           -- if exists , drop
create table Lottery (
  id INTEGER PRIMARY KEY autoincrement, -- id,autoincrement
  room_id VARCHAR(32) NOT NULL ,        -- room id
  room_name VARCHAR(255) ,              -- room name
  prize_name VARCHAR(255) ,             -- prize name
  prize_num VARCHAR(32),                -- prize num
  lottery_range VARCHAR(255),           -- lottery type 0,1,2,3
  start_time TIMESTAMP ,                -- start time
  command_content VARCHAR(255),         -- lottery command
  insert_time TIMESTAMP  DEFAULT (datetime(CURRENT_TIMESTAMP ,'localtime'))   -- insert time
);

-- auto-generated definition
CREATE INDEX Lottery_start_time_index
  ON Lottery (start_time DESC);
