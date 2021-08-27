import socket
import numpy as np
import pandas as pd
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
sns.set_theme(style="darkgrid")
np_array=np.zeros((1, 4),str)
np_array = np.delete(np_array, (0), axis=0)

temp_array=np.zeros((1,), float)
temp_array = np.delete(temp_array, (0), axis=0)
hum_array=np.zeros((1,), float)
hum_array = np.delete(hum_array, (0), axis=0)
lux_array=np.zeros((1,), float)
lux_array = np.delete(lux_array, (0), axis=0)
time_array=np.zeros((1), str)
time_array = np.delete(time_array, (0), axis=0)
UDP_IP = "192.168.0.18"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))


while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    t,h,l=str(data).replace("\'","").replace("b","").split(" ")
    now = datetime.now()
    if((float(t)>=35) or (float(t)<=15) or float(h)<10):
        f = open("alarm.txt", "w")
        f.write("3")
        f.close()
    elif(float(t)>=28 or float(t)<=20 or float(h)<30):
        f = open("alarm.txt", "w")
        f.write("2")
        f.close()
    else:
        f = open("alarm.txt", "w")
        f.write("1")
        f.close()
    current_time = now.strftime("%H:%M:%S")

    temp_array=np.append(temp_array,t)
    hum_array=np.append(hum_array,h)
    lux_array=np.append(lux_array,l)
    time_array=np.append(time_array,str(current_time))
    data_temp=np.vstack([temp_array,time_array])
    data_temp=np.transpose(data_temp)
    #print(data_temp)
    fig,  temp_plot,= plt.subplots()
    fig2,hum_plot=plt.subplots()
    fig3,lux_plot=plt.subplots()


    temp_array = list(map(float, temp_array))
    temp_plot.plot(time_array, temp_array)
    hum_array = list(map(float, hum_array))
    hum_plot.plot(time_array,hum_array)
    lux_array = list(map(float, lux_array))
    lux_plot.plot(time_array,lux_array)

    temp_plot.axhline(y=15, color='r', linestyle='-')
    temp_plot.axhline(y=20, color='y', linestyle='-')
    temp_plot.axhline(y=28, color='y', linestyle='-')
    temp_plot.axhline(y=35, color='r', linestyle='-')
    temp_plot.set_title("temperature plot")
    temp_plot.set_xlabel("time")
    temp_plot.set_ylabel("temp(C)")
    temp_plot.grid(color = 'green', linestyle = '--', linewidth = 0.5)
    temp_plot.xaxis.set_major_locator(plt.MaxNLocator(15))
    fig.autofmt_xdate()
    fig.savefig("static/temp.png")

    plt.show()




    hum_plot.axhline(y=10, color='r', linestyle='-')
    hum_plot.axhline(y=30, color='y', linestyle='-')
    hum_plot.set_title("Humidity plot")
    hum_plot.set_xlabel("time")
    hum_plot.set_ylabel("Hum(%)")
    hum_plot.plot(time_array,hum_array)
    hum_plot.xaxis.set_major_locator(plt.MaxNLocator(15))
    hum_plot.grid(color = 'green', linestyle = '--', linewidth = 0.5)
    fig2.autofmt_xdate()
    fig2.savefig("static/hum.png")

    plt.show()




    lux_plot.set_title("brightness plot")
    lux_plot.set_xlabel("time")
    lux_plot.set_ylabel("brightness")
    lux_plot.grid(color = 'green', linestyle = '--', linewidth = 0.5)
    lux_plot.xaxis.set_major_locator(plt.MaxNLocator(15))
    fig3.autofmt_xdate()
    fig3.savefig("static/lux.png")
    plt.show()

    pd.DataFrame(np_array).to_csv("data.csv")
    print("temp="+t+" hum="+h+" lux="+l+" time="+current_time)
    #temp_plot.figure.savefig("temp.png")
    #hum_plot.figure.savefig("hum.png")
    #lux_plot.figure.savefig("lux.png")