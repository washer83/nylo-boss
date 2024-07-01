import statistics
import csv
import random

'''
Boss simluation functions.
simulate_fight:
    - Operates primarily based on tick, which is a counter that determines when the boss
    should change phases, when the players can hit, and when thralls should hit. 
    - Logic is as follows:
        - While the boss is > 0 hp, run the simulation. Count down from 10 to determine when to change phases.
        - Each tick, the player will try to attack (but be blocked by cooldown if it's too early, happens in (playerClass.py))
        - Thralls attack every 4 ticks, and roll from 1 to 3.
    
output_results:
    - Outputs the results in the terminal in a neat format.

export_results:
    - Export the results to a csv.
'''

def simulate_fight(players, boss):
    tick = 0
    thrall_tick = 0  
    
    while boss.health > 0:
        if boss.phase_timer == 0:
            boss.change_phase(tick)
        boss.phase_timer -= 1
        for player in players:
            player.attack(boss, tick)
        
        # Thrall attack every 4 ticks
        if thrall_tick == 4:
            thrall_damage = random.randint(1, 3)
            boss.take_dmg(thrall_damage)
            thrall_tick = 0  # Reset thrall tick counter

        tick += 1
        thrall_tick += 1  # Increment thrall tick counter
        
    return tick
def output_results(results):
    print(f"{'setup_name':<25} {'avg_duration':<15} {'std_dev':<10} {'minimum':<8} {'maximum':<8}")
    for setup_name, durations in results.items():
        average_duration = statistics.mean(durations)
        std_deviation = statistics.stdev(durations)
        min_duration = min(durations)
        max_duration = max(durations)
        print(f"{setup_name:<25} {average_duration:<15.3f} {std_deviation:<10.3f} {min_duration:<8} {max_duration:<8}")
    return

def export_results(results):
    # Transpose results for CSV export
    transposed_results = list(zip(*[durations for durations in results.values()]))

    # Export results to CSV
    with open('fight_durations.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(results.keys())  # Write column headers
        writer.writerows(transposed_results)

    print("Fight durations saved to fight_durations.csv")