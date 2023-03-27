class Mystery():
    def __init__(self, name:str, target:str, target_stat_and_strength:dict, is_active:bool, turn_count = 0) -> None:
        self.name = name
        self.target = target
        self.target_stat_and_strength = target_stat_and_strength
        self.is_active = is_active
        self.turn_count = turn_count
    
    def __str__(self) -> str:
        return self.name
    
    def get_description(self):
        # f"The intrepid adventurer {self.name} has set their sights on {self.target}! With {self.target_stat_and_strength} in their sights, they unleash a devastating attack that will last for {self.turn_count} turns." + Will their risky gambit pay off, or will they fall prey to the dangers lurking around every corner in this rogue-like adventure?
        return f"{self.name} is targeting {self.target} with {self.target_stat_and_strength} for {self.turn_count} turns."
    

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

    def get_conditions(self):
        if not self.conditions:
            return "No conditions"

    def change_weapon(self, taken_weapon):
        self.weapon = taken_weapon
        self.set_mysteries()

    def take_mystery(self, taken_mystery):
        self.mystery_dict.update({mystery.name: mystery for mystery in taken_mystery})
        self.set_mysteries()


    def fill_energy(self):
        self.primordial_aura = self.real_stats["constitution"]*10

    def set_complex_stats(self):
        self.complex_stats.update({ 
            "health": self.real_stats["vitality"]*7 + self.real_stats["constitution"]*3,
            "initiative": self.real_stats["dexterity"]*3 + self.real_stats["prediction"]*2,
            "primordial_aura":self.real_stats["constitution"]*8 + self.real_stats["vitality"]*2,
            })
        # vitality = stamina regen
        # prediction = show enemy stats see traps 
        # initiative = first attack and dodge
        # dex = attack count
        # constitution = stamina
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
        for mystery in self.passive_mysteries.values():
            if mystery.target == "self":
                for target_stat, passive_strength in mystery.target_stat_and_strength.items():
                    self.real_stats[target_stat] = passive_strength + self.base_stats[target_stat]


    def set_conditions(self, mystery):
        self.conditions.update({mystery.name: [mystery.target_stat_and_stregth, mystery.turn_count]})
    

    def attack(self, target:object, mystery:object):
        # target should be list and can be multiple targets
        print("slm")
        ...
                
    
class Player(Creature):
    def __init__(self, name, vitality, aura_density, dexterity, constitution, prediction, weapon=None, mysteries=None) -> None:
        super().__init__(name, vitality, aura_density, dexterity, constitution, prediction, weapon, mysteries)
    
    def __str__(self) -> str:
        return self.name
    
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
        

pure_soul = Mystery("Pure Soul", "self", {"aura_density":10}, False)
ticker_skin = Mystery("Ticker Skin","self", {"constitution":10}, False)
blackfire = Mystery("black fire", "enemy", {"health":-10}, True, 3)
fireball = Mystery("fire ball", "enemy", {"health":-5}, True, 3)
katana = Weapon("Katana", 5, [fireball])
great_katana = Weapon("Great Katana", 10, [blackfire])
player = Player("player", 15, 10, 10, 100, 8, katana, [ticker_skin]) 


#get player for batt_sys. as variable
def battle_system(player):
    # create a random creature / Sparkle-Goat - stubbornness
    enemies = []
    for _ in range(2): #change that number for set difficulty
        enemies.append(Creature("Slime", 10, 20, 8, 100, 3, katana, [ticker_skin, fireball]))

    
    turn = 0
    while True:
        turn += 1
        battle_queue = check_battle_queue(player, enemies)

        battle_ui(turn, player, battle_queue)
        attack_system(turn, battle_queue)
        
        break


def check_battle_queue(player, enemies):
    battlers = [[player.complex_stats["initiative"], player]]

    for enemy in enemies:
        battlers.append([enemy.complex_stats["initiative"], enemy])

    battle_queue = [battler for _,battler in sorted(battlers, key=lambda battler: battler[0], reverse=True)]
    return battle_queue


def battle_ui(turn, player, battle_queue):
    print(f"==========\n |turn {turn}|\n==========\n")
    print((f"{player.name} | Health: {player.complex_stats['health']} | Primordial Aura: {player.complex_stats['primordial_aura']} | Conditions: {player.get_conditions()}"))
    print("----------")
    for enemy in battle_queue:
        if enemy.__class__.__name__ == "Player":
            continue
        print(f"{enemy.name} | Health: {enemy.complex_stats['health']} | Primordial Aura: {enemy.complex_stats['primordial_aura']} | Conditions: {enemy.get_conditions()} \n")
    
    input("Press Enter to continue...")


def attack_system(turn, battle_queue):

    #attack
    for battler in battle_queue:
        if battler.__class__.__name__ == "Player":
            enemy_queue = [enemy for enemy in battle_queue if enemy.__class__.__name__ != "Player"]
            attack_ui(battler, enemy_queue)

        else:
            ...

def attack_ui(player, enemy_queue):
    while True:
        choice = input("""
        Take action:
        1 => Show info
        2 => Attack

        action: """)
        print("----------")
        if choice == "1":   
            info_ui(player, enemy_queue)
        elif choice == "2":
            attack_action(player, enemy_queue)
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


def attack_action(player, enemy_queue):
    while True:
        choice = check_is_int_and_len_longty(input("Choose an Action:\n"+player.get_stats(True)[0]+"\nAction: "), len(player.active_mysteries))
        if choice:
            chosen_mystery = player.get_stats(True)[1][choice-1]
            if chosen_mystery.target == "enemy":
                enemies = "".join([f"{count}==> {enemy.name}\n" for count, enemy in enumerate(enemy_queue, 1)])
                while True:
                    target = check_is_int_and_len_longty(input(f"Choose a target:\n{enemies}Target: "), len(enemy_queue))
                    if target:
                        player.attack(enemy_queue[target-1], chosen_mystery)
                        break
                break
            ...
        # show active mysteries
        # take target if requered
    ...




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


player.take_mystery([blackfire, pure_soul])
battle_system(player)

