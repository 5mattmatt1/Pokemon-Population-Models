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
# Built-ins
from argparse import ArgumentParser
from collections import deque
from csv import DictWriter, DictReader
from random import randint, random
import json
# Libraries gotten from pip
from matplotlib import pyplot as plt

CSV_FILE = "{}_population.csv"
# CSV_FILE = "bulbasaur_population.csv"
SPECIES_DATA_FILE = "species_data.json"
FIELD_NAMES = ['tick', 'female', 'male']
# Not sure the exact meaning of this number. 
# It feels two specific to be random.
# The only thing I could think of is that it is roughly
# The threshold required for a member of a population to 
# have a 50% chance to die every egg cycle.
DEATH_THRESHOLD = 243
STARTING_POPULATION = 16
MAX_POPULATION = 20000
EGG_CYCLE = 20

# According to PEP 8, all functions and variables should be named with snake_case.
def csv_write_header(species):
    """
    Create a new csv file for the given species
    and writes the header to it so that it can be read in later.
    """
    # There is no need to call csv_file.close()
    # since files are also ContextManagers meaning 
    # that they handle all cleanup code when they exit the block
    # including when errors occur.
    # Look into PEP 343 for ore information
    csv_file_name = CSV_FILE.format(species)
    with open(csv_file_name, 'w', newline='') as csv_file:
        writer = DictWriter(csv_file, fieldnames=FIELD_NAMES)
        writer.writeheader()

def csv_write_row(species, tick, population):
    """
    Writes a new row to the csv file for the given species
    detailing the population for the current tick.
    """
    csv_file_name = CSV_FILE.format(species)
    with open(csv_file_name, 'a', newline='') as csv_file:
        writer = DictWriter(csv_file, fieldnames=FIELD_NAMES)
        row = {'tick': tick}
        row.update(population)
        writer.writerow(row)

def death_tick(population, sex):
    """
    For every member of a population of the given sex,
    do a check to see if they should die this tick.
    """
    for _ in range(population[sex]):
        death = randint(1, 10000)
        if death <= DEATH_THRESHOLD:
            population[sex] -= 1

def hatch_tick(eggs_ready_to_hatch, population, male_ratio):
    """
    Hatches all eggs for this tick and determines their sex and increases 
    the population of the corresponding sex.
    """
    print("{} eggs are hatching!".format(eggs_ready_to_hatch))
    for _ in range(eggs_ready_to_hatch):
        # random.random generates a float between [0.0, 1.0) making it ideal for working
        # with percentages.
        sexroll = random()
        if sexroll <= male_ratio:
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

def generate_plot(species):
    """
    Uses matplotlib to generate a simple plot
    from the data in the exported csv file.
    """
    # Labels the axises and title of the plot
    plt.title("Pokemon Population Model")
    plt.ylabel("Population of {}".format(species))
    plt.xlabel("Tick")

    xaxis_ticks = []
    yaxis_male_pop = []
    yaxis_female_pop = []

    csv_file_name = CSV_FILE.format(species)
    with open(csv_file_name, 'r', newline='') as csv_file:
        for row in DictReader(csv_file):
            # Matplotlib is not a fan of non-float values
            xaxis_ticks.append(float(row["tick"]))
            yaxis_female_pop.append(float(row["female"]))
            yaxis_male_pop.append(float(row["male"]))

    plt.plot(xaxis_ticks, yaxis_female_pop, label="Female Population")
    plt.plot(xaxis_ticks, yaxis_male_pop, label="Male Population")
    plt.legend()
    plt.show()

def get_species_data(species):
    """
    Simply reads in the JSON file holding all the species data for species within
    the Kanto region.
    """
    with open(SPECIES_DATA_FILE, 'r') as json_file:
        try:
            species_data = json.load(json_file)[species]
        except KeyError as e:
            print("Species {} not found".format(species))
    return species_data

def get_raw_sex_ratio(species):
    """
    Reads in the raw sex ratio from the species data JSON file and simply breaks it out
    into raw male and female sex ratios.
    """
    species_data = get_species_data(species)
    try:
        sex_ratio = species_data["sex_ratio"]
    except KeyError as e:
        print("Malformed JSON entry")
    male_ratio_raw, female_ratio_raw = sex_ratio.split(":")
    return int(male_ratio_raw), int(female_ratio_raw)

def convert_sex_ratio(male_ratio_raw, female_ratio_raw):
    """
    Converts between the raw ratio to the percentages for each
    Example: 7:1 raw ratio to 87.5% male and 12.5% male
    """
    total_raw = float(male_ratio_raw + female_ratio_raw)
    male_ratio = male_ratio_raw / total_raw
    female_ratio = female_ratio_raw / total_raw

    return (male_ratio, female_ratio)

def get_sex_ratio(species):
    """
    Simple shorthand for using get_raw_sex_ratio and converting it to percentages.
    """
    male_ratio_raw, female_ratio_raw = get_raw_sex_ratio(species)
    return convert_sex_ratio(male_ratio_raw, female_ratio_raw)

def main():
    # Parses out any command line arguments
    parser = ArgumentParser()
    parser.add_argument("--human", action='store_true', 
                                help="Toggles human interaction in the environment")
    parser.add_argument("species", action='store', nargs='?', default="bulbasaur",
                                help="Which species of pokemon to simulate")
    vargs = parser.parse_args()

    species_data = get_species_data(vargs.species)
    male_ratio, female_ratio = get_sex_ratio(vargs.species)

    # Creates a starting population based on the sex ratio of that species
    population = {"male": int(round(male_ratio * STARTING_POPULATION)), 
                  "female": int(round(female_ratio * STARTING_POPULATION))}
    tick = 0
    # Length of 21
    # I think this has to do with egg cyles and how the egg cycle for Bulbasaur is 20 
    # So an egg at index 0 is 
    current_cycle = 0
    # The egg cycle for bulbasaurs is 20, so we want to make our deque that size.
    eggs = deque([0] * species_data["egg_cycles"])
    csv_write_header(vargs.species)

    while True:
        csv_write_row(vargs.species, tick, population)
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
        hatch_tick(eggs_ready_to_hatch, population, male_ratio)

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
    generate_plot(vargs.species)

# It is usually best practice to add
# this snippet to the end of your main python script.
# This snippet ensures that no body code gets executed unless it
# was intentionally invoked as the main script rather than as a module.
if __name__ == "__main__":
    main()