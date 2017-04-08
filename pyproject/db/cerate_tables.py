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

# ALTER TABLE `account` ADD INDEX account_search ( `ACCOUNT_ID` );


sql_create_player_base = """
create table IF NOT EXISTS player
(
  SESSION_ID bigint not null,
  NAME varchar(10) not null,
  SEX varchar(1) not null,
  CREATE_DATA datetime default null,
  primary key(SESSION_ID)
)ENGINE=INNODB DEFAULT CHARSET=utf8;
"""

sql_create_player_money = """
create table IF NOT EXISTS player_money
(
  SESSION_ID bigint not null,
  MONEY_TYPE int not null,
  MONEY_VALUE int not null,
  primary key(SESSION_ID)
)ENGINE=INNODB DEFAULT CHARSET=utf8;
"""


