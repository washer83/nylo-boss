import random

'''
Nylo boss class.
Default attributes:
    - health: 1875 (for a solo, duo, or trio)
    - phase: initial phase
    - prev_phase: storage of the previous phase (for tick fixes)
    - prev_prev_phase: 2 phases ago, in case i get bullied into adding even more fixes
    - phase_timer: time in ticks before a phase change occurs
    - phases: phase options (mage, range, melee)
    - last_phase_change_tick: tracking to know when to change phase
    - defence_rolls: nylo boss defence rolls at 0 defence. 
    - phase_counts: track how many of each phase the boss gets
    - phase_log: track how the boss changes between phases

func change_phase():
    - prev_prev_phase: as described
    - prev_phase: as described
    - phase: choose between the two phases that it currently isn't
    - phase_timer: same as above
    - last_phase_change_tick: storage of when it has changed
    - phase_counts: above
    - phase_log: above
'''
class NyloBoss:
    def __init__(self):
        self.health = 1875
        self.phase = 'melee' 
        self.prev_phase = None
        self.prev_prev_phase = None
        self.phase_timer = 10 
        self.phases = ['magic', 'ranged', 'melee']
        self.last_phase_change_tick = -1  
        self.defence_rolls = {
            'magic': 3776,
            'ranged': 576,
            'melee': 576
        }
        self.phase_counts = {'magic': 0, 'ranged': 0, 'melee': 1}  # Track phase occurrences
        self.phase_log = ['M']  # Initialize with the starting phase

    def change_phase(self, current_tick):
        self.prev_prev_phase = self.prev_phase
        self.prev_phase = self.phase
        next_phase = [phase for phase in self.phases if phase != self.phase]
        self.phase = random.choice(next_phase)
        self.phase_timer = 10
        self.last_phase_change_tick = current_tick
        self.phase_counts[self.phase] += 1  # Increment phase count
        phase_map = {'magic': 'G', 'ranged': 'R', 'melee': 'M'}  # Phase mapping
        self.phase_log.append(phase_map[self.phase])  # Log the phase change
        #unmute below to debug
        #print(f'----- Boss switched from {self.prev_phase} to {self.phase} -----')

    def take_dmg(self, damage):
        self.health -= damage #reduce hp by dmg
        return damage
    
    def get_defence_roll(self, style):
        return self.defence_rolls.get(style, 11111111)  # Default to a base value if style is not found