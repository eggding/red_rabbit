
class player_mgr_t:
    def __init__(self):
        self.all_players = {}
    def get(self, session_id_):
        return self.all_players.get(session_id_)
    def remove(self, session_id_):
        if None != self.all_players.get(session_id_):
            del  self.all_players[session_id_]
    def add(self, session_id_, player):
        self.all_players[session_id_] = player
    def size(self):
        return len(self.all_players)
    def idlist(self):
        return self.all_players.keys()

class player_t:
    def __init__(self, session_id_=0):
        self.session_id = session_id_
        self.extra_data = ''
        self.online_time = 0
        self.ip         = ''
        self.gate_name  = ''

    def id(self):
        return self.session_id

    def set_id(self, id_):
        self.session_id = id_

