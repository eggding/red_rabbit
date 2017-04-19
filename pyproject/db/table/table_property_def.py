import entity.const_entity as const_entity

class MemoryAttr(const_entity.Const):
    GATE = "g"
    IP = "ip"
    ONLINE_TIME = "ot"

class TableName(const_entity.Const):
    PLAYER_MONEY = "player_money"

class Player(const_entity.Const):
    SESSION_ID = "SESSION_ID"
    NAME = "name"
    SEX = "sex"
    CREATE_TIME = "create_time"
    MONEY_LIST = "money_list"

    # memory
    IP = "ip"
    GATE_NAME = "gate"

