import random
import os
from game_classes import Mystery, Weapon, Player , Enemy


def main():
    global mapd
    
    # Set player
    # name, vitality, aura_density, dexterity, constitution, prediction, weapon, mysteries
    print("Welcome to the Void Tower fellow!\n")
    player_name = input("Enter player name: ")
    player = Player(player_name, random.randint(8,15), random.uniform(1,1.25), random.randint(8,12), 
                            random.randint(35,55), random.randint(3,8), random.choice(starter_weapons),
                            [random.choice(passive_mystery_storage), random.choice(instant_mystery_storage), random.choice(turn_based_mystery_storage)])
    stage = 0
    level = 1
    while True:
        mapd = get_map(level)
        if mapd == "end":
            print("You have reached the end of the tower!")
            break
        while True:
            event = movement_system()
            if event_system(event, player, stage):
                break
            stage += 1
        level += 1

# Set mysteries
# name, target, effect, aura_cost, is_active, turns, is_active
    #passive mysteries
pure_blood = Mystery("Pure Blood", "self", {"constitution":5}, 0, False)
pure_soul = Mystery("Pure Soul", "self", {"aura_density":4}, 0, False)
ticker_skin = Mystery("Ticker Skin","self", {"constitution":3}, 0, False)
eagle_eye = Mystery("Eagle Eye", "self", {"prediction":2}, 0, False)
overflowed_aura = Mystery("Overflowed Aura", "self", {"aura_density":0.25}, 0, False)
improved_reflexes = Mystery("Improved Reflexes", "self", {"dexterity":3}, 0, False)
overflowed_life = Mystery("Overflowed Life", "self", {"vitality":5}, 0, False)
sturdy_aura = Mystery("Sturdy Aura", "self", {"aura_density":3}, 0, False)

passive_mystery_storage = [pure_blood, pure_soul, ticker_skin, eagle_eye, improved_reflexes, overflowed_life, sturdy_aura, overflowed_aura]

    #active mysteries
        #Turn based mysteries
weak_aura_lock = Mystery("Weak Aura Lock", "enemy", {"primordial_aura":-75}, 50, True, 3)
blackfire = Mystery("black fire", "enemy", {"health":-25}, 100, True, 3, True)
fireball = Mystery("fire ball", "enemy", {"health":-10}, 50, True, 3, True)
little_blessing = Mystery("little blessing", "self", {"health":50}, 100, True, 3, True)
toxic_slash = Mystery("toxic slash", "enemy", {"health":-15}, 65, True, 3, True)
aura_burst = Mystery("aura burst", "self", {"aura_density":1.5}, 75, True, 3)
poisened_stab = Mystery("poisened stab", "enemy", {"health":-20}, 35, True, 2, True)
bloody_slash = Mystery("bloody slash", "enemy", {"health":-40}, 110, True, 2, True)
slowless = Mystery("slowless", "enemy", {"dexterity":-5}, 75, True, 2)
dark_binding = Mystery("dark binding", "enemy", {"prediction":-3}, 60, True, 2)
acid_blast = Mystery("acid blast", "enemy", {"health":-30}, 80, True, 2, True)
energized_life = Mystery("energized life", "self", {"vitality":10}, 100, True, 2)

turn_based_mystery_storage = [weak_aura_lock, blackfire, fireball, little_blessing, toxic_slash,
                               poisened_stab, bloody_slash, slowless, dark_binding, acid_blast, aura_burst, energized_life]


        #Instant mysteries
quick_slice =  Mystery("quick slice", "enemy", {"health":-85}, 125, True)
heavy_strike = Mystery("heavy strike", "enemy", {"health":-150}, 220, True)
blunt_edge = Mystery("blunt edge", "enemy", {"health":-30}, 20, True)
aura_blast = Mystery("aura blast", "enemy", {"health":-50}, 85, True)
horizontal_slash = Mystery("horizontal slash", "enemy", {"health":-75}, 100, True)
reaper = Mystery("reaper", "enemy", {"health":-500}, 10, True) #gm only
hearth_strike = Mystery("hearth strike", "enemy", {"health":-100}, 150, True)
body_slam = Mystery("body slam", "enemy", {"health":-50}, 75, True)
exhaustion_curse = Mystery("exhaustion curse", "enemy", {"primordial_aura":-125}, 100, True)
double_strike = Mystery("double strike", "enemy", {"health":-100}, 140, True)


instant_mystery_storage = [quick_slice, heavy_strike, blunt_edge, aura_blast, horizontal_slash, hearth_strike, body_slam, exhaustion_curse, double_strike]

active_mystery_storage = turn_based_mystery_storage + instant_mystery_storage

# Set starter weapons
katana = Weapon("Katana", 1, [horizontal_slash])
twin_daggers = Weapon("Twin Daggers", 1, [toxic_slash, improved_reflexes])
club = Weapon("Club", 1, [blunt_edge, body_slam])
great_katana = Weapon("Great Katana", 1, [quick_slice, sturdy_aura])
war_hammer = Weapon("War Hammer", 1, [heavy_strike, overflowed_life])

uchigatana = Weapon("Uchigatana", 1.75, [horizontal_slash, quick_slice, bloody_slash, weak_aura_lock])
dual_katanas = Weapon("Dual Katanas", 1.85, [toxic_slash, improved_reflexes, poisened_stab, weak_aura_lock])
boss_weapons = [uchigatana, dual_katanas]
starter_weapons = [katana, twin_daggers, club, great_katana, war_hammer]



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
    | ?            !       ?     !       +    # 
    |   ┌────────┐   ┌───┐   ┌─┐   ┌────────────
┌───┘   |________|   |___|   |_|   ├────────────
|x    !            ?       !     !   *   +    # 
├───┐   ┌────────────────┐   ┌─────┐   ┌────────
    |   |_________       |   |_____|   |        
    | !         * |      | !         * |        
    ├─────────┐   |      |   ┌─────┐   |        
              |   |______|   |_____|   |________
              | ?          !         !   +    # 
              ├─────────────────────────────────
"""
    )
    if level > len(levels):
        return "end"
    return levels[level-1][1:]

def movement_system(mapd_test = None):
    global mapd
    #for testing
    if mapd_test:
        mapd = mapd_test
    #----------------
    player_location = mapd.find("x")
    os.system("clear")
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
def event_system(event, player, stage):
    os.system("clear")
    if event in "! * #":
        battle_system(player, stage, event)
    elif event == "?":
        random_event_system(player, stage)
    elif event == "+":
        campfire_system(player)

    if event == "#":
        print("You have defeated the boss!")
        print("You have conquer the floor!")
        input("Press Enter to continue...")
        return True

def battle_system(player, stage, event):
        # create a random creature / Sparkle-Goat - stubbornness
        enemies = create_enemies(stage, event)
    
        turn = 0
        while True:
            turn += 1
            
            enemies = check_healths(player, enemies, event, stage)
            if not enemies:
                dice = random.randint(1,100)
                if dice > 65:
                    old_health = player.complex_stats["health"]
                    player.complex_stats["health"] += player.max_complex_stats["health"]//3
                    print(f"An Unknown Goddes blessed you with life essence due to your victory!\n{player.name}'s Health:{old_health} ==> {player.complex_stats['health']}")
                    input("Press Enter to continue...")
                break
            battle_queue = check_battle_queue(player, enemies)
            battle_ui(turn, player, battle_queue)
            battle_action_system(battle_queue, player)

def create_enemies(stage, event):
    # take addtional variable to determine fights as elite, boss or normal 
    enemies = []
    if event == "!":
        for _ in range(stage//2+1): #change that number for set difficulty
            # name, vitality, aura_density, dexterity, constitution, prediction, weapon, mysteries 
            enemies.append(Enemy("Dungeon Crawler", random.randint(5,11), random.uniform(1,2), random.randint(5,11),
                                random.randint(25,45), random.randint(3,5), club,
                                random.choices(active_mystery_storage, k=random.randint(1,stage//2.5+1)) + random.choices(passive_mystery_storage, k=random.randint(1,stage//2.5+1))))
    elif event == "*":
        enemies.append(Enemy("Archdemon Crawler", random.randint(12,18), random.uniform(1.5,3), random.randint(8,15),
                            random.randint(50,65), random.randint(5,9), random.choice(starter_weapons),
                            random.choices(active_mystery_storage, k=random.randint(2,stage//2+2)) + random.choices(passive_mystery_storage, k=random.randint(2,stage//2+2))))
    elif event == "#":
        enemies.append(Enemy("Overlord of the dungeon", random.randint(20,26), random.uniform(2.5,4), random.randint(18,25),
                            random.randint(75,95), random.randint(11,15), boss_weapons.pop(0),
                            random.choices(active_mystery_storage, k=random.randint(3,stage//2+3)) + random.choices(passive_mystery_storage, k=random.randint(3,stage//2+3))))

    return enemies

def check_healths(player, enemies, event, stage):
    check_battlers_conditions([player] + [enemy for enemy in enemies])

    if player.complex_stats["health"] <= 0:
        os.system("clear")
        print("You died!")
        exit()
    else:
        enemies = [enemy for enemy in enemies if enemy.complex_stats["health"] > 0]
        if enemies == []:
            os.system("clear")
            print("You survived the battle!")
            player.complex_stats["primordial_aura"] = player.max_complex_stats["primordial_aura"]

            weapon_mystery, weapon_affinity = [], 0
            dice = random.randint(1,100)

            if event == "!":
                if dice > 95:
                    player.taken_mystery = random.choices(active_mystery_storage, k=random.randint(1,stage//2.5+1)) + random.choices(passive_mystery_storage, k=random.randint(1,stage//2.5+1))
                elif dice > 80:
                    player.taken_mystery = random.choices(active_mystery_storage, k=random.randint(1,stage//2.5+1))
                elif dice > 30-stage:
                    weapon_affinity = round(random.uniform(1, 1.3),2)
                    weapon_mystery = random.choices(active_mystery_storage, k=random.randint(1,stage//2.5+1))
                    create_random_weapon(player, weapon_affinity, weapon_mystery)     
                else:
                    print("You found nothing.")

            elif event == "*":
                if dice > 88:
                    player.taken_mystery = random.choices(active_mystery_storage, k=random.randint(2,stage//2+2)) + random.choices(passive_mystery_storage, k=random.randint(2,stage//2+2))
                elif dice > 60:
                    player.taken_mystery = random.choices(active_mystery_storage, k=random.randint(2,stage//2+2))
                elif dice > 5:
                    weapon_affinity = round(random.uniform(1.25, 1.5),2)
                    weapon_mystery = random.choices(active_mystery_storage, k=random.randint(2,stage//2+2))
                    create_random_weapon(player, weapon_affinity, weapon_mystery)
                else:
                    print("You found nothing.")

            elif event == "#":
                weapon_affinity = round(random.uniform(1.45, 1.8),2)
                weapon_mystery = random.choices(active_mystery_storage, k=random.randint(3,stage//2+3))
                create_random_weapon(player, weapon_affinity, weapon_mystery)
                if dice > 80:
                    player.taken_mystery = random.choices(active_mystery_storage, k=random.randint(3,stage//2+3)) + random.choices(passive_mystery_storage, k=random.randint(3,stage//2+3))
                elif dice > 45:
                    player.taken_mystery = random.choices(active_mystery_storage, k=random.randint(3,stage//2+3))

            input("\nPress enter to continue.")
        return enemies

def create_random_weapon(player, weapon_affinity, weapon_mystery):
    weapon_name = random.choice(["Short Sword", "Long Sword", "Axe", "Mace", "Flail", "Spear", "Trident", "Halberd", "Dagger", "Throwing Axe", "Throwing Knife", "Scimitar", "Katana", "Rapier", "Whip", "Club"])

    print(f"\nYou found {weapon_name} with {weapon_affinity} affinity with {[mystery.name for mystery in weapon_mystery]} mystery.")
    print(f"\nYour current weapon is {player.weapon.name} has {player.weapon.aura_affinity} affinity with {[mystery.name for mystery in player.weapon.mysteries]} mysteries.\n")
    while decision:=input("Do you want to equip it? (y/n): "):
        if decision == "y":
            print("You equipped the new weapon.")
            player.change_weapon(Weapon(weapon_name, weapon_affinity, weapon_mystery)) 
            break
        elif decision == "n":
            break
        else:
            print("Wrong input. Try again.")

def check_battlers_conditions(battlers):
    for battler in battlers:
        if battler.conditions:
            battler.activate_conditions()
    

def check_battle_queue(player, enemies):
    battlers = [[player.complex_stats["initiative"], player]]

    for enemy in enemies:
        battlers.append([enemy.complex_stats["initiative"], enemy])

    battle_queue = [battler for _,battler in sorted(battlers, key=lambda battler: battler[0], reverse=True)]
    return battle_queue


def battle_ui(turn, player, battle_queue):
    os.system("clear")
     # Print turn information
    print(f"{'='*10}\n| Turn {turn} |\n{'='*10}\n")

    # Print player status
    print(f"{player.name} | Health: {player.complex_stats['health']} | " 
          f"Primordial Aura: {player.complex_stats['primordial_aura']} | "
          f"Conditions: {player.get_conditions()}\n"+"─"*(len(player.name)+2))

    # Print enemies' status
    for enemy in battle_queue:
        if enemy.__class__.__name__ == "Player":
            continue
        print(f"{enemy.name} | Health: {enemy.complex_stats['health']} | "
              f"Primordial Aura: {enemy.complex_stats['primordial_aura']} | "
              f"Conditions: {enemy.get_conditions()}\n"+"-"*(len(enemy.name)+2))
        
    input("Press Enter to continue...")


def battle_action_system(battle_queue, player):

    #attack
    for battler in battle_queue:
        if battler.complex_stats["health"] <= 0:
            continue

        battler.aura_regen()
        if battler.__class__.__name__ == "Player":
            enemy_queue = [enemy for enemy in battle_queue if enemy.__class__.__name__ != "Player"]
            battle_action_ui(battler, enemy_queue)

        else:
            selected_mystery = battler.select_mystery_for_battle(player)
            battler.battle_action(player if selected_mystery.target != "self" else battler, selected_mystery)

            current_target = player if selected_mystery.target != "self" else battler
            current_target_stats = list(selected_mystery.target_stat_and_strength.keys())[0]
            print(f"\n{battler.name} used {(selected_mystery.name).upper()} mystery with {selected_mystery.get_damage_amount(battler.aura_amplifier)}\n")
            print(f"{current_target.name}'s current {current_target_stats}: {current_target.complex_stats[current_target_stats] if current_target_stats in current_target.complex_stats else current_target.real_stats[current_target_stats]}")
            input("Press Enter to continue...")
            

def battle_action_ui(player, enemy_queue):
    while True:
        os.system("clear")
        choice = input("Take action:\n1 => Show info\n2 => Take Action\n\naction: ")
        print("----------")
        if choice == "1":   
            info_ui(player, enemy_queue)
        elif choice == "2":
            player_take_battle_action(player, enemy_queue)
            break


def info_ui(player, enemy_queue):
    os.system("clear")
    print(player.get_stats())
    print("----------")
    for enemy in enemy_queue:
        print(enemy.get_stats(player.real_stats["prediction"]))
        print("----------")
    input("Press Enter to continue...")


def player_take_battle_action(player, enemy_queue):
    os.system("clear")
    while True:
        choice = check_is_int_and_len_longty(input("Choose an Action:\n"+player.get_stats(True)[0]+"\nAction: "), len(player.active_mysteries))
        if choice:
            chosen_mystery = player.get_stats(True)[1][choice-1]
            if chosen_mystery.target == "enemy":
                enemies = "".join([f"{count}==> {enemy.name} | health:{enemy.complex_stats['health']}\n" for count, enemy in enumerate(enemy_queue, 1)])
                while True:
                    target = check_is_int_and_len_longty(input(f"Choose a target:\n{enemies}Target: "), len(enemy_queue))
                    os.system("clear")
                    if target:
                        successful_action = player.battle_action(enemy_queue[target-1], chosen_mystery)
                        break
            elif chosen_mystery.target == "self":
                successful_action = player.battle_action(player, chosen_mystery)
                
            if successful_action == None:
                break
            else:
                print("\nNot enough primordial aura!\n")

def random_event_system(player, stage):
    dice = random.randint(1, 100)
    weapon_affinity = round(random.uniform(1.1, 1.5),2)
    weapon_mystery = random.choices(active_mystery_storage, k=random.randint(2,stage//2+2))
    if dice <= 35:
        trap_activision(player, stage)
        
    elif dice <= 85:
        trap_activision(player, stage)
        create_random_weapon(player, weapon_affinity, weapon_mystery)

    else:
        create_random_weapon(player, weapon_affinity, weapon_mystery)
        print("You have found a mystery!")
        player.take_mystery([random.choice(passive_mystery_storage)])
    
def trap_activision(player, stage):
    trap_perception = random.randint(1, 10)
    trap_dexterity = random.randint(1, 20)
    trap_initiative = trap_perception*2 + trap_dexterity*3
    if trap_initiative > player.complex_stats["initiative"]:
        trap_damage = random.randint(player.complex_stats["health"]//(20-stage//3), player.complex_stats["health"]//(7.5-stage//3))
        player.complex_stats["health"] -= trap_damage
        print(f"You have been ambushed by a trap!\nTrap deals {trap_damage} damage to you!")
        print(f"{player.name}'s current Health: {player.complex_stats['health']}")
        input("Press Enter to continue...")
    else:
        print("You have been ambushed by a trap!\nYou have successfully avoided the trap!")
        input("Press Enter to continue...")

    if player.complex_stats["health"] <= 0:
        print("You have been killed by a trap!")
        exit() 

def campfire_system(player):
    old_health = player.complex_stats["health"]
    player.complex_stats["health"] += player.max_complex_stats["health"]//2
    print(f"You have rested at the campfire!\n{player.name}'s Health:{old_health} ==> {player.complex_stats['health']}")
    input("Press Enter to continue...")

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
