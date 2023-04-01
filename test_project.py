import pytest
import project as pr
from game_classes import Mystery, Weapon, Player , Enemy


# example map for testing
mapd_test= """
      _____________________        
     │ !         !        !│_______
┌────┘   ┌─────┐   ┌────┐ *   +  # 
│x     ? │     │   |____├──────────
├────┐   │_____│ ?             +  #
     │ !     ? ├───────────────────
     ├─────┐   │___________________
           │ *                 +  #
           ├───────────────────────
"""[1:]

# test classes
pure_soul = Mystery("Pure Soul", "self", {"aura_density":4}, 0, False)
horizontal_slash = Mystery("horizontal slash", "enemy", {"health":-75}, 100, True)
test_weapon = Weapon("test_weapon", 1, [horizontal_slash])
player = Player("Test_player", 10, 10, 10, 10, 10,test_weapon,[pure_soul])
enemy = Enemy("Test_enemy", 10, 10, 8, 10, 10,test_weapon,[pure_soul])
enemy_two = Enemy("Test_enemy", 10, 10, 15, 10, 10,test_weapon,[pure_soul])

# Test the get_map function
def test_get_map():
    assert pr.get_map(3) == "end"
    assert pr.get_map(1) == """
      _____________________        
     │ !         !        !│_______
┌────┘   ┌─────┐   ┌────┐ *   +  # 
│x     ? │     │   |____├──────────
├────┐   │_____│ ?             +  #
     │ !     ? ├───────────────────
     ├─────┐   │___________________
           │ *                 +  #
           ├───────────────────────
"""[1:]
# Test the movement_system function
def test_movement_system(monkeypatch):
    user_input = "1"
    expected_output = "?"
    monkeypatch.setattr('builtins.input', lambda _: user_input)
    # call the function and check the output
    assert pr.movement_system(mapd_test) == expected_output

    user_input = iter(["2", "1"])
    expected_output = "?"
    monkeypatch.setattr('builtins.input', lambda _: next(user_input))
    # call the function and check the output
    assert pr.movement_system(mapd_test) == expected_output

# Test the create_evenmy function
def test_create_enemy():
    # test the enemy creation
    assert pr.create_enemies(stage=2,event="!")[0].name == "Dungeon Crawler"
    # test the number of enemies
    assert len(pr.create_enemies(stage=3,event="!")) == 2
    # test the type of the enemy
    assert pr.create_enemies(stage=3,event="*")[-1].name == "Archdemon Crawler"


def test_create_random_weapon(monkeypatch):
    user_input = "y"
    monkeypatch.setattr('builtins.input', lambda _: user_input)
    pr.create_random_weapon(player,1.2,[pure_soul])
    # test is weapon changed
    assert player.weapon.name != "test_weapon"
    assert player.weapon.aura_affinity == 1.2
    # test is player take the weapon's mystery
    assert pure_soul in player.passive_mysteries.values()

# test the check_battle_queue function
def test_check_battle_queue():
    enemies = [enemy,enemy_two]
    assert pr.check_battle_queue(player,enemies) == [enemy_two,player,enemy]


def test_campfire_system(monkeypatch):
     health_before = player.complex_stats["health"]
     user_input = "y"
     monkeypatch.setattr('builtins.input', lambda _: user_input)
     pr.campfire_system(player)
     assert player.complex_stats["health"] > health_before