# -*- coding:utf-8 -*-

sql_create_id_generator = """
create table IF NOT EXISTS id_generator
(
  AUTO_INC_ID bigint not null,
  TYPE int not null,
  SERVER_ID int not null,
  RUNING_FLAG int not null,
  primary key(TYPE, SERVER_ID)
)ENGINE=INNODB DEFAULT CHARSET=utf8;
"""

sql_create_account = """
create table IF NOT EXISTS account
(
  ACCOUNT_ID varchar(24) not null,
  SESSION_ID bigint not null,
  SESSION_UPD_TIME timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CREATE_DATA datetime default null,
  primary key(ACCOUNT_ID)
)ENGINE=INNODB DEFAULT CHARSET=utf8;
"""

sql_create_account = """
create table IF NOT EXISTS gm_token
(
  TOKEN_ID varchar(100),
  primary key(TOKEN_ID)
)ENGINE=INNODB DEFAULT CHARSET=utf8;
"""

# ALTER TABLE `account` ADD INDEX account_search ( `ACCOUNT_ID` );


sql_create_player_base = """
create table IF NOT EXISTS player
(
  SESSION_ID bigint not null,
  DATA_INFO_BASE JSON,
  DATA_INFO JSON,
  primary key(SESSION_ID)
)ENGINE=INNODB DEFAULT CHARSET=utf8;
"""

# ALTER TABLE `player` ADD INDEX player_search ( `SESSION_ID` );

sql_create_account = """
create table IF NOT EXISTS game_config
(
  CONFIG_ID bigint not null,
  CONFIG_DATA JSON,
  primary key(CONFIG_ID)
)ENGINE=INNODB DEFAULT CHARSET=utf8;
"""



