"""
# No Genderless
# Tyrogue = Hitmonlee/Hitmonchan
# No Chansey
# No Kangaskhan
# No Tauros
# This is due to the fact that their species only have pokemon of one
# gender meaning that they either must only mate with pokemon of another species
# within the same egg group, or they must have a secondary means of reproduction, 
# which is beyond the scope of this simple script
"""
from argparse import ArgumentParser
from collections import deque
from csv import DictWriter
from random import randint

CSV_FILE = "BulbasaurPopulation.csv"
FIELD_NAMES = ['tick', 'female', 'male']
# Not sure the exact meaning of this number. 
# It feels two specific to be random.
DEATH_THRESHOLD = 243
MAX_POPULATION = 20000
EGG_CYCLE = 20

# According to PEP 8, all functions and variables should be named with snake_case.
def csv_write_header():
    # There is no need to call csv_file.close()
    # since files are also ContextManagers meaning 
    # that they handle all cleanup code when they exit the block
    # including when errors occur.
    # Look into PEP 343 for ore information
    with open(CSV_FILE, 'w', newline='') as csv_file:
        writer = DictWriter(csv_file, fieldnames=FIELD_NAMES)
        writer.writeheader()

def csv_write_row(tick, population):
    with open(CSV_FILE, 'a', newline='') as csv_file:
        writer = DictWriter(csv_file, fieldnames=FIELD_NAMES)
        row = {'tick': tick}
        row.update(population)
        writer.writerow(row)

def death_tick(population, sex):
    """

    """
    for _ in range(population[sex]):
        death = randint(1, 10000)
        if death <= DEATH_THRESHOLD:
            population[sex] -= 1

def hatch_tick(eggs_ready_to_hatch, population):
    """

    """
    print("{} Bulbasaur eggs are hatching!".format(eggs_ready_to_hatch))
    for _ in range(eggs_ready_to_hatch):
        sexroll = randint(1, 8)
        # Bulbasaur have a 7:1 gender ratio.
        if sexroll <= 7:
            population["male"] += 1
        else:
            population["female"] += 1

def lay_eggs(fertility_rate, female_pop):
    """
    For every female in the population of the species,
    a check is made if they have a child this tick.

    TODO: Check if this is done in the same way as within the pokemon games.
    """
    eggs_lain = 0
    # Unused variables are best named _
    for _ in range(female_pop):
        lay_egg = randint(1, 100)
        if lay_egg <= fertility_rate:
            eggs_lain += 1
    return eggs_lain

def main():
    # Parses out any command line arguments
    parser = ArgumentParser()
    parser.add_argument("--human", action='store_true', 
                                help="Toggles human interaction in the environment")
    vargs = parser.parse_args()

    # Simple 7:1 starting population
    population = {"male": 14, "female": 2}
    male_pop = 14
    female_pop = 2
    tick = 0
    # Length of 21
    # I think this has to do with egg cyles and how the egg cycle for Bulbasaur is 20 
    # So an egg at index 0 is 
    current_cycle = 0
    # The egg cycle for bulbasaurs is 20, so we want to make our deque that size.
    eggs = deque([0] * EGG_CYCLE)
    csv_write_header()

    while True:
        csv_write_row(tick, population)
        tick += 1
        print("Tick:", tick)
        death_tick(population, "female")
        death_tick(population, "male")
        
        # We effectively want to move all generations forward
        # And hatch all the eggs for the newest generation and determine
        # their sexes 
        eggs_ready_to_hatch = eggs.popleft()
        # No need to check if eggs_ready_to_hatch is non-zero
        # as hatch_tick does an iteration for each integer between
        # 0 and the number of eggs ready to hatch. Which for 0, is a nop.
        hatch_tick(eggs_ready_to_hatch, population)

        fertility_rate = 0
        # Introduction of humans to the population
        # causing the fertility rate of pokemon to drop
        # down to the same level as if there were no males in 
        # the population.
        if population["male"] >= 1 and (tick <= 100 and vargs.human):
            fertility_rate = 50
        elif population["female"] >= 1:
            # There are no males of this species left, so
            # the females are forced to breed
            fertility_rate = 10
        
        # Creates the new generation of eggs
        eggs.append(lay_eggs(fertility_rate, population["female"]))

        total_population = sum(population.values())
        print("Total Population: {}".format(total_population))
        print("Females: {}".format(population["female"]))
        print("Males: {}".format(population["male"]))
        print("")

        # Preferably our population won't go extinct so add in a condition
        # if our population absolutely *EXPOLODES*
        if total_population >= MAX_POPULATION:
            print("Population max reached")
            break

        # Pokemon can mate with other species of pokemon within their egg group
        # and produce offspring of the female's species. Therefore a species isn't truly
        # extinct until all offspring and females of that species are dead.
        elif population["female"] <= 0 and not any(eggs):      
            print("Extinction")
            break

# It is usually best practice to add
# this snippet to the end of your main python script.
# This snippet ensures that no body code gets executed unless it
# was intentionally invoked as the main script rather than as a module.
if __name__ == "__main__":
    main()