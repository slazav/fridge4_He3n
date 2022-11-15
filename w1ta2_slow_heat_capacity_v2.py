import sys

from matplotlib import pyplot as plt

sys.path.insert(0, '/Users/tinekesalmon/Documents/exp_py/graphene')

import numpy as np

# import graphene
import graphene
graphene.set_args(['ssh', 'f4a', 'device_c', 'ask', 'db'])
graphene.set_cache('.graphene')

#load a text file of times. t1 column 0, t2 column 1.
times=np.loadtxt("/Users/tinekesalmon/Documents/fridge4_He3n/times.txt")

#open some empty lists
heat_capacity=[]
heat_leak=[]
average_temperature=[]
time_1=[]
time_2=[]

#define time_set function
def time_set(t1, t2):
    # set temp and volt to be 30 mins before t1 and 30 mins after t2
    temp=graphene.get_range('w1ta2:f1', t1-30*60, t2+30*60)
    volt=graphene.get_range('volt_h1', t1-30*60, t2+30*60)
    #set t0 as inital time
    t0= temp[0][0]

    # Find indices correlating to the point closest to the time at which the heating starts, t1, 
    # and the time at which the heating finishes, t2. 
    # Take the absolute difference of time points - t1 and time points - t2
    # set loop over times:
    difference_t1=[]
    difference_t2=[]
    for index in temp[0]:
        diff_t1=abs(index - t1)
        difference_t1.append(diff_t1)
        diff_t2=abs(index -t2)
        difference_t2.append(diff_t2)

    # Use argmin function to find the index of the minimum difference. 
    # This will be the index of the point closest to the time, t1 or t2. 
    break1=np.argmin(difference_t1)+1
    break2=np.argmin(difference_t2)+1

    #break up the time into 3 parts and subtract initial time to start graph at zero
    time_initial=temp[0][0:break1]-t0
    time_centre=temp[0][break1:break2]-t0
    time_end=temp[0][break2:]-t0
    #break up the temp into 3 parts
    temp_inital=temp[1][0:break1]
    temp_centre=temp[1][break1:break2]
    temp_end=temp[1][break2:]
    
    # plot figure 1
    plt.figure(1)
    plt.clf()
    # polynomial fit of x against y (temp values), 1st order polynomial
    z_initial=np.polyfit(time_initial, temp_inital, 1)
    p_initial = np.poly1d(z_initial)
    print("p_initial =",p_initial)
    # # finds the gradient from the polynomial fit output 
    # print("Grad_initial =", p_initial[1])
    # creates a linspace suitable for the length of the displayed fit line
    xp_initial= np.linspace(0, temp[0][break1]-t0 + 200, 100)
    
    # centre part 
    z_centre=np.polyfit(time_centre, temp_centre, 1)
    p_centre = np.poly1d(z_centre)
    print("p_centre =",p_centre)
    # # finds the gradient from the polynomial fit output 
    # print("Grad_centre =", p_centre[1])
    # creates a linspace suitable for the length of the displayed fit line
    xp_centre = np.linspace(temp[0][break1]-t0 -100, temp[0][break2]-t0 +200, 100)

    # end part 
    z_end=np.polyfit(time_end, temp_end, 1)
    p_end = np.poly1d(z_end)
    print("p_end =",p_end)
    # # finds the gradient from the polynomial fit output 
    # print("Grad_end =", p_end[1])
    # creates a linspace suitable for the length of the displayed fit line
    xp_end = np.linspace(temp[0][break2]-t0 -100, temp[0][-1]-t0+100, 100)
    
    #plot
    plt.plot(temp[0]-t0, temp[1], '.', xp_initial, p_initial(xp_initial), xp_centre, p_centre(xp_centre), xp_end, p_end(xp_end))
    plt.title("w1ta at %d" %(t1))
    plt.xlabel("Time (s)")
    plt.ylabel("Temperature")
    plt.savefig('/Users/tinekesalmon/Documents/fridge4_He3n/heat_capacity_slow_temp_plot%d.png' %(t1))
    
    plt.figure(2)
    plt.clf()
    plt.plot(volt[0]-t0, volt[1], '*-')
    plt.title("w1ta at %d" %(t1))
    plt.xlabel("Time (s)")
    plt.ylabel("Voltage (V)")
    plt.savefig('/Users/tinekesalmon/Documents/fridge4_He3n/heat_capacity_slow_volt_plot%d.png' %(t1))

    #temperature rate (gradients). Temp measured in milliKelvin so *e-3 to convert to K
    # parasitic temperature gradient before heating 
    T_p1=p_initial[1]*1e-3
    # parasitic temperature gradient after heating 
    T_p2=p_end[1]*1e-3
    # average parasitic temperature gradient 
    T_p = (T_p1 + T_p2)/2
    # temperature gradient whilst heating 
    T_h = p_centre[1]*1e-3
    # Voltage applied to heater in Volts
    V = 0.02
    # Resistance of the heater in Ohms
    R = 197.1
    #Temp gradient difference
    T_diff = T_h - T_p
    #Heat capacity in J/K
    c = (V**2)/(R*T_diff)
    #Heat leak in Watts 
    Q_p = c*T_p
    #average temperature 
    T_av = np.mean(temp[1])
    
    #need to save values to an array
    heat_capacity.append(c)
    print('c', heat_capacity)
    heat_leak.append(Q_p)
    print('Q_p', heat_leak)
    average_temperature.append(T_av)
    print('av T', average_temperature)
    time_1.append(t1)
    print('t1', time_1)
    time_2.append(t2)
    print('t2', time_2)

    return heat_capacity, heat_leak, average_temperature, time_1, time_2

for index in range(len(times)):
    t1a=times[index,0]
    t2a=times[index,1]
    heat_capacity, heat_leak, average_temperature, time_1, time_2 =time_set(t1a, t2a)

print('time1',time_1)
print('time2',time_2)
print('av temp',average_temperature)
print('c',heat_capacity)
print('q_p',heat_leak)

# #slow heating. starts 2022-10-20 12:18:35 ends 2022-10-20 12:31:33
# #convert time to unix 
# import datetime
# import time
# date_time = datetime.datetime(2022, 10, 20, 12, 18, 35)
# print("Given Date:",date_time)
# print("UNIX timestamp:",
# (time.mktime(date_time.timetuple())))
# t1a=time.mktime(date_time.timetuple())
# print(t1a)

# date_time = datetime.datetime(2022, 10, 20, 12, 31, 33)
# print("Given Date:",date_time)
# print("UNIX timestamp:",
# (time.mktime(date_time.timetuple())))
# t2a=time.mktime(date_time.timetuple())