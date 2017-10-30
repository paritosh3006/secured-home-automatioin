#!/usr/bin/python
import Tkinter
import sys
import Adafruit_DHT
import RPi.GPIO as io
import time
import smtplib
from Tkinter import *
from w1thermsensor import W1ThermSensor

io.setmode(io.BOARD)
io.setwarnings(False)

io.setup(12,io.OUT)
io.setup(13,io.OUT)
io.setup(38,io.OUT)
io.setup(40,io.OUT)

io.setup(3,io.IN)   #humidity
io.setup(7,io.IN)   #temperature
io.setup(5,io.IN)   #Reed
io.setup(10,io.IN)  #PIR
io.setup(8,io.IN)   #LPG

io.output(38,0)
io.output(40,0)

l=io.PWM(12,255)
s=io.PWM(13,255)

l.start(0)
s.start(0)
a,b,c,d=0,0,0,0
val1,val2,val3,val4=0,0,0,0

def hum():
    global humi
    global val4
    humidity,temperature=Adafruit_DHT.read_retry(11,2)
    Label(text=('Humidity: %'+str(humidity)),fg="white",bg="red",font=30).grid(row=8,column=6)
    print 'humidity % :' + str(humidity)
    val4=1
    humi=('humidity % :' + str(humidity))
def readtempa():
    global temp1
    sensor = W1ThermSensor()
    temperature_in_celsius = sensor.get_temperature()
    print "Temperature: "+ str(temperature_in_celsius)
    Label(text=('Temperature: '+str(temperature_in_celsius)),fg="white",bg="red",font=30).grid(row=10,column=6)
    temp1=('Temperature: '+str(temperature_in_celsius))
def value():
    global val1
    global val2
    global val3
    global val4
    value=io.input(5)
    hum()
    readtempa()
    if value == 1:
        Label(text=('Gate Opened'),fg="white",bg="green",font=30).grid(row=2,column=6)
        val1=1
    else:
        Label(text='Gate Closed',fg="white",bg="red",font=30).grid(row=2,column=6)
        val1=0
    value=io.input(8)
    if value == 1:
        Label(text='Leakage detected',fg="white",bg="red",font=30).grid(row=4,column=6)
        val2=1
    else:
        Label(text='    No leakage    ',fg="white",bg="green",font=30).grid(row=4,column=6)
        val2=0
    value=io.input(10)
    if value == 1:
        Label(text='Motion Detected',fg="white",bg="red",font=30).grid(row=6,column=6)
        val3=1
    else:
        Label(text='     No Motion     ',fg="white",bg="green",font=30).grid(row=6,column=6)
        val3=0

def mail():
    server=smtplib.SMTP('smtp.gmail.com',587)
    print "starting server"
    server.starttls()
    server.login("paritoshkr30@gmail.com","30june1995paritosh")
    print "login"
    subject = 'parameters'
    if a==0:
        light_msg = 'Lights off'
    if a==1:
        light_msg = 'Lights on'
    if a==2:
        light_msg = 'Lights off'
    if b==0:
        fan_msg = 'Fans off'
    if b==1:
        fan_msg = 'Fans on'
    if b==2:
        fan_msg = 'Fans off'
    if d==0:
        intens = 'Lights off'
    if d==1:
        intens = 'Lights off'
    if d==2:
        intens = 'Lights level 1'
    if d==3:
        intens = 'Lights level 2'
    if d==4:
        intens = 'Lights level 3'
    if d==5:
        intens = 'Lights level 4'
    if c==0:
        speed = 'fans off'
    if c==1:
        speed = 'fans off'
    if c==2:
        speed = 'fans level 1'
    if c==3:
        speed = 'fans level 2'
    if c==4:
        speed = 'fans level 3'
    if c==5:
        speed = 'fans level 4'
    if val1==1:
        sensor1 = 'Gate Open'
    if val1==0:
        sensor1 = 'Gate closed'
    if val2==1:
        sensor2 = '***LPG Leaking***'
    if val2==0:
        sensor2 = 'No LPG Leakage'
    if val3==1:
        sensor3 = 'Motion detected'
    if val3==0:
        sensor3 = 'No motion detected'
    sensor4 = humi
    sensor5 = temp1
    msg = 'Subject:{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}'.format(subject,light_msg,fan_msg,intens,speed,sensor1,sensor2,sensor3,sensor4,sensor5)
    server.sendmail("paritoshkr30@gmail.com","kaushikashutosh21@gmail.com",msg)
    server.quit()
    print "mail sent"

def light_on():
    global a
    io.output(38,1)
    a=1
    print "lights on"
    
def light_off():
    global a
    io.output(38,0)
    a=2
    print "Lights off"
    
def fan_on():
    global b
    io.output(40,1)
    b=1
    print "Fan on"
    
def fan_off():
    global b
    io.output(40,0)
    b=0
    print "Fan off"
    
def l1():
    global d
    l.ChangeDutyCycle(0)
    d=1
    print "Light Intensity Level 1"
    time.sleep(0.01)

def l2():
    global d
    l.ChangeDutyCycle(30)
    d=2
    print "Light Intensity Level 2"
    time.sleep(0.01)

def l3():
    global d
    l.ChangeDutyCycle(55)
    d=3
    print "Light Intensity Level 3"
    time.sleep(0.01)

def l4():
    global d
    l.ChangeDutyCycle(80)
    d=4
    print "Light Intensity Level 4"
    time.sleep(0.01)

def l5():
    global d
    l.ChangeDutyCycle(100)
    d=5
    print "Light Intensity Level 5"
    time.sleep(0.01)

def s1():
    global c
    s.ChangeDutyCycle(0)
    c=1
    print "Fan Speed level 1"
    time.sleep(0.01)

def s2():
    global c
    s.ChangeDutyCycle(30)
    c=2
    print "Fan Speed level 2"
    time.sleep(0.01)
    
def s3():
    global c
    s.ChangeDutyCycle(55)
    c=3
    print "Fan Speed level 3"
    time.sleep(0.01)

def s4():
    global c
    s.ChangeDutyCycle(80)
    c=4
    print "Fan Speed level 4"
    time.sleep(0.01)

def s5():
    global c
    s.ChangeDutyCycle(100)
    c=5
    print "Fan Speed level 5"
    time.sleep(0.01)

def q():
    exit()

root = Tk()
root.grid()
v = IntVar()
w = IntVar()
x = IntVar()
y = IntVar()
z = IntVar()
root.geometry('500x250+400+200')
root.title('Secured home automation')

##############         LIGHT        ########################
Head=Label(text='Lights',fg='black').grid(row=0,column=0)
button = Radiobutton(root, text = "On",variable =v, value=1,command=light_on)
button.grid(row = 0, column = 2, sticky = W)
button = Radiobutton(root, text = "Off", variable=v, value=2,command=light_off)
button.grid(row = 0, column = 4, sticky = W)

##############          FAN          ######################
Head=Label(text='Fan',fg='black').grid(row=2,column=0)
button = Radiobutton(root, text = "On", variable=w, value=1,command=fan_on)
button.grid(row = 2, column = 2, sticky = W)
button = Radiobutton(root, text = "Off", variable=w, value=2,command=fan_off)
button.grid(row = 2, column = 4, sticky = W)

##############         INTENSITY     ###########################
Label(root,text="Intensity",fg="black",bg="white").grid(row=4, column=0)
button = Radiobutton(root, text = "off",variable =x, value=1,command=l1)
button.grid(row = 4, column = 1, sticky = W)
button = Radiobutton(root, text = "1",variable =x, value=2,command=l2)
button.grid(row = 4, column = 2, sticky = W)
button = Radiobutton(root, text = "2",variable =x, value=3,command=l3)
button.grid(row = 4, column = 3, sticky = W)
button = Radiobutton(root, text = "3",variable =x, value=4,command=l4)
button.grid(row = 4, column = 4, sticky = W)
button = Radiobutton(root, text = "4",variable =x, value=5,command=l5)
button.grid(row = 4, column = 5, sticky = W)

##############           SPEED       ###########################
Label(root,text="Speed",fg="black",bg="white").grid(row=6, column=0)
button = Radiobutton(root, text = "off",variable =y, value=1,command=s1)
button.grid(row = 6, column = 1, sticky = W)
button = Radiobutton(root, text = "1",variable =y, value=2,command=s2)
button.grid(row = 6, column = 2, sticky = W)
button = Radiobutton(root, text = "2",variable =y, value=3,command=s3)
button.grid(row = 6, column = 3, sticky = W)
button = Radiobutton(root, text = "3",variable =y, value=4,command=s4)
button.grid(row = 6, column = 4, sticky = W)
button = Radiobutton(root, text = "4",variable =y, value=5,command=s5)
button.grid(row = 6, column = 5, sticky = W)

##############          Sensor      ################################
Temp=Button(text="Sensor Status",bd=3,activebackground='orange',activeforeground='blue',fg="red",bg="white",font=40,command=value).grid(row=0,column=6)
Label(text='PIR',fg="white",bg="black",font=30).grid(row=2,column=6)
Label(text='LPG',fg="white",bg="black",font=30).grid(row=4,column=6)
Label(text='Fire',fg="white",bg="black",font=30).grid(row=6,column=6)
Label(text='Humidity',fg="white",bg="black",font=30).grid(row=8,column=6)
Label(text='Temperature',fg="white",bg="black",font=30).grid(row=10,column=6)

######################################################################
Temp=Button(text="MAIL",activebackground='blue',bd=2, activeforeground='white',fg="green",bg="white",font=40,command=mail).grid(row=12,column=5)
Temp=Button(text="Quit",activebackground='red',bd=4, activeforeground='yellow',fg="blue",bg="white",font=40,command=q).grid(row=14,column=5)	

root.mainloop()
