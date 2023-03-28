class Mystery():
    def __init__(self, name:str, target:str, target_stat_and_strength:dict, aura_cost:int, is_active:bool, turn_count = 0, permanence = False) -> None:
        self.name = name
        self.target = target
        self.target_stat_and_strength = target_stat_and_strength
        self.aura_cost = aura_cost
        self.is_active = is_active
        self.turn_count = turn_count
        self.permanence = permanence
    
    def __str__(self) -> str:
        return self.name
    
    def get_description(self):
        # f"The intrepid adventurer {self.name} has set their sights on {self.target}! With {self.target_stat_and_strength} in their sights, they unleash a devastating attack that will last for {self.turn_count} turns." + Will their risky gambit pay off, or will they fall prey to the dangers lurking around every corner in that floor?
        return f"{self.name} is targeting {self.target} with {self.target_stat_and_strength} until {self.turn_count} turns for cost of {self.aura_cost} aura"
    

class Weapon():
    def __init__(self, name:str, weapon_strength:int, mysteries = []) -> None:
        self.name = name
        self.weapon_strength = weapon_strength
        self.mysteries = mysteries
        

    def __str__(self) -> str:
        return self.name

    def get_mysteries(self):
        return self.mysteries

    

class Creature():
    
    def __init__(self,name, vitality, aura_density, dexterity, constitution, prediction, weapon=None, mysteries=None) -> None:
        self.name = name

        self.base_stats = {  "vitality": vitality, "aura_density": aura_density,
                             "dexterity": dexterity, "constitution": constitution,
                             "prediction":prediction}
        self.real_stats = {**self.base_stats}

        self.complex_stats = {}
        self.set_complex_stats()

        self.weapon = weapon

        self.mystery_dict = {mystery.name:mystery for mystery in mysteries if mysteries}
        self.set_mysteries()

        self.conditions = {}

    def __str__(self) -> str:
        return self.name

    def get_stats(self, player_prediction):
        # order mysteries in str to look better
        active_mysts = "\n".join([f"{key}: {value.get_description()}" for key, value in self.active_mysteries.items()]) + "\n"
        passive_mysts = "\n".join([f"{key}: {value.get_description()}" for key, value in self.passive_mysteries.items() 
                                    if self.passive_mysteries]) + "\n"
        
        if player_prediction < self.real_stats["prediction"]-2:
            return f"{self.name} is hiding"
        elif self.real_stats["prediction"]+2 >= player_prediction >= self.real_stats["prediction"]-2:
            return f"{self.name}'s info:\nReal stats: {self.real_stats}\nComplex stats: {self.complex_stats}"
        else:
            return f"\n{self.name}'s info:\n\nReal stats: {self.real_stats}\nComplex stats: {self.complex_stats}\n\nPassive mysteries;\n{passive_mysts}\nActive mysteries;\n{active_mysts}"

    def set_conditions(self, mystery):
        self.conditions.update({mystery.name: [mystery.target_stat_and_strength, mystery.turn_count, mystery.permanence, {"is_activated": False}]})

    def get_conditions(self):
        if not self.conditions:
            return "No conditions"
        else:
            return "\n"+"\n".join([f"{key}: {value[0]} for remeaning {value[1]} turns" + (" -temporarily-" if not value[2] else "") for key, value in self.conditions.items()])


    def change_weapon(self, taken_weapon):
        self.weapon = taken_weapon
        self.set_mysteries()


    def take_mystery(self, taken_mystery):
        self.mystery_dict.update({mystery.name: mystery for mystery in taken_mystery})
        self.set_mysteries()


    def set_complex_stats(self):
        self.max_complex_stats = {
            "health": self.real_stats["vitality"]*7 + self.real_stats["constitution"]*3,
            "initiative": self.real_stats["dexterity"]*3 + self.real_stats["prediction"]*2,
            "primordial_aura":self.real_stats["constitution"]*8 + self.real_stats["aura_density"]*2,
        }
        
        self.complex_stats.update({ 
            "health": self.max_complex_stats["health"],
            "initiative": self.max_complex_stats["initiative"],
            "primordial_aura":self.max_complex_stats["primordial_aura"],
            })
        # vitality = aura regen in fight
        # prediction = show enemy stats see traps 
        # initiative = first attack and dodge
        # dex = attack count, crit chance (if prediction is higher than enemy)
        # constitution = auro deposit
        # aura_density = mystery damage


    def set_mysteries(self):
        active_replacment = {}
        passive_replacment = {}
        for name, mystery in (self.mystery_dict.items() if not self.weapon else {**self.mystery_dict, **{mystery.name:mystery for mystery in self.weapon.get_mysteries()}}.items()):
            if mystery.is_active:
                active_replacment[name] = mystery
            else:
                passive_replacment[name] = mystery
        if passive_replacment:
            self.passive_mysteries = passive_replacment
            self.activate_passive_skills()
        else:
            self.passive_mysteries = {}
        self.active_mysteries = active_replacment
        
    
    def activate_passive_skills(self):
        passive_stat_placeholders = {"real_stats":{}, "complex_stats":{}} # to avoid changing stats while iterating
        for mystery in self.passive_mysteries.values():
            if mystery.target == "self":
                for target_stat, passive_strength in mystery.target_stat_and_strength.items():
                    
                    target_stat_name_statement = "real_stats" if target_stat in self.real_stats else "complex_stats"

                    if target_stat not in passive_stat_placeholders[target_stat_name_statement]:
                        passive_stat_placeholders[target_stat_name_statement][target_stat] = passive_strength
                    else:
                        passive_stat_placeholders[target_stat_name_statement][target_stat] += passive_strength

                for stat_name, stat_value in passive_stat_placeholders.items():
                    for stat, value in stat_value.items():
                        self.__dict__[stat_name][stat] = value + self.base_stats[stat] if stat_name == "real_stats" else value + self.max_complex_stats[stat]
    
    def activate_conditions(self):
        if self.conditions:
            conditions_stat_placeholders = {"real_stats":{}, "complex_stats":{}} # to avoid changing stats while iterating
            for condition in self.conditions.values():
                for target_stat, condition_strength in condition[0].items():
                    if condition[3]["is_activated"] and not condition[2]:
                        continue
                    elif not condition[3]["is_activated"]:
                        condition[3]["is_activated"] = True

                    target_stat_name_statement = "real_stats" if target_stat in self.real_stats else "complex_stats"

                    if target_stat not in conditions_stat_placeholders[target_stat_name_statement]:
                            conditions_stat_placeholders[target_stat_name_statement][target_stat] = condition_strength
                    else:
                        conditions_stat_placeholders[target_stat_name_statement][target_stat] += condition_strength

            for stat_name, stat_value in conditions_stat_placeholders.items():
                for stat, value in stat_value.items():
                    self.__dict__[stat_name][stat] = value + self.real_stats[stat] if stat_name == "real_stats" else value + self.complex_stats[stat]

            finished_conditions = []
            for mystery_name, condition in self.conditions.items():
                condition[1] -= 1
                if condition[1] == 0:
                    finished_conditions.append({"mystery_name":mystery_name,"target_and_strength":condition[0],"permanency":condition[2]})

            for condition in finished_conditions:
                if not condition["permanency"]:
                    print(condition["target_and_strength"])
                    target_stat, condition_strength = next(iter(condition["target_and_strength"].items()))
                    target_stat_name_statement = "real_stats" if target_stat in self.real_stats else "complex_stats"
                    self.__dict__[target_stat_name_statement][target_stat] -= condition_strength

                del self.conditions[condition["mystery_name"]]
    ...


    
        
class Enemy(Creature):
    def __init__(self, name, vitality, aura_density, dexterity, constitution, prediction, weapon=None, mysteries=None) -> None:
        super().__init__(name, vitality, aura_density, dexterity, constitution, prediction, weapon, mysteries)
    

    ...
    
    

class Player(Creature):
    def __init__(self, name, vitality, aura_density, dexterity, constitution, prediction, weapon=None, mysteries=None) -> None:
        super().__init__(name, vitality, aura_density, dexterity, constitution, prediction, weapon, mysteries)
    
    def get_stats(self, is_attack = None):
        active_mysts = "\n".join([f"{count}==> {key}: {value.get_description()}" for count, (key, value) in enumerate(self.active_mysteries.items(), 1)]
                                    if is_attack
                                else [f"{key}: {value.get_description()}" for key, value in self.active_mysteries.items()]) + "\n"
        
        passive_mysts = "\n".join([f"{key}: {value.get_description()}" for key, value in self.passive_mysteries.items()
                                    if self.passive_mysteries]) + "\n"

        if is_attack:
            mysts_classes = [value for value in self.active_mysteries.values()]
            return [active_mysts, mysts_classes]
        else:
            return f"\n{self.name}'s info:\n\nReal stats: {self.real_stats}\nComplex stats: {self.complex_stats}\n\nPassive mysteries;\n{passive_mysts}\nActive mysteries;\n{active_mysts}"
        
    def fill_energy(self):
        self.primordial_aura = self.max_complex_stats["primordial_aura"]
    
    def forge_mystery_to_weapon(self, forged_mystery:list):
        self.weapon.mysteries += forged_mystery
        self.set_mysteries()
    
    def battle_action(self, target_entity:object, mystery:object):
        # target should be list and can be multiple targets
        if mystery.aura_cost >= self.complex_stats["primordial_aura"]:
            return False
        if mystery.turn_count:
            target_entity.set_conditions(mystery)
        else:
            for target_stat, attack_strength in mystery.target_stat_and_strength.items():
                # check if target stat is complex stat
                # instant attacks can just affect complex stats
                if target_stat in self.complex_stats:
                    target_entity.complex_stats[target_stat] += attack_strength
                    self.complex_stats["primordial_aura"] -= mystery.aura_cost
        ...
        
pure_blood = Mystery("Pure Blood", "self", {"constitution":10}, 0, False)
pure_soul = Mystery("Pure Soul", "self", {"aura_density":10}, 0, False)
ticker_skin = Mystery("Ticker Skin","self", {"constitution":15}, 0, False)
blackfire = Mystery("black fire", "enemy", {"health":-25}, 100, True, 3, True)
fireball = Mystery("fire ball", "enemy", {"health":-10}, 50, True, 3, False)
quick_slice =  Mystery("quick slice", "enemy", {"health":-25}, 150, True)
little_blessing = Mystery("little blessing", "self", {"health":50}, 50, True, 3, False)
katana = Weapon("Katana", 5, [fireball])
great_katana = Weapon("Great Katana", 10, [blackfire])
player = Player("player", 15, 10, 10, 50, 8, katana, [ticker_skin]) 


#get player for batt_sys. as variable
def battle_system(player):
    # create a random creature / Sparkle-Goat - stubbornness
    enemies = []
    for _ in range(2): #change that number for set difficulty
        enemies.append(Creature("Slime", 10, 20, 8, 50, 3, katana, [ticker_skin, fireball]))

    
    turn = 0
    while True:
        turn += 1

        battle_queue = check_battle_queue(player, enemies)

        battle_ui(turn, player, battle_queue)
        battle_action_system(turn, battle_queue)
        


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

def battle_action_system(turn, battle_queue):

    #attack
    for battler in battle_queue:
        if battler.__class__.__name__ == "Player":
            enemy_queue = [enemy for enemy in battle_queue if enemy.__class__.__name__ != "Player"]
            battle_action_ui(battler, enemy_queue)

        else:
            ...

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
        
    # show info of player and enemies(prediction required) okay
    # take action
        # show active mysteries
            #take target if requered
    ...


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



player.forge_mystery_to_weapon([little_blessing, pure_blood])
player.take_mystery([blackfire, pure_soul, quick_slice])
battle_system(player)
