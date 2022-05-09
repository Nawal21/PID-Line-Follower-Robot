from controller import Robot

robot = Robot()
timestep = 32

ds=[]
wheel =[]
wheel_name =["wheel1","wheel2","wheel3","wheel4"]
ds_name=["ds_middle","ds_right","ds_left"]
ds_val = [0]*len(ds_name)
for i in ds_name:
    ds.append(robot.getDevice(i))
    ds[-1].enable(timestep)
for i in wheel_name:
    wheel.append(robot.getDevice(i))
    wheel[-1].setPosition(float("inf"))
    wheel[-1].setVelocity(0.0)

last_error = intg = prop = diff = 0
Kp = 0.12
Ki = 0
Kd = 0.01
def pid(error):
    global last_error, intg, prop ,diff, Kp,Kd,Ki
    prop = error
    intg = error  + intg 
    diff = error  - last_error
    balance = (Kp*prop) + (Kd*diff) + (Ki*intg)
    last_error = error
    return balance
    
def setSpeed(base_speed,balance):
    
    wheel[0].setVelocity(base_speed+balance)
    wheel[1].setVelocity(base_speed-balance)
    wheel[2].setVelocity(base_speed+balance)
    wheel[3].setVelocity(base_speed-balance)
    

while robot.step(timestep) != -1:
    
    for i in range(len(ds)):
        ds_val[i] = ds[i].getValue()
        print(f"{ds_name[i]}:{ds_val[i]}\n")
            
    if ds_val[0]>950  and ds_val[1]<950 and ds_val[2]<950:
        error = 0
        rectify = pid(error)
        setSpeed(5,rectify)
        print("case 0")
    elif ds_val[0]>950  and ds_val[1]>950 and ds_val[2]<950:
        error = ds_val[1] - 900
        rectify = pid(error)
        setSpeed(5,-rectify)
        print("case 1")    
    elif ds_val[0]>950 and ds_val[1]<950 and ds_val[2]>950:
        error = ds_val[2] - 900
        rectify = pid(error)
        setSpeed(5,rectify)
        print("case 2")
    elif ds_val[0]<950  and ds_val[1]>950 and ds_val[2]<950:
        error = ds_val[1] - 900
        rectify = pid(error)
        setSpeed(5,-rectify)    
        print("case 3")
    elif ds_val[0]<950 and ds_val[1]<950 and ds_val[2]>950:
        error = ds_val[2] - 900
        rectify = pid(error)
        setSpeed(5,rectify)
        print("case 4")
    elif ds_val[0]>950 and ds_val[1]>950 and ds_val[2]>950:
        print("case 5")   
    
    pass


 

        