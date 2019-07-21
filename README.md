# Pokemon Population Models
This is a project meant to back up the theory that starter pokemon are so rare due to a genetic disadvantage caused by a sex ratio of 7 males to 1 female within starter pokemon specices (including the amazing bulbasaur). This is done by comparing the populations of multiples species over time and how the effect of sex ratio of these species affects the populations. 

You can hear more about the purpose of this script in the [YouTube video](https://www.youtube.com/watch?v=OccWmmaCqlE)

# Simplifications by Austin
+ All species use the same egg cycle
+ As long as 
+ 'Human' impact on the environment is shown by dropping the fertility rate down to the same rate as if there were no remaining males within the populaiton and the females were forced to breed with other species within the same egg group.

## Planned changes by me
+ Incorporate egg groups into population growth more directly rather than just having the species be allowed to stay alive if there are females within the population
+ Create a population pyramid that shows the ratio of males to females at a particular tick.
+ Generation of the population graph by the python script
+ Model out the habitats of these pokemon and model which pokemon 
+ Incorporate the mechanisms from all generations that are used to determine gender
    + Gen II - Attack stat
    + Gen III/IV -
    + Gen V/VI - 

# Supporting info on the theory
After reading over the data in sex_ratios.json I saw that the pokemon that you can only obtain through fossils (Omanyte, Kabuto, Aerodactyl) all had the same 7:1 male to female sex ratio expressed within starter pokemon. Hinting that this sex ratio may have also been the reason for their extinction, and the reason why they went extinct and the starter pokemon are only endangered is because those extinct pokemon also had much longer egg cycles. These longer egg cycles made it so that it took much longer for their young to mature.

There is also the fact that in Generation II of pokemon, the sex of a pokemon is based off of its attack state. Although the sentiment expressed in the games is that human and pokemon coexist, it is obvious that humans use them excessively in glorified dog-fighting and as such would probably breed them to have very high attack stats. Especially pokemon as strong as starter pokemon. This selective breeding would over time make them have an unnatural ratio of males to females and would help explain how they came to get a trait that is obviously evolutionarily unfavorable.

# Outstanding Questions
+ Should growth rate be added in as a variable for modeling population trends. This value is normally used to determine how much experience it takes for a pokemon to level up. Though level and evolution status do not determine fertility in the pokemon games, and even a newborn pokemon are fertile. Though it is still worth noting that all newly hatched pokemon are level 1 indiciating that it at least has something to do with age and fertility, and could be incorporated into a theory with the basis that the reason that levels aren't used to determine if a pokemon is able to breed is to reduce the hassle on players.

# Community Guidlines
+ Please use docstrings as much as possible in any additions of your code and have them follow [PEP 257](https://www.python.org/dev/peps/pep-0257/)
+ Try to keep your commits descriptive
+ In general make any additions you can as informative as possible. This repo was created by an education channel, and as such this code should strive to be a good source of education for people who want to understand programming and the reasonings behind the theory.
+ Do **NOT** be outright hateful about any code written by Austin or any one who contributes to this codebase. Constructive criticism is a much better way to get your points across.
+ Tabs are evil.