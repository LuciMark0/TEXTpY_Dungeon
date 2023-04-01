import random


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
    
    def get_damage_amount(self, aura_amplifier):
        return f"{list(self.target_stat_and_strength.keys())[0]}:{int(list(self.target_stat_and_strength.values())[0]*aura_amplifier)}"

    def get_description(self, aura_amplifier = 1):
        """
        Creates and returns a string description of the Mystery,
        detailing its target and effect, aura cost, and duration.
        """
        repeatable_info = "each " if self.permanence else ""
        if self.turn_count:
            duration = f"until {repeatable_info}remaining {self.turn_count} turns for a cost of {self.aura_cost} AURA"
            if not self.permanence:
                duration += " -Temporarily-"
        else:
            duration = f"for a cost of {self.aura_cost} AURA"
        effect = [f"deals {int(value*aura_amplifier)} damage to {key}" for key, value in self.target_stat_and_strength.items()][0]
        return f"Targets the {self.target} with {effect} {duration}."



class Weapon():
    def __init__(self, name:str, aura_affinity:int, mysteries = []) -> None:
        self.name = name
        # addition to the damage of used mystery which forged into the weapon
        self.aura_affinity = aura_affinity
        self.mysteries = mysteries
        

    def __str__(self) -> str:
        return self.name

    def get_mysteries(self):
        return self.mysteries



class Creature():
    def __init__(self,name, vitality, aura_density, dexterity, constitution, prediction, weapon = None, mysteries=None) -> None:
        self.name = name
        
        self.base_stats = {  "vitality": vitality, "aura_density": aura_density,
                             "dexterity": dexterity, "constitution": constitution,
                             "prediction":prediction}
        self.real_stats = {**self.base_stats}

        self.complex_stats = {}
        self.set_complex_stats()

        self.weapon = weapon
        self.set_aura_amplifier()
        self.mystery_dict = {mystery.name:mystery for mystery in mysteries if mysteries}
        self.set_mysteries()

        self.conditions = {}

    def __str__(self) -> str:
        return self.name

    def get_stats(self, player_prediction):
        # order mysteries in str to look better
        active_mysts = "\n".join([f"{key}: {value.get_description(self.aura_amplifier)}" for key, value in self.active_mysteries.items()]) + "\n"
        passive_mysts = "\n".join([f"{key}: {value.get_description()}" for key, value in self.passive_mysteries.items() 
                                    if self.passive_mysteries]) + "\n"
        
        if player_prediction < self.real_stats["prediction"]-2:
            return f"{self.name} is hiding from prying eyes!"
        elif self.real_stats["prediction"]+2 >= player_prediction >= self.real_stats["prediction"]-2:
            return f"{self.name}'s info:\nReal stats: {self.real_stats}\nComplex stats: {self.complex_stats}\nWeapon: {self.weapon} with {self.weapon.aura_affinity} aura affinity"
        else:
            return f"\n{self.name}'s info:\n\nReal stats: {self.real_stats}\nComplex stats: {self.complex_stats}Weapon: {self.weapon} with {self.weapon.aura_affinity} aura affinity\n\nPassive mysteries;\n{passive_mysts}\nActive mysteries;\n{active_mysts}"

    def set_conditions(self, mystery):
        self.conditions.update({mystery.name: [mystery.target_stat_and_strength , mystery.turn_count, mystery.permanence, {"is_activated": False}]})

    def get_conditions(self):
        if not self.conditions:
            return "No conditions"
        else:
            return "\n"+"\n".join([f"{key}: {value[0]} for remeaning {value[1]} turns" + (" -temporarily-" if not value[2] else "") for key, value in self.conditions.items()])

    def set_aura_amplifier(self):
        self.aura_amplifier = (self.weapon.aura_affinity if self.weapon.aura_affinity <= self.real_stats["aura_density"] else self.real_stats["aura_density"]) if self.weapon else 1

    def change_weapon(self, taken_weapon):
        self.weapon = taken_weapon
        self.set_mysteries()
        self.set_aura_amplifier()


    def take_mystery(self, taken_mystery):
        print(f"{self.name} gain {[mystery.name for mystery in taken_mystery]} mystery")
        input("Press enter to continue...")
        self.mystery_dict.update({mystery.name: mystery for mystery in taken_mystery})
        self.set_mysteries()
            

    def set_complex_stats(self):
        self.max_complex_stats = {
            "health": self.real_stats["vitality"]*7 + self.real_stats["constitution"]*3,
            "initiative": self.real_stats["dexterity"]*3 + self.real_stats["prediction"]*2,
            "primordial_aura":self.real_stats["constitution"]*8 + self.real_stats["aura_density"]*2,
            "aura_regeneration": self.real_stats["vitality"]*3 - self.real_stats["aura_density"],
        }
        
        self.complex_stats.update({ 
            "health": self.max_complex_stats["health"],
            "initiative": self.max_complex_stats["initiative"],
            "primordial_aura":self.max_complex_stats["primordial_aura"],
            "aura_regeneration": self.max_complex_stats["aura_regeneration"],
            })
        # vitality = aura regen in fight
        # prediction = show enemy stats 
        # initiative = first attack and 
        # constitution = auro deposit
        # aura_density = mystery damage

    def calculate_in_battle_complex_stats(self):
        self.complex_stats.update({ 
            "initiative": self.real_stats["dexterity"]*3 + self.real_stats["prediction"]*2,
            "aura_regeneration": self.real_stats["vitality"]*3 - self.real_stats["aura_density"],
            })

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
                    # add weapon aura affinity to condition strength
                    if target_stat not in conditions_stat_placeholders[target_stat_name_statement]:
                            conditions_stat_placeholders[target_stat_name_statement][target_stat] = int(condition_strength * (self.aura_amplifier))
                    else:
                        conditions_stat_placeholders[target_stat_name_statement][target_stat] += int(condition_strength * (self.aura_amplifier))

            for stat_name, stat_value in conditions_stat_placeholders.items():
                for stat, value in stat_value.items():
                    self.__dict__[stat_name][stat] = value + self.real_stats[stat] if stat_name == "real_stats" else value + self.complex_stats[stat]
                    if stat_name == "real_stats":
                        self.calculate_in_battle_complex_stats
            finished_conditions = []
            for mystery_name, condition in self.conditions.items():
                condition[1] -= 1
                if condition[1] == 0:
                    finished_conditions.append({"mystery_name":mystery_name,"target_and_strength":condition[0],"permanency":condition[2]})

            for condition in finished_conditions:
                if not condition["permanency"]:
                    target_stat, condition_strength = next(iter(condition["target_and_strength"].items()))
                    target_stat_name_statement = "real_stats" if target_stat in self.real_stats else "complex_stats"
                    self.__dict__[target_stat_name_statement][target_stat] -= condition_strength

                del self.conditions[condition["mystery_name"]]


    def battle_action(self, target_entity:object, mystery:object):
        # target should be list and can be multiple targets
        if self.complex_stats["primordial_aura"] - mystery.aura_cost < 0:
            return False
        if mystery.turn_count:
            target_entity.set_conditions(mystery)
            self.complex_stats["primordial_aura"] -= mystery.aura_cost
        else:
            for target_stat, attack_strength in mystery.target_stat_and_strength.items():
                # check if target stat is complex stat
                # instant attacks can just affect complex stats
                # add weapon aura affinity to attack strength
                if target_stat in self.complex_stats:
                    target_entity.complex_stats[target_stat] += int(attack_strength * (self.aura_amplifier))
                    self.complex_stats["primordial_aura"] -= mystery.aura_cost
    

    def aura_regen(self):
        self.complex_stats["primordial_aura"] += self.complex_stats["aura_regeneration"]
        if self.complex_stats["primordial_aura"] > self.max_complex_stats["primordial_aura"]:
            self.complex_stats["primordial_aura"] = self.max_complex_stats["primordial_aura"]
    
        
class Enemy(Creature):
    def __init__(self, name, vitality, aura_density, dexterity, constitution, prediction, weapon=None, mysteries=None) -> None:
        super().__init__(name, vitality, aura_density, dexterity, constitution, prediction, weapon, mysteries)
        self.last_selected_mystery = None
    

    def select_mystery_for_battle(self, player):
        selectable_mysteries = [mystery for mystery in self.active_mysteries.values() if mystery.aura_cost <= self.complex_stats["primordial_aura"]]
        selected_mystery = random.choice(selectable_mysteries)
        
        while True:
            if selected_mystery == self.last_selected_mystery and len(selectable_mysteries) > 1 and not selected_mystery.name in player.conditions.keys():
                selected_mystery = random.choice(selectable_mysteries)
            else:
                break

        self.last_selected_mystery = selected_mystery
        return selected_mystery


class Player(Creature):
    def __init__(self, name, vitality, aura_density, dexterity, constitution, prediction, weapon=None, mysteries=None) -> None:
        super().__init__(name, vitality, aura_density, dexterity, constitution, prediction, weapon, mysteries)
    
    def get_stats(self, is_attack = None):
        active_mysts = "\n".join([f"{count}==> {key}: {value.get_description(self.aura_amplifier)}" for count, (key, value) in enumerate(self.active_mysteries.items(), 1)]
                                    if is_attack
                                else [f"{key}: {value.get_description(self.aura_amplifier)}" for key, value in self.active_mysteries.items()]) + "\n"
        
        passive_mysts = "\n".join([f"{key}: {value.get_description()}" for key, value in self.passive_mysteries.items()
                                    if self.passive_mysteries]) + "\n"

        if is_attack:
            mysts_classes = [value for value in self.active_mysteries.values()]
            return [active_mysts, mysts_classes]
        else:
            description = f"\n{self.name}'s info:\n\nReal stats: {self.real_stats}\nComplex stats: {self.complex_stats}\n"
            description += f"\nWeapon: {self.weapon.name} with {self.weapon.aura_affinity} aura_affinity\n\nPassive mysteries;\n{passive_mysts}\nActive mysteries;\n{active_mysts}"
            return description
        
    def fill_aura(self):
        self.primordial_aura = self.max_complex_stats["primordial_aura"]
    
    def forge_mystery_to_weapon(self, forged_mystery:list):
        self.weapon.mysteries += forged_mystery
        self.set_mysteries()
    
def main():
     ...


if __name__ == "__main__":
    main()
