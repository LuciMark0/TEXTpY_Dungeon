from random import randint
from game_classes import Mystery, Weapon, Player , Enemy
# use tabulate to show stats

def main():
    global mapd
    level = 1
    mapd = get_map(level)
    # player_name = input("Name: ")
    # player = Creature(player_name,randint(5,15),randint(5,15),randint(50,150),randint(0,10))
    while True:
        event = movement_system()
        event_system(event)
# Set mysteries
pure_blood = Mystery("Pure Blood", "self", {"constitution":10}, 0, False)
pure_soul = Mystery("Pure Soul", "self", {"aura_density":10}, 0, False)
ticker_skin = Mystery("Ticker Skin","self", {"constitution":15}, 0, False)
blackfire = Mystery("black fire", "enemy", {"health":-25}, 100, True, 3, True)
fireball = Mystery("fire ball", "enemy", {"health":-10}, 50, True, 3, False)
quick_slice =  Mystery("quick slice", "enemy", {"health":-85}, 150, True)
little_blessing = Mystery("little blessing", "self", {"health":50}, 50, True, 3, False)
# Set weapons
katana = Weapon("Katana", 2, [fireball])
great_katana = Weapon("Great Katana", 10, [blackfire])
# Set player
player = Player("player", 15, 10, 10, 50, 8, katana, [ticker_skin]) 

def get_map(level):
    levels = ("""
      _____________________        
     │ !         !        !│_______
┌────┘   ┌─────┐   ┌────┐ *   +  # 
│x     ? │     │   |____├──────────
├────┐   │_____│ ?             +  #
     │ !     ? ├───────────────────
     ├─────┐   │___________________
           │ *                 +  #
           ├───────────────────────
""",
"""
     ___________________________________________
    |                                           
    |   ┌────────┐   ┌───┐   ┌─┐   ┌────────────
┌───┘   |________|   |___|   |_|   ├────────────
|x                                              
├───┐   ┌────────────────┐   ┌─────┐   ┌────────
    |   |_________       |   |_____|   |        
    |             |      |             |        
    ├─────────┐   |      |   ┌─────┐   |        
              |   |______|   |_____|   |________
              |                                 
              ├─────────────────────────────────
"""
    )
    return levels[level-1][1:]

def movement_system():
    global mapd
    player_location = mapd.find("x")
    print(mapd)

    available_ways = check_ways(mapd,player_location)
    way_choice = get_way_choice(available_ways)
    
    mapd = list(mapd)
    event = mapd[way_choice]
    mapd[way_choice] = "x"
    mapd[player_location] = "-"
    mapd = "".join(mapd)
    
    return event


def check_ways(mapd,player_location):
    walls = ("─","|","-","_","├","┘","┌","┐","┤")
    events = ("?","!","*","#","+")

    map_lines_len = len(mapd.split("\n")[0])+1 # +1 for splited "\n" character

    upper_locations = range(player_location,-1,-map_lines_len)
    lower_locations = range(player_location,len(mapd),map_lines_len)
    forward_locations = range(player_location,player_location+map_lines_len-player_location%map_lines_len-1)
    all_locaitons = (upper_locations, lower_locations, forward_locations)

    locations = 0
    down_location,up_location,forward_location = 0,0,0
    while locations < 3:
        for location in all_locaitons[locations]:
            if mapd[location] in events:
                locations += 1
                if locations == 2:
                    down_location = location
                elif locations == 1:
                    up_location = location
                else:
                    forward_location = location
                break
            elif mapd[location] in walls:
                locations += 1
                break

    ways = {"up":up_location,"forward":forward_location,"down":down_location}
    available_ways = {}
    
    for key,item in ways.items():
        if item != 0:
            available_ways[f"{key}"] = item

    return available_ways
    

def get_way_choice(available_ways):
    way_count = 0
    choices = {}

    for key,item in available_ways.items():
        way_count += 1
        print(f"{way_count} ==> {key}")
        choices[f"{way_count}"] = item
    
    while True:
        try:
            chosen_way = input("Enter a way number: ")
            if int(chosen_way) in range(1,way_count+1):
                break
            else:
                print("Invalid Input!\n")
        except:
            print("Invalid Input!\n")

    return choices[chosen_way]
        
"""Events:
    ? - Random event
    + - Campfire event
    ! - Normal battle
    * - Elite battle
    # - Boss battle
"""
def event_system(event):
    if event == "!":
        battle_system(player)

def battle_system(player):
        # create a random creature / Sparkle-Goat - stubbornness
        enemies = []
        for _ in range(2): #change that number for set difficulty
            enemies.append(Enemy("Slime", 10, 20, 8, 50, 3, katana, [ticker_skin, quick_slice, blackfire]))

        
        turn = 0
        while True:
            turn += 1
            enemies = check_healths(player, enemies)
            if not enemies:
                break
            battle_queue = check_battle_queue(player, enemies)
            battle_ui(turn, player, battle_queue)
            battle_action_system(battle_queue, player)
            
def check_healths(player, enemies):
    if player.complex_stats["health"] <= 0:
        print("You died!")
        exit()
    else:
        enemies = [enemy for enemy in enemies if enemy.complex_stats["health"] > 0]
        if enemies == []:
            print("You won!")
            player.complex_stats["primordial_aura"] = player.max_complex_stats["primordial_aura"]
            # add rewards etc.
        return enemies

def check_battle_queue(player, enemies):
    battlers = [[player.complex_stats["initiative"], player]]

    for enemy in enemies:
        battlers.append([enemy.complex_stats["initiative"], enemy])

    battle_queue = [battler for _,battler in sorted(battlers, key=lambda battler: battler[0], reverse=True)]
    return battle_queue


def battle_ui(turn, player, battle_queue):
    check_battlers_conditions(battle_queue)
    print(f"==========\n |turn {turn}|\n==========\n")
    print((f"{player.name} | Health: {player.complex_stats['health']} | Primordial Aura: {player.complex_stats['primordial_aura']} | Conditions: {player.get_conditions()}"))
    print("----------")
    for enemy in battle_queue:
        if enemy.__class__.__name__ == "Player":
            continue
        print(f"{enemy.name} | Health: {enemy.complex_stats['health']} | Primordial Aura: {enemy.complex_stats['primordial_aura']} | Conditions: {enemy.get_conditions()} \n")
    
    input("Press Enter to continue...")

def check_battlers_conditions(battle_queue):
    for battler in battle_queue:
        if battler.conditions:
            battler.activate_conditions()
    ...

def battle_action_system(battle_queue, player):

    #attack
    for battler in battle_queue:
        battler.aura_regen()
        if battler.__class__.__name__ == "Player":
            enemy_queue = [enemy for enemy in battle_queue if enemy.__class__.__name__ != "Player"]
            battle_action_ui(battler, enemy_queue)

        else:
            selected_mystery = battler.select_mystery_for_battle(player)
            print(f"{battler.name} used {selected_mystery.name}!")
            battler.battle_action(player if selected_mystery.target != "self" else battler, selected_mystery)

def battle_action_ui(player, enemy_queue):
    while True:
        choice = input("""
        Take action:
        1 => Show info
        2 => Take Action

        action: """)
        print("----------")
        if choice == "1":   
            info_ui(player, enemy_queue)
        elif choice == "2":
            player_take_battle_action(player, enemy_queue)
            break


def info_ui(player, enemy_queue):
    print(player.get_stats())
    print("----------")
    for enemy in enemy_queue:
        print(enemy.get_stats(player.real_stats["prediction"]))
        print("----------")
    input("Press Enter to continue...")


def player_take_battle_action(player, enemy_queue):
    while True:
        choice = check_is_int_and_len_longty(input("Choose an Action:\n"+player.get_stats(True)[0]+"\nAction: "), len(player.active_mysteries))
        if choice:
            chosen_mystery = player.get_stats(True)[1][choice-1]
            if chosen_mystery.target == "enemy":
                enemies = "".join([f"{count}==> {enemy.name}\n" for count, enemy in enumerate(enemy_queue, 1)])
                while True:
                    target = check_is_int_and_len_longty(input(f"Choose a target:\n{enemies}Target: "), len(enemy_queue))
                    if target:
                        successful_action = player.battle_action(enemy_queue[target-1], chosen_mystery)
                        break
            elif chosen_mystery.target == "self":
                successful_action = player.battle_action(player, chosen_mystery)
                
            if successful_action == None:
                break
            else:
                print("\nNot enough primordial aura!\n")



def check_is_int_and_len_longty(input, lenght = None):
    try:
        input = int(input)
        if lenght:
            if not (0 < input <= lenght):
                raise ValueError
    except ValueError:
        print("\nInvalid input\n")
        return False
    return input


if __name__ == "__main__":
    main()
