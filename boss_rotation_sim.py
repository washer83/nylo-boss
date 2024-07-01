import random
import csv

class NyloBoss:
    def __init__(self):
        self.health = 1875
        self.phase = 'melee'  # Initialize the phase
        self.prev_phase = None
        self.phase_timer = 10
        self.phases = ['magic', 'ranged', 'melee']
        self.phase_log = ['M']  # Initialize with the starting phase
        self.phase_counts = {'magic': 0, 'ranged': 0, 'melee': 1}

    def change_phase(self, current_tick):
        self.prev_phase = self.phase
        next_phase = [phase for phase in self.phases if phase != self.phase]
        self.phase = random.choice(next_phase)
        self.phase_timer = 10
        self.phase_counts[self.phase] += 1  # Increment phase count
        phase_map = {'magic': 'G', 'ranged': 'R', 'melee': 'M'}  # Phase mapping
        self.phase_log.append(phase_map[self.phase])  # Log the phase change

def simulate_boss_transitions(num_ticks, rota, num_sims):
    total_counts = {transition: 0 for transition in rota}
    
    for _ in range(num_sims):
        boss = NyloBoss()
        for tick in range(num_ticks):
            if boss.phase_timer == 0:
                boss.change_phase(tick)
            boss.phase_timer -= 1
        
        phase_sequence = ''.join(boss.phase_log)
        for transition in rota:
            total_counts[transition] += phase_sequence.count(transition)
    
    avg_counts = {transition: total_counts[transition] / num_sims for transition in rota}
    return avg_counts

def main(num_ticks, rota, num_sims):
    avg_results = simulate_boss_transitions(num_ticks, rota, num_sims)
    print(f"Results from {num_sims} simulations of {num_ticks} tick bosses.")
    for transition, avg_count in avg_results.items():
        print(f"Average instances of {transition} per simulation: {avg_count:.2f}")

if __name__ == "__main__":
    num_ticks = 150  
    rota = ["GR", "GM"]  
    num_sims = 100000  
    main(num_ticks, rota, num_sims)
