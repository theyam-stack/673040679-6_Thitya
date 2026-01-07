from P3_method import VideoGame

p1 = VideoGame("Ditto23", "Princess")
p2 = VideoGame("MaryPotter", "Trianee Wizard")
p3 = VideoGame("SylusDevill666", "Dark Knight")

print("\t=== Server Info ===")
print(VideoGame.get_server_stats())

print("\n\t=== Actions ===")
p1.collect_coins(150)
p1.fight_monster("Momin Big Fat Cat", 2)
p1.fight_monster("Salit Catly Dragon", 5)
p1.level = 23
VideoGame.leaderboard[p1.name] = p1.level * 100 + p1.coins
print(f"{p1.name} has been boosted to level {p1.level}!")

p2.fight_monster("Salit Catly Dragon", 5)
p2.take_damage(30)
p2.collect_coins(888)
p2.level = 50
p2.hp = 100
VideoGame.leaderboard[p2.name] = p2.level * 100 + p2.coins
print(f"{p2.name} has been boosted to level {p2.level}!")

p3.level = 66
p3.fight_monster("Dark Lord Tigerrr", 10)
p3.take_damage(120)
p3.collect_coins(66)
VideoGame.leaderboard[p3.name] = p3.level * 100 + p3.coins

print("\n\t=== Stats ===")
print(p1.get_stats())
print(p2.get_stats())
print(p3.get_stats())

print("\n=== Leaderboard ===")
print(VideoGame.get_leaderboard())

print("\n=== Reset ===")
VideoGame.reset_server()
print(VideoGame.get_server_stats())