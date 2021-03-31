import os

import math
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

'''
This is the full lockdown case. Difference from the control (no_lockdown_case.py):

- People who are infected will stop moving, just like in the self quarantine (self_quarantine_case.py) case.
- The overall movement speed is slowed for everyone.
'''

POPULATION_SIZE = 350

INFECT_DIST = 0.04
INFECT_CHANCE = 0.07

SPEED_RANGE = [0.001, 0.005]

DEATH_CHANCE = 0.04
ELDERLY_DEATH_CHANCE = 0.1

TIME_INFECTED = 70
SELF_QUARANTINE_TIME = 20 # time it takes for someone infected to stop moving, being the asymptomatic phase of covid

def population_setup(population_size):
    # setup function, loops for every person and assigns random values.
    # only the age uses a normal distribution, because age isnt a uniform distribution in real life

    population = []

    for i in range(0, population_size):
        # set status 0 = healthy, 1 = sick, 2 = immune, 3 = dead
        status = 0
        age = np.random.normal(45, 90)
        x_pos = random.uniform(0, 1)
        y_pos = random.uniform(0, 1)
        x_dir = random.uniform(-1, 1)
        y_dir = random.uniform(-1, 1)
        speed = random.uniform(SPEED_RANGE[0], SPEED_RANGE[1])
        infected_since = 0

        population.append([status, age, x_pos, y_pos, x_dir, y_dir, speed, infected_since])
    return population

def movement_update(population):
    # this function adjusts the position using the positions, headings and speeds.

    for i in population: 
        i[2] = i[2] + (i[4] * i[6])
        i[3] = i[3] + (i[5] * i[6])
 
def check_infect(population, current_frame):
    # this function loops every infected person and checks if anyone is nearby them.
    # this is horribly inefficient, but this code's main purpose is being exported to a png sequence so it doesn't matter as much
    # also i made this in a day for the FLEXweek, what do you expect of me

    for i in population:
        if i[0] == 1:
            for j in population:
                if math.sqrt((j[2] - i[2])**2 + (j[3] - i[3])**2) < INFECT_DIST and j[0] == 0:
                    if random.uniform(0,1) < INFECT_CHANCE:
                        j[0] = 1
                        j[7] = current_frame

def live_or_die(population, frame):
    # loops every frame to see if anyone has reached passed TIME_INFECTED frames.
    # i chose the age of 65 because the odds of death seem to rise significantly after 65 y/o according to 
    # https://www.acsh.org/news/2020/11/18/covid-infection-fatality-rates-sex-and-age-15163

    # todo: make death odds scale with age 

    for i in population:
        if i[0] == 1 and frame - i[7] >= TIME_INFECTED:
            death_random = random.uniform(0, 1)

            if i[1] < 65 and death_random <= DEATH_CHANCE:
                i[0] = 3
                i[6] = 0
            elif i[1] < 65 and death_random > DEATH_CHANCE:
                i[0] = 2

                # this is special for this file too, everyone who was infected stopped moving, so they'll have to move again
                i[6] = random.uniform(SPEED_RANGE[0], SPEED_RANGE[1])

            if i[1] >= 65 and death_random <= ELDERLY_DEATH_CHANCE:
                i[0] = 3
                i[6] = 0
            elif i[1] >= 65 and death_random > ELDERLY_DEATH_CHANCE: 
                i[0] = 2

                # this is special for this file too, everyone who was infected stopped moving, so they'll have to move again
                i[6] = random.uniform(SPEED_RANGE[0], SPEED_RANGE[1])

def wall_bounce(population):
    for i in population:
        if i[2] <= 0 or i[2] >= 1:
            i[4] = i[4] * -1

        if i[3] <= 0 or i[3] >= 1:
            i[5] = i[5] * -1

def self_quarantine(population, frame):
    # this function makes this file different from no_lockdown_case.py, in that anyone who is infected will stop moving
    # after a certain number of frames (to take the asymptomatic stage of the virus into account)

    for i in population:
        if i[0] == 1 and frame - i[7] >= SELF_QUARANTINE_TIME:
            i[6] = 0

def update(frame, population, infected_plot=[], death_plot=[]):
    if frame == 10:
        population[0][0] = 1
        population[0][7] = 10

    main_plot.clear()
    infected_over_time.clear()

    movement_update(population)
    wall_bounce(population)
    check_infect(population, frame)
    live_or_die(population, frame)

    self_quarantine(population, frame) # the special function for this case

    # making arrays for the coordinates of healthy people
    healthy_x = []
    healthy_y = []

    # making arrays for the coordinates of infected people
    infected_x = []
    infected_y = []

    immune_x = []
    immune_y = []

    dead_x = []
    dead_y = []

    # appending the correct arrays
    for i in population:
        if i[0] == 0: # if healthy, append to healthy x and y
            healthy_x.append(i[2])
            healthy_y.append(i[3])

        elif i[0] == 1: # if infected, append to infected x and y
            infected_x.append(i[2])
            infected_y.append(i[3])

        elif i[0] == 2: # if immune, append to immune x and y
            immune_x.append(i[2])
            immune_y.append(i[3])
        
        elif i[0] == 3: # if dead, append to dead x and y
            dead_x.append(i[2])
            dead_y.append(i[3])

    # append newest data to plotting array for graph
    infected_plot.append(len(infected_x) / POPULATION_SIZE * 100)
    death_plot.append(len(dead_x) / POPULATION_SIZE * 100)

    # set title and credit
    main_plot.set_title('Full lockdown case')

    # set autoscale to false
    main_plot.autoscale(False)

    #hide axes on simulation
    main_plot.axes.get_xaxis().set_ticks([])
    main_plot.axes.get_yaxis().set_ticks([])

    main_plot.scatter(healthy_x, healthy_y, color='green', s=3, label='healthy')
    main_plot.scatter(infected_x, infected_y, color='red', s=3, label='infected')
    main_plot.scatter(immune_x, immune_y, color='blue', s=3, label='immune')
    main_plot.scatter(dead_x, dead_y, color='gray', s=3, label='dead')

    # set up graph
    infected_over_time.set_title('Infection cases over time')

    infected_over_time.set_xlim(0, frame + 1)
    infected_over_time.set_ylim(0, 100)

    # set labels
    infected_over_time.set_xlabel('Time (frames)')
    infected_over_time.set_ylabel('% of the population')

    infected_over_time.plot(infected_plot, color='red')
    infected_over_time.plot(death_plot, color='gray')

    # export to the render folder made in the main function
    plt.savefig('render/%s.png' %frame) # export individual frames


if __name__ == '__main__':
    simulation_steps = 1000

    population = population_setup(POPULATION_SIZE) # use setup function to initialize population array 

    # some wacky matplotlib code i don't really understand
    fig = plt.figure(figsize=(5,7))
    spec = fig.add_gridspec(ncols=1, nrows=2, height_ratios=[5,2])
    
    main_plot = fig.add_subplot(spec[0,0])
    
    # set the limits for the main plot
    main_plot.set_xlim(0, 1)
    main_plot.set_ylim(0, 1)

    # create second plot to graph infections and deaths
    infected_over_time = fig.add_subplot(spec[1,0])

    # make rendering folder to export png sequence to
    if not os.path.exists('render/'):
        os.makedirs('render/')

    animation = FuncAnimation(fig, update, fargs=(population,), frames=simulation_steps, interval=33)
    plt.show()