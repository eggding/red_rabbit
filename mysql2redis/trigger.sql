use red_rabbit;

DELIMITER |
DROP TRIGGER IF EXISTS player_sync_redis_insert;
CREATE TRIGGER player_sync_redis_insert
AFTER INSERT ON player
FOR EACH ROW BEGIN
    SET @tt_json = (SELECT json_object(SESSION_ID, NAME, SEX) FROM player WHERE SESSION_ID = NEW.SESSION_ID);
    SET @ret = (SELECT redis_command("127.0.0.1", 6379, concat("hset ", NEW.SESSION_ID, " player ", @tt_json)));
END |
DELIMITER ;

-- SET @tt_json = (SELECT json_object(SESSION_ID, NAME, SEX) FROM player WHERE SESSION_ID = 393);
-- select redis_command("127.0.0.1", 6379, concat("hset ", 393, " player ", @tt_json));