import random
import math
import numpy



class Car:
	def __init__(self, arrival_time, number, speed, start_time, exit_cross):
		self.arrival = arrival_time
		self.number = number
		self.speed = speed  # feet/s
		self.start_up_time = start_time  # s
		self.exit_cross = exit_cross


class Cross:
	def __init__(self, n, l):
		self.name = n
		self.length = l


class Road:
	def __init__(self, n, l):
		self.name = n
		self.length = l


# at the very begining when the car entering the peachstreet


class Activity_EnterRoad:
	def __init__(self, car, road):
		self.car = car
		self.end_time = car.arrival


class Activity_OnTheRoad:
	def __init__(self, activity, road):  # feet
		self.car = activity.car
		self.start_time = activity.end_time
		self.end_time = math.floor(10*(self.start_time + road.length / activity.car.speed))/10  # sec


class Activity_EnterCross:
	def __init__(self, activity, cross):
		self.car = activity.car
		self.start_time = activity.end_time


# class Activity_OnTheCross:
class Activity_OnTheCross:
	def __init__(self, activity_EnterCross, cross, t):
		self.car = activity_EnterCross.car
		self.start_time = t
		self.end_time = math.floor(10*(self.start_time + cross_passing_time(self.car, cross)))/10  # sec


# generate random car arrival time
def generate_arrival_list(m,l):  #ms
	time_list = [0]
	inter_arrival_list = numpy.random.poisson(l, m)/10  # sec
	for i in range(m - 1):
		time_list.append(time_list[i] + inter_arrival_list[i])
	return time_list


# generate random average speed of a car
def generate_speed_list(m):
	speed_list = []
	for i in range(m):
		speed_list.append(0.1 * random.randrange(300, 500, 1))  # feet per sec
	return speed_list


# generate random start_up time of a car
def generate_start_time_list(m):
	start_list = []
	for i in range(m):
		start_list.append(random.randrange(10, 30, 1))  # ms
	return start_list


# assume the traffic light red=20s green=15s ,initial state is red
def light_is_green(t, red_time):
	t_red = red_time+30
	t_green = 30
	t_total = t_red + t_green
	re = t % t_total
	if t_red > re >= 0:
		return True
	else:
		return False


# compute the time for a Car to pass the Cross
def cross_passing_time(car, cross):
	return car.start_up_time + cross.length / car.speed


def generate_exit_cross_list(m):
	exit_list=[]
	for i in range(m):
		x=random.uniform(0, 10)
		if 0<=x<0.5:
			exit_list.append(1)
		elif 0.5<=x<1:
			exit_list.append(2)
		elif 1<=x<1.5:
			exit_list.append(3)
		elif 1.5<=x<2:
			exit_list.append(4)
		else:
			exit_list.append(5)
	return exit_list
x_axis = []
y_axis = []
max_time = 2000 # sec
m = 500
# main
road_1 = Road("1st peach street", 127.391)
road_2 = Road("2nd peach street", 441.437)
road_3 = Road("3rd peach street", 412.070)
road_4 = Road("4th peach street", 353.727)
road_5 = Road("5th peach street", 343.922)
road_6 = Road("6th peach street", 11.730)

cross_1 = Cross("10th", 99.645)
cross_2 = Cross("11th", 129.795)
cross_3 = Cross("12th", 73.815)
cross_4 = Cross("13th", 66.979)
cross_5 = Cross("14th", 117.411)

arrival_list = generate_arrival_list(m, 21.8)
speed_list = generate_speed_list(m)
start_time_list = generate_start_time_list(m)
exit_cross_list = generate_exit_cross_list(m)

road_1_list = []
road_2_list = []
road_3_list = []
road_4_list = []
road_5_list = []
road_6_list = []

cross_1_queue = []
cross_11_queue = []
cross_2_queue = []
cross_22_queue = []
cross_3_queue = []
cross_33_queue = []
cross_4_queue = []
cross_44_queue = []
cross_5_queue = []
cross_55_queue = []

red_light=0
t = 0.0
k = 0
kk=0
Sum = 0
average = 0
while t < max_time:

	if k < m and arrival_list[k] - 0.5 <= t < arrival_list[k] + 0.5:
		car = Car(arrival_list[k], k, speed_list[k], start_time_list[k], exit_cross_list[k])

# Road 1----------
		C = Activity_EnterRoad(car, road_1)
		B = Activity_OnTheRoad(C, road_1)
		road_1_list.append(B)
		k = k + 1

# Cross 1------------

	j = 0
	while j < len(road_1_list):
		if road_1_list[j].end_time - 0.5 <= t < road_1_list[j].end_time + 0.5:

			cross_1_queue.append(Activity_EnterCross(road_1_list.pop(j), cross_1))
			j = j-1
		j = j+1


	if len(cross_1_queue) != 0:
		if light_is_green(t, red_light):

			cross_11_queue.append(Activity_OnTheCross(cross_1_queue.pop(0), cross_1, t+2*len(cross_1_queue)))

	# Road 2-----------------------------
	if len(cross_11_queue) != 0:
		i = 0
		while i < len(cross_11_queue):

			if cross_11_queue[i].end_time - 0.5 <= t < cross_11_queue[i].end_time + 0.5:
				C = Activity_OnTheRoad(cross_11_queue.pop(i), road_2)
				if C.car.exit_cross != 1:
					road_2_list.append(C)
				i = i - 1
			i = i + 1


	# Cross 2------------

	j = 0
	while j < len(road_2_list):
		if road_2_list[j].end_time - 0.5 <= t < road_2_list[j].end_time + 0.5:

			cross_2_queue.append(Activity_EnterCross(road_2_list.pop(j), cross_2))
			j = j-1
		j = j+1


	if len(cross_2_queue) != 0:
		if light_is_green(t, red_light):

			cross_22_queue.append(Activity_OnTheCross(cross_2_queue.pop(0), cross_2, t+2*len(cross_2_queue)))

	# Road3-----------------------------
	if len(cross_22_queue) != 0:
		i = 0
		while i < len(cross_22_queue):

			if cross_22_queue[i].end_time - 0.5 <= t < cross_22_queue[i].end_time + 0.5:
				C = Activity_OnTheRoad(cross_22_queue.pop(i), road_3)
				if C.car.exit_cross != 2:
					road_3_list.append(C)
				i = i - 1
			i = i + 1

	# Cross 3------------


	j = 0
	while j < len(road_3_list):
		if road_3_list[j].end_time - 0.5 <= t < road_3_list[j].end_time + 0.5:

			cross_3_queue.append(Activity_EnterCross(road_3_list.pop(j), cross_3))
			j = j-1
		j = j+1


	if len(cross_3_queue) != 0:
		if light_is_green(t,red_light):

			cross_33_queue.append(Activity_OnTheCross(cross_3_queue.pop(0), cross_3, t+2*len(cross_3_queue)))

	# Road 4-----------------------------
	if len(cross_33_queue) != 0:
		i = 0
		while i < len(cross_33_queue):

			if cross_33_queue[i].end_time - 0.5 <= t < cross_33_queue[i].end_time + 0.5:
				C = Activity_OnTheRoad(cross_33_queue.pop(i), road_4)
				if C.car.exit_cross != 3:
					road_4_list.append(C)
				i = i - 1
			i = i + 1

	# Cross 4------------

	j = 0
	while j < len(road_4_list):
		if road_4_list[j].end_time - 0.5 <= t < road_4_list[j].end_time + 0.5:

			cross_4_queue.append(Activity_EnterCross(road_4_list.pop(j), cross_4))
			j = j-1
		j = j+1



	if len(cross_4_queue) != 0:
		if light_is_green(t,red_light):

			cross_44_queue.append(Activity_OnTheCross(cross_4_queue.pop(0), cross_4, t+2*len(cross_4_queue)))

	# Road 5-----------------------------
	if len(cross_44_queue) != 0:
		i = 0
		while i < len(cross_44_queue):

			if cross_44_queue[i].end_time - 0.5 <= t < cross_44_queue[i].end_time + 0.5:
				C = Activity_OnTheRoad(cross_44_queue.pop(i), road_5)
				if C.car.exit_cross != 4:
					road_5_list.append(C)
				i = i - 1
			i = i + 1
	# Cross 5------------


	j = 0
	while j < len(road_5_list):
		if road_5_list[j].end_time - 0.5 <= t < road_5_list[j].end_time + 0.5:

			cross_5_queue.append(Activity_EnterCross(road_5_list.pop(j), cross_5))
			j = j-1
		j = j+1


	if len(cross_5_queue) != 0:
		if light_is_green(t,red_light):
			cross_55_queue.append(Activity_OnTheCross(cross_5_queue.pop(0), cross_5, t+2*len(cross_5_queue)))
	# Road 6-----------------------------
	if len(cross_55_queue) != 0:
		i = 0
		while i < len(cross_55_queue):
			if cross_55_queue[i].end_time - 0.5 <= t < cross_55_queue[i].end_time + 0.5:
				C = Activity_OnTheRoad(cross_55_queue.pop(i), road_6)
				road_6_list.append(C)
				i = i - 1
			i = i + 1
	t = t + 1

Sum = 0
for i in range(len(road_6_list)):
	Sum = Sum + road_6_list[i].end_time - road_6_list[i].car.arrival
kk = len(road_6_list)
average = Sum / kk
print('number of cars=',m , 'average passing time=', average/ 60, 'min')


