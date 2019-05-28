# Traffic Simulator using Cellular Automata

import numpy as np
import random

#import matplotlib
#matplotlib.use("TkAgg")
#import matplotlib.pyplot as plt


# Class Definitions
# Vehicle Class
class Vehicle:
    def __init__(self, precede_veh, trail_veh, position, curr_speed, new_speed, is_target_veh, enter_time):
        self.precede_veh = precede_veh
        self.trail_veh = trail_veh
        self.position = position
        self.curr_speed = curr_speed
        self.new_speed = new_speed
        self.dist_to_precede_veh = -1
        self.is_target_veh = is_target_veh
        self.enter_time = enter_time

    def update_speed(self, max_speed):
        # First, obtain the distance between it and the preceding vehicle
        if self.precede_veh != None:
            self.dist_to_precede_veh = self.precede_veh.position - self.position - 1
        else:
            self.dist_to_precede_veh = -1

        # Update Rule 1: always try to reach the max speed limit
        self.new_speed = min(self.curr_speed + 1, max_speed)

        # Update Rule 2: maintain the current nonzero speed with 40% probability
        if random.randint(1, 100) < 40:
            if self.curr_speed > 0:
                self.new_speed = self.curr_speed

        # Update Rule 3: reduce speed by 1 with 30% probability (due to random factors on road,
        # or erratic driving)
        if random.randint(1, 100) < 30:
            self.new_speed = max(self.curr_speed - 1, 0)

        # Update Rule 4: reduce speed  based on the preceding vehicle
        if self.dist_to_precede_veh != -1:
            self.new_speed = min(self.new_speed, self.dist_to_precede_veh)

    def update_position(self):
        self.position = self.position + self.new_speed
        self.curr_speed = self.new_speed


# Helper functions for the main simulation loop
def UpdateAllVehsSpeed(lead_veh, max_speed):
    curr_veh = lead_veh
    while curr_veh != None:
        curr_veh.update_speed(max_speed)
        curr_veh = curr_veh.trail_veh


def UpdateAllVehsPosition(lead_veh, tail_veh, intersections_pos, traffic_lights_timing, turn_at_xroad_prob, curr_time):
    prev_veh = None
    curr_veh = lead_veh
    new_lead_veh = lead_veh
    new_tail_veh = tail_veh

    while curr_veh != None:
        next_veh = curr_veh.trail_veh
        passing_xroad_idx = CheckIfAtXroad(curr_veh, intersections_pos, traffic_lights_timing, curr_time)
        if passing_xroad_idx != -1:
            if random.randint(1, 100) < turn_at_xroad_prob[passing_xroad_idx]:
                # the current car is turning at this current intersection
                if prev_veh != None:
                    if next_veh != None:
                        prev_veh.trail_veh = next_veh
                        next_veh.precede_veh = prev_veh
                        curr_veh = next_veh
                    else:
                        prev_veh.trail_veh = None
                        new_tail_veh = prev_veh
                        curr_veh = None
                else:
                    if next_veh != None:
                        next_veh.precede_veh = None
                        new_lead_veh = next_veh
                        curr_veh = next_veh
                    else:
                        new_lead_veh = None
                        new_tail_veh = None
                        curr_veh = None
            else:
                curr_veh.update_position()
                prev_veh = curr_veh
                curr_veh = curr_veh.trail_veh
        else:
            curr_veh.update_position()
            prev_veh = curr_veh
            curr_veh = curr_veh.trail_veh

    return new_lead_veh, new_tail_veh

def CheckIfAtXroad(curr_veh, intersections_pos, traffic_lights_timing, curr_time):
    passing_intersection_number = -1

    curr_veh_curr_pos = curr_veh.position
    curr_veh_new_pos = curr_veh.position + curr_veh.new_speed
    for i in range(len(intersections_pos)):
        if curr_veh_curr_pos <= intersections_pos[i] and curr_veh_new_pos > intersections_pos[i]:
            # if this car is at an intersection, then first check for traffic lights
            if CheckTrafficLights(i, traffic_lights_timing, curr_time) == 1:
                passing_intersection_number = i
            else:
                curr_veh.new_speed = 0
            break

    return passing_intersection_number


def CheckTrafficLights(lights_number, traffic_lights_timing, curr_time):
    light_green_now = 0
    light_green_duration = traffic_lights_timing[lights_number][0]
    light_red_duration = traffic_lights_timing[lights_number][1]
    light_period_duration = light_green_duration + light_red_duration
    if (curr_time % light_period_duration) < light_green_duration:
        light_green_now = 1

    return light_green_now


############################### Simulator Initial Setup ########################################

# based on the dataset, the length of car is set to 16ft for all vehicles
############### Road COndition Data ####################
# Road Section 1:
# length : 99+127 = 226ft  226/16 = 15 cells
# traffic lights 1: position: cell 14
# Road Section 2:
# length : 442+130 = 572ft  572/16 = 36 cells
# traffic lights 2: position: cell 50
# Road Section 3:
# length : 412+74 = 486ft  486/16 = 31 cells
# traffic lights 3: position: cell 81
# Road Section 4:
# length : 354+67 = 421ft  421/16 = 27 cells
# traffic lights 4: position: cell 108
# Road Section 5:
# length : 344+118 = 462ft  462/16 = 29 cells
# traffic lights 5: position: cell 137

num_cells = 137  # The number of cells along the road
max_speed = 4    # posted max speed is 51 ft/s = 3 cells/s, but the actual car speed is around 56 ft/s = 4 cells/s
init_num_veh = 0

# intersections setup
intersections_pos = [14, 50, 81, 108, 137]
turn_at_xroad_prob = [10, 10, 10, 10, 0]

# traffic lights timing setup
# i-th light: (green time duration, red)
traffic_lights_timing = [(38,49),(45,55),(64,36),(20,0),(38,46)]

# Next, in each cell, put a vehicle randomly (coin flip)
lead_veh = None
prev_veh = None
curr_veh = None
tail_veh = None


################################### Main Simulation Loop ########################################
curr_time = 0
num_veh_entered = 0
desired_num_veh_entered = 1000
total_num_arrived_veh = 0
num_arrived_target_veh = 0
total_target_veh_travel_time = 0
average_target_veh_travel_time = 0
is_road_empty = 1

# Variables for plotting purpose
avg_travel_time_vs_num_veh_entered = []

# Generate the inter-arrival times for the vehicles based on a fitted Poisson distribution
inter_arrival_times = np.random.poisson(1, desired_num_veh_entered)
next_veh_arrival_time = inter_arrival_times[0]
if next_veh_arrival_time <= 0:
    next_veh_arrival_time = 1

while num_arrived_target_veh < 400:
    curr_time = curr_time + 1  # increment time step
    UpdateAllVehsSpeed(lead_veh, max_speed)  # update all the vehicles' speed
    lead_veh, tail_veh = UpdateAllVehsPosition(lead_veh, tail_veh, intersections_pos, traffic_lights_timing, turn_at_xroad_prob, curr_time)  # update all the vehicles' position

    if lead_veh == None:
        is_road_empty = 1
    else:
        is_road_empty = 0

    # check if any vehicles have exited the road section
    while is_road_empty != 1 and lead_veh.position >= num_cells:
        total_num_arrived_veh += 1
        # if this exiting vehicle is a target one, then record its total travel
        # time on this road section
        if lead_veh.is_target_veh == 1:
            num_arrived_target_veh += 1
            total_target_veh_travel_time += curr_time - lead_veh.enter_time
            average_target_veh_travel_time = total_target_veh_travel_time / num_arrived_target_veh
            avg_travel_time_vs_num_veh_entered.append(average_target_veh_travel_time)
        lead_veh = lead_veh.trail_veh
        if lead_veh == None:
            is_road_empty = 1
            tail_veh = None
        else:
            lead_veh.precede_veh = None

    # randomly create new vehicle to enter the road section
    # mark it as a target one, since its total travel time
    # will be recorded
    if curr_time == next_veh_arrival_time:
        if tail_veh == None:
            init_speed = random.randint(1, max_speed)
            new_enter_vehicle = Vehicle(None, None, 0, init_speed, 0, 1, curr_time)
            lead_veh = new_enter_vehicle
            tail_veh = new_enter_vehicle
            num_veh_entered += 1

        else:
            if tail_veh.position != 0:
                init_speed = random.randint(1, max_speed)
                new_enter_vehicle = Vehicle(tail_veh, None, 0, init_speed, 0, 1, curr_time)
                tail_veh.trail_veh = new_enter_vehicle
                tail_veh = new_enter_vehicle
                num_veh_entered += 1

        next_veh_arrival_time = curr_time + inter_arrival_times[num_veh_entered-1]
        if next_veh_arrival_time <= curr_time:
            next_veh_arrival_time = curr_time + 1


print('Simulation Complete')
print('The average travelling time is (in sec): ')
print(average_target_veh_travel_time)


####### This is for plotting the output plots #######
#plt.plot(avg_travel_time_vs_num_veh_entered)
#plt.xlabel('Number of Finished Vehicles')
#plt.ylabel('Average Travelling Time (s)')
#plt.title('Output Plot with Pre-fitted Poisson Inter-Arrival Time Distribution')
#plt.show()
