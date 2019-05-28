import random
import sys
#import matplotlib.pyplot as plt
#from scipy.stats import binom, norm, beta, expon
import numpy as np

'''Author: Yuhao Chen
   Gtid: 903427793
   Date: 2019/4/1
'''

sys.setrecursionlimit(2147483647)


class Car:
    def __init__(self, onetime, carindex, alight, onelist, onestr, onenumber, number,vcount):
        self.Curr_time = onetime
        self.Index = carindex
        self.Curr_traffic_light = alight
        self.arrivetime = onelist
        self.Event = onestr
        self.Processtime = onenumber
        self.cap = number
        self.valid = 1


#Event = {"arrive", "running_on_road", "waiting_for_light"}

'''define the interarrival time to be a random value to simulate traffic'''


def random_arrival_time(n):
    time_list = [0]
    dt = 0
    for i in range(n-1):
        dt = dt + random.random()*50
        time_list.append(dt)
    return time_list


def out_or_not():
    tempX = random.randint(0, 100)
    if tempX > 90:
        return True
    else:
        return False


def red_or_green(test_time):
    if test_time % 40 < 25:
        return False
    else:
        return True


def to_green_time(test_time):
    target_time = (test_time//40)*40+25
    waiting_time = target_time - test_time
    return waiting_time


def arrive(car_flag):
    if car_list[car_flag].Event != "arrive":
        print("Unexpected Event happen!")
    if car_list[car_flag].Curr_traffic_light == 5:
        already_pass_cars[car_list[car_flag].Curr_traffic_light - 1] += 1
        # print("The "+str(car_list[car_flag].Index)+"th car has arrived the destination region!" + "\n" +
              # "At the time of "+str(car_list[car_flag].Curr_time))
        car_list[car_flag].arrivetime[4] = car_list[car_flag].Curr_time
        if car_flag == car_number-1:
            print("All the cars have passed the '10th-14th' traffic system!")
            # return # the end of the simulation
        else:
            car_flag += 1
            waiting_for_light(car_flag)
    else:
        already_pass_cars[car_list[car_flag].Curr_traffic_light - 1] += 1
        car_list[car_flag].arrivetime[car_list[car_flag].Curr_traffic_light-1] = car_list[car_flag].Curr_time
        car_list[car_flag].Event = "running_on_road"
        running_on_road(car_flag)


def running_on_road(car_flag):
    if car_list[car_flag].Event != "running_on_road":
        print("Unexpected Event happen!")
    car_list[car_flag].Curr_time += constant_to_pass[car_list[car_flag].Curr_traffic_light]
    car_list[car_flag].Event = "waiting_for_light"
    waiting_for_light(car_flag)


def how_many_cars_pass(road_index, onetime, car_flag):
    count = 0
    if onetime >= car_list[i-1].arrivetime[road_index]:
        count = car_list[car_flag].Index - 1
    return count


def waiting_for_light(car_flag):
    if car_list[car_flag].Event != "waiting_for_light":
        print("Unexpected Event happen!")
    if out_or_not() is True:
        if car_list[car_flag].Curr_traffic_light != 5:
            if car_flag < car_list[car_flag].cap-1:
                car_list[car_flag].valid= 0
                car_flag += 1
                car_list[car_flag].Event = "waiting_for_light"
                waiting_for_light(car_flag)
    else:
        if red_or_green(car_list[car_flag].Curr_time):
            if how_many_cars_pass(car_list[car_flag].Curr_traffic_light, car_list[car_flag].Curr_time, car_flag) == car_list[car_flag].Index - 1:
                car_list[car_flag].Curr_time += Through_light_time
                car_list[car_flag].Curr_traffic_light += 1
                car_list[car_flag].Event = "arrive"
                arrive(car_flag)
            else:
                car_list[car_flag].Curr_time += Through_light_time
                waiting_for_light(car_flag)
        # Easiest condition
        else:
            if car_list[car_flag].Index == 1:
                car_list[car_flag].Curr_time += to_green_time(car_list[car_flag].Curr_time)
                car_list[car_flag].Curr_time += Through_light_time
                car_list[car_flag].Curr_traffic_light += 1
                car_list[car_flag].Event = "arrive"
                arrive(car_flag)
                # no car ahead of the first car, so we can ignore it, just wait for the green light
            else:
                car_list[car_flag].Curr_time += to_green_time(car_list[car_flag].Curr_time)
                car_list[car_flag].Event = "waiting_for_light"
                waiting_for_light(car_flag)
    '''if the traffic light ahead of this car is green,
    we should only scan the number of cars ahead of this car to decide how long will it take to wait

    '''


if __name__ == '__main__':
    '''
    Initialization of the traffic simulation system
    '''
    print("********************************************************")
    print("********Welcome to the Traffic Simulation System********")
    print("********************************************************")
    car_flag = 0
    already_pass_cars = [0, 0, 0, 0, 0]
    # The cars already pass the nth street
    curr_car_in_different_path = [0, 0, 0, 0, 0]
    # The car numbers on the (n+10)th road
    constant_to_pass = [0, 30, 45, 50, 40]
    '''
    We suppose that every car travel in the same speed, which means they spend the same time to travel each region;
    We do not have affairs like "Overtake" here
    '''
    Through_light_time = 0.7
    red_duration = 25
    green_duration = 15
    # the constant value to get the timing of the Traffic_light
    '''we consider that all the traffic light is at the begining of the red mode when '''
    car_max_number = int(input("Please input the car number range you would like to simulate:"))
    car_running_time = []
    for car_number in range(1,car_max_number):
        car_list = []
        for i in range(car_number):
            car_list.append(Car(0, i+1, 0, [0]*5, "None", 0, car_number, 1))
    # print(car_list[0].processing_for_certain_path)
        temp = []
        for i in range(car_number):
            #car_list[i].Curr_time = random_arrival_time(car_number)[i]
            if i == 0:
                car_list[i].Curr_time = 0
            else:
                tempv = np.random.poisson(lam=2.18, size=1)
                car_list[i].Curr_time = car_list[i - 1].Curr_time + int(tempv)
            temp.append(car_list[i].Curr_time)
        # car_list[i].Curr_time = arrive_time[i]
            car_list[i].Event = "waiting_for_light"
    # Simulation process

        waiting_for_light(0)
    # Final Output
    # average_time = 0
    # print("***********Final Simulation Result:**********")
    # print("The average running time is "+str(average_time)+";When the car number is "+ str(car_number)+'.')

        '''def print_trace(case, car_number):
            if case > car_number:
                print("Please input a right car_index")
            case = int(input("Please input the car trace you want to know (based on the time of the first car arrived):"))
            print(case, car_number)
            else:
            print(car_list[case-1].arrivetime)
        trace_number = int(input("Please input the car trace you want to know (based on the time of the first car arrived):"))
        print_trace(trace_number, car_number)'''
        Process_time = []
        '''for i in range(car_number):
            car_list[i].Processtime = car_list[i].arrivetime[4] - temp[i]
            Process_time.append(car_list[i].Processtime)
    # print(Process_time)'''

        validnumber = 0
        for i in range(car_number):
            car_list[i].Processtime = car_list[i].arrivetime[4] - temp[i]
            if car_list[i].valid == 1:
                Process_time.append(car_list[i].Processtime)
                validnumber += 1

        # print(Process_time)
        if validnumber == 0:
            car_running_time.append(car_running_time[-1])
        if validnumber != 0:
            print("The average running of this traffic system is " + str(sum(Process_time) / validnumber) + " seconds.")
            car_running_time.append(sum(Process_time) / validnumber)

    x = []
    for i in range(car_max_number-1):
        x.append(i+1)
    '''for i in range(len(car_running_time)-30):
        for j in range(29):
            car_running_time[i] += car_running_time[i+j]
        car_running_time[i] /= 30'''
'''
    plt.plot(x, car_running_time)
    plt.title('The average travel time when the car number changes')
    plt.ylim(20,300)
    plt.xlabel('Car number')
    plt.ylabel('average travel time(s)')
    plt.show()'''

















