from playerClass import Player, Role, Weapon
from nyloBoss import NyloBoss
from sim_functions import simulate_fight, output_results, export_results

'''
The layout of the setups are pretty painful but was the easiest way to 
implement a bunch of different setups without writing a ton of custom code.

For the purposes of the sim, the only ranger setup has been std_weapons_range.
The remainder are with the mage varying setups.

The 'Weapons' class takes inputs as such:
    (name, accuracy, max_hit, speed, style), and the previous string is how it is referred to.
    i.e, calling player.role.weapons['magic'] calls the magic weapon for a certain player.

Some setups have special items, like blowpipe or chalbred. This is for tick fills.
'''

std_weapons_range = {
    'magic': Weapon('sang', accuracy=13708, max_hit=37, speed=4, style='magic'),        
    'ranged': Weapon('tbow', accuracy=32541, max_hit=81, speed=5, style='ranged'),      
    'blowpipe': Weapon('blowpipe', accuracy=17004, max_hit=32, speed=2, style='ranged'),      
    'melee': Weapon('scythe', accuracy=33592, max_hit=50, speed=5, style='melee')          
}

std_weapons_mage_dart = {
    'magic': Weapon('sang', accuracy=24764, max_hit=43, speed=4, style='magic'),        
    'ranged': Weapon('tbow', accuracy=22663, max_hit=70, speed=5, style='ranged'),      
    'blowpipe': Weapon('bp', accuracy=7668, max_hit=22, speed=2, style='ranged'),      #DRAGON DARTS 
    'melee': Weapon('scythe', accuracy=33592, max_hit=50, speed=5, style='melee'),         
    'chalbred': Weapon('chalbred', accuracy=30694, max_hit=66, speed=7, style='melee')  
}

std_weapons_mage = {
    'magic': Weapon('sang', accuracy=24764, max_hit=43, speed=4, style='magic'),        
    'ranged': Weapon('tbow', accuracy=22663, max_hit=70, speed=5, style='ranged'),      
    'blowpipe': Weapon('blowpipe', accuracy=10508, max_hit=27, speed=2, style='ranged'),      
    'melee': Weapon('scythe', accuracy=33592, max_hit=50, speed=5, style='melee'),        
    'chalbred': Weapon('chalbred', accuracy=30694, max_hit=66, speed=7, style='melee')  
}

std_weapons_mage_lb = {
    'magic': Weapon('sang', accuracy=24764, max_hit=43, speed=4, style='magic'),        
    'ranged': Weapon('tbow', accuracy=22663, max_hit=70, speed=5, style='ranged'),      
    'blowpipe': Weapon('blowpipe', accuracy=10508, max_hit=27, speed=2, style='ranged'),      
    'melee': Weapon('scythe', accuracy=33592, max_hit=47, speed=5, style='melee'),         
    'chalbred': Weapon('chalbred', accuracy=30694, max_hit=62, speed=7, style='melee')  
}

shadow_8way_ring = {    
    'magic': Weapon('shadow', accuracy=80332, max_hit=65, speed=5, style='magic'),        
    'ranged': Weapon('tbow', accuracy=22663, max_hit=70, speed=5, style='ranged'),      
    'melee': Weapon('scythe', accuracy=33592, max_hit=50, speed=5, style='melee')          
}

shadow_8way_boots = {    
    'magic': Weapon('shadow', accuracy=77161, max_hit=64, speed=5, style='magic'),       
    'ranged': Weapon('tbow', accuracy=22663, max_hit=70, speed=5, style='ranged'),      
    'melee': Weapon('scythe', accuracy=33592, max_hit=50, speed=5, style='melee')          
}

shadow_5way = {    
    'magic': Weapon('shadow', accuracy=63118, max_hit=57, speed=5, style='magic'),       
    'ranged': Weapon('tbow', accuracy=22663, max_hit=70, speed=5, style='ranged'),      
    'melee': Weapon('scythe', accuracy=33592, max_hit=50, speed=5, style='melee')          
}

shadow_8way_boots_lb = {    
    'magic': Weapon('shadow', accuracy=77161, max_hit=64, speed=5, style='magic'),       
    'ranged': Weapon('tbow', accuracy=22663, max_hit=70, speed=5, style='ranged'),      
    'melee': Weapon('scy', accuracy=33592, max_hit=47, speed=5, style='melee')          
}

shadow_5way_lb = {    
    'magic': Weapon('shadow', accuracy=63118, max_hit=57, speed=5, style='magic'),       
    'ranged': Weapon('tbow', accuracy=22663, max_hit=70, speed=5, style='ranged'),      
    'melee': Weapon('scy', accuracy=33592, max_hit=47, speed=5, style='melee')          
}

setups = {
    'std_weapons_mage': std_weapons_mage,
    'std_weapons_mage_dart': std_weapons_mage_dart,
    '5 way shadow': shadow_5way,
    '8 way shadow w/ boots': shadow_8way_boots,
    '8 way shadow w/ magus': shadow_8way_ring,
    'std_weapons_mage_lb': std_weapons_mage_lb,
}

'''
run_simulations is the primary function that handles the simulations.
1. The function will iterate through a set of setups (above) for the mage, and use the std range setup.
2. The function will then determine if it is a shadow setup or not (mainly for tick filling logic)
3. The function will initialize a Player class for each player (playerClass.py)
4. The function will initalize a Boss class (nyloBoss.py)
5. The function will then simulate a fight with the boss (sim_functions.py)
6. The function will structure the results in a neat format for output.
(7). Optionally, if you'd like to output the results of the simulation (outside of the terminal, in .csv form), 
you are able to run 'run_simulations_csv', and then use the function export_results(results).
'''
def run_simulations(setups, num_simulations):
    results = {setup_name: [] for setup_name in setups.keys()}
    for setup_name, setup in setups.items():
        for _ in range(num_simulations):
            p1_role = Role('mage', setup)
            p2_role = Role('range', std_weapons_range)
            if setup_name in ['std_weapons_mage', 'std_weapons_mage_dart', 'std_weapons_mage_lb']:
                setup_type = 'std'
            else:
                setup_type = 'shadow'            
            players = [Player(role=p1_role, setup_type=setup_type), Player(role=p2_role)]
            boss = NyloBoss()
            fight_duration = simulate_fight(players, boss)
            results[setup_name].append(fight_duration)
    return results

def run_simulations_csv(setups, num_simulations):
    results = {setup_name: [] for setup_name in setups.keys()}
    for setup_name, setup in setups.items():
        for _ in range(num_simulations):
            p1_role = Role('mage', setup)
            p2_role = Role('range', std_weapons_range)
            if setup_name in ['std_weapons_mage', 'std_weapons_mage_dart', 'std_weapons_mage_lb']:
                setup_type = 'std'
            else:
                setup_type = 'shadow'
            players = [Player(role=p1_role, setup_type=setup_type), Player(role=p2_role)]
            boss = NyloBoss()
            fight_duration = simulate_fight(players, boss)
            results[setup_name].append(fight_duration)
    return results


num_simulations = 10000 # Define the number of simulations to run
results = run_simulations(setups, num_simulations) # Run the simulations as described above
output_results(results) # Output the simulations neatly in the terminal.

#to output a csv:
#results = run_simulations_csv(setups, num_simulations)
#export_results(results)