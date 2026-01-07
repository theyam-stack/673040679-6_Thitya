# P3 Lab 4-2
from datetime import datetime

class VideoGame:
    # server-wide stuff
    total_players = 0
    difficulty_levels = ["Easy", "Medium", "Hard"]
    max_level = 100
    server_start_time = datetime.now()
    active_players = []
    leaderboard = {}

    def __init__(self, name, char_type):
        # quick validation
        if not VideoGame.is_valid_character_name(name):
            raise ValueError("Bad name: must be 3-20 chars, only letters/numbers")

        # basic stats
        self.name = name
        self.char_type = char_type
        self.level = 1
        self.hp = 100
        self.exp = 0
        self.coins = 0
        self.items = []   # inventory
        self.alive = True

        # update server info
        VideoGame.total_players += 1
        VideoGame.active_players.append(self.name)
        VideoGame.leaderboard[self.name] = 0

    # instance methods
    def level_up(self):
        if self.level < VideoGame.max_level:
            self.level += 1
            self.hp = 100
            # score formula is kinda arbitrary
            VideoGame.leaderboard[self.name] = self.level * 100 + self.coins
            print(f"{self.name} leveled up! Lv={self.level}, HP={self.hp}, Score={VideoGame.leaderboard[self.name]}")
        else:
            print(f"{self.name} already max level!")

    def collect_coins(self, amt):
        self.coins += amt
        VideoGame.leaderboard[self.name] = self.level * 100 + self.coins
        print(self.name, "now has", self.coins, "coins. Score:", VideoGame.leaderboard[self.name])

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.hp = 0
            self.alive = False
            if self.name in VideoGame.active_players:
                VideoGame.active_players.remove(self.name)
            print(self.name, "died... RIP")
        else:
            print(self.name, "took", dmg, "damage. HP left:", self.hp)

    def fight_monster(self, monster, m_lvl, atk=10, defense=5):
        if not self.alive:
            print(self.name, "can't fight, already dead.")
            return

        dmg = VideoGame.calculate_damage(atk, defense, m_lvl)
        self.take_damage(dmg)

        if self.alive:
            gained_exp = 10 * m_lvl
            self.exp += gained_exp
            gained_coins = 3 * m_lvl
            self.collect_coins(gained_coins)

            print(f"{self.name} fought {monster} (Lv{m_lvl}) → dmg={dmg}, exp+{gained_exp}, coins+{gained_coins}")

            if self.exp >= VideoGame.calculate_exp_needed(self.level):
                # reset exp after level up
                self.exp = 0
                self.level_up()

    def get_stats(self):
        return f"""
        Player: {self.name}
        Job: {self.char_type}
        Level: {self.level} ({VideoGame.get_rank_title(self.level)})
        HP: {self.hp}
        EXP: {self.exp}
        Coins: {self.coins}
        Alive: {self.alive}
        """

    # class methods
    @classmethod
    def create_party(cls, names, char_type):
        party = []
        for n in names:
            party.append(cls(n, char_type))
        return party

    @classmethod
    def get_server_stats(cls):
        uptime = datetime.now() - cls.server_start_time
        return f"""
        Server Stats:
        Total Players: {cls.total_players}
        Active: {cls.active_players}
        Leaderboard: {cls.leaderboard}
        Uptime: {uptime}
        """

    @classmethod
    def get_leaderboard(cls):
        sorted_lb = sorted(cls.leaderboard.items(), key=lambda x: x[1], reverse=True)
        out = "Leaderboard:\n"
        for i, (p, s) in enumerate(sorted_lb):
            out += f"{i+1}. {p} → {s}\n"
        return out

    @classmethod
    def reset_server(cls):
        cls.total_players = 0
        cls.active_players = []
        cls.leaderboard = {}
        cls.server_start_time = datetime.now()
        print("Server reset.")

    # static methods
    @staticmethod
    def calculate_damage(atk, defense, lvl):
        dmg = (atk * lvl) - defense
        if dmg < 0:
            dmg = 0
        return dmg

    @staticmethod
    def calculate_exp_needed(lvl):
        return 100 * lvl

    @staticmethod
    def is_valid_character_name(name):
        return 3 <= len(name) <= 20 and name.isalnum()

    @staticmethod
    def get_rank_title(lvl):
        if lvl < 10:
            return "Noob"
        elif lvl < 30:
            return "Adventurer"
        elif lvl < 60:
            return "Warrior"
        elif lvl < 90:
            return "Hero"
        else:
            return "Legend"