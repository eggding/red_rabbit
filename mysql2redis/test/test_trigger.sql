use red_rabbit;

DROP TRIGGER  IF EXISTS playerUpd2Redis;

DELIMITER |
create trigger playerUpd2Redis AFTER INSERT on player
  For EACH ROW BEGIN
-- DECLARE done INT DEFAULT 999; 
set done = redis_command("127.0.0.1",6379,concat("hset ", 123, " player ", "{name:}"));
END;
|
DELIMITER ;

