from random import randint
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

def get_map(level):
    levels = ("""
      _____________________        
     │ !         !        !│_______
┌────┘   ┌─────┐   ┌────┐ $   +  # 
│x     ? │     │   |____├──────────
├────┐   │_____│ ?             +  #
     │ !     ? ├───────────────────
     ├─────┐   │___________________
           │ $                 +  #
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
    events = ("?","!","$","#","+")

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
        

def event_system(event):
    ...




if __name__ == "__main__":
    main()