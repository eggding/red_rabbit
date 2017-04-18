DROP FUNCTION IF EXISTS `json_object`;
create function json_object returns string soname 'udf_json.so';


use phpwind;

DELIMITER |

DROP TRIGGER IF EXISTS sync_redis_insert;
CREATE TRIGGER sync_redis_insert
AFTER INSERT ON pw_threads
FOR EACH ROW BEGIN
    SET @tt_json = (SELECT json_object(tid,fid,icon,author,authorid,subject,toolinfo,toolfield,ifcheck,type,postdate,replies,favors,modelid,shares,topped,topreplays,locked,digest,special,state,ifupload,ifmail,ifmark,ifshield,anonymous,dig,fight,ptable,ifmagic,ifhide,inspect,tpcstatus) FROM pw_threads WHERE tid = NEW.tid LIMIT 1); 
    SET @tt_con  = (SELECT redis_connect("127.0.0.1",6378));
    SET @tt_resu = (SELECT redis_pipe(CONCAT("SET pw_threads_hits_",NEW.tid," ",NEW.hits,"\r\n","SET pw_threads_lastpost_",NEW.tid," ",NEW.lastpost,"\r\n","SET pw_threads_lastposter_",NEW.tid," ",NEW.lastposter,"\r\n","LPUSH pw_threads_",NEW.fid," ",NEW.tid,"\r\n","SET pw_threads_",NEW.tid," ",@tt_json,"\r\n")));

END |


DELIMITER ;


# UPDATE���²����Ĵ����� titlefont   
/*
DELIMITER |   
DROP TRIGGER IF EXISTS sync_redis_update;   
CREATE TRIGGER sync_redis_update   
AFTER UPDATE ON pw_threads   
FOR EACH ROW BEGIN   
    SET @tt_json = (SELECT json_object(tid,fid,icon,author,authorid,subject,toolinfo,toolfield,ifcheck,type,postdate,replies,favors,modelid,shares,topped,topreplays,locked,digest,special,state,ifupload,ifmail,ifmark,ifshield,anonymous,dig,fight,ptable,ifmagic,ifhide,inspect,tpcstatus) FROM pw_threads WHERE tid = NEW.tid LIMIT 1); 
    SET @tt_con  = (SELECT redis_connect("127.0.0.1",6378));
    SET @tt_resu = (SELECT redis_pipe(CONCAT("SET pw_threads_hits_",NEW.tid," ",NEW.hits,"\r\n","SET pw_threads_lastpost_",NEW.tid," ",NEW.lastpost,"\r\n","SET pw_threads_lastposter_",NEW.tid," ",NEW.lastposter,"\r\n","SET pw_threads_",NEW.tid," ",@tt_json,"\r\n")));
 
END |   
DELIMITER ;  
*/
/* DELETEɾ�������Ĵ����� */   
/*
DELIMITER |   
DROP TRIGGER IF EXISTS sync_redis_delete;   
CREATE TRIGGER sync_redis_delete   
AFTER DELETE ON pw_threads   
FOR EACH ROW BEGIN   
    SET @tt_con  = (SELECT redis_connect("127.0.0.1",6378));
    SET @tt_resu = (SELECT redis_pipe(CONCAT("DEL pw_threads_hits_",OLD.tid,"\r\n","DEL pw_threads_lastpost_",OLD.tid,"\r\n","DEL pw_threads_lastposter_",OLD.tid,"\r\n","RPUSH pw_threads_",NEW.fid," ",NEW.tid,"\r\n","DEL pw_threads_",OLD.tid,"\r\n")));
#    SET @tt_resu = (SELECT http_delete(CONCAT('http://192.168.8.34:1978/', OLD.id)));   
END |   
DELIMITER ;  

*/
