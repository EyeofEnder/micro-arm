import microbit  # Write your code here :-)

i2c = microbit.i2c

#microbit.i2c.init(scl=19, sda=20)

active = 1

set_pins = {1:microbit.pin12,2:microbit.pin13,3:microbit.pin14,4:microbit.pin15}

reg_addr = {"power":0x6b,"fs_sel":0x1b,"afs_sel":0x1c,"gxh":0x43,"gxl":0x44,"gyh":0x45,"gyl":0x46,"gzh":0x47,"gzl":0x48,"fifo":0x23,"axh":0x3b,"axl":0x3c,"ayh":0x3d,"ayl":0x3e,"azh":0x3f,"azl":0x40}

dev_addr = 0x68

vals = [[0,0,0] for i in range(0,4)]

cal = [[0,0,0] for i in range(0,4)]

ori = [[0,0,0] for i in range(0,4)]

last_avg = 0

timer = microbit.running_time()

def set_active(sens=1):
    
    global active,set_pins
    
    for pin in set_pins.keys:
        
        if pin != sens:
            
            set_pins[pin].write_digital(0)
            
        else:
            
            set_pins[pin].write_digital(1)
            
    active = sens

def to_bytes(x):

    return bytearray(x.to_bytes(1,"big"))
    
def read_addr(dev_addr,reg,byte_n=1):
    
    global reg_addr
    
    i2c.write(dev_addr,to_bytes(reg_addr[reg]),False)
    
    return bytearray(i2c.read(dev_addr,byte_n,True))
    
def write_addr(dev_addr,reg,w):
    
    global reg_addr
    
    msg = to_bytes(reg_addr[reg])+to_bytes(w)
    
    i2c.write(dev_addr,msg,True)

def read_gyro(d_addr,reg="gx",sens=65.5):
        
    g = "{:0>8b}".format(int.from_bytes(read_addr(d_addr,reg+"h"),"big")) + "{:0>8b}".format(int.from_bytes(read_addr(d_addr,reg+"l"),"big"))

    g = eval("0b"+g)
    
    if "{:0>16b}".format(g)[0] == "1":
            
        g = 0b1111111111111111 - g
            
        g = -(g + 1)
        
    return g/sens
    
def calibrate(cycles=5):
    
    global cal
    
    cal = [[0,0,0] for i in range(0,4)]
    
    for n in range(0,cycles):
        
        cal[0][0] += read_gyro(dev_addr,"gx")
        
        cal[0][1] += read_gyro(dev_addr,"gy")
        
        cal[0][2] += read_gyro(dev_addr,"gz")
    
        microbit.sleep(50)
        
    for n in cal:
        
        n = map(lambda x: x/cycles,n)
    
    print(cal)
    
def reset():
    
    global vals,ori,last_avg
    
    calibrate()
    
    last_avg = 0
    
    vals = [[0,0,0] for i in range(0,4)]
    
    ori = [[0,0,0] for i in range(0,4)]
    
def read_sensor():
    
    gy = [read_gyro(dev_addr,"gx"),read_gyro(dev_addr,"gy"),read_gyro(dev_addr,"gz")]
    
    ac = [read_gyro(dev_addr,"ax",sens=4096),read_gyro(dev_addr,"ay",sens=4096),read_gyro(dev_addr,"az",sens=4096)]
    
    return gy, ac

def gyro():
    
    global vals, cal, last_avg,timer,ori,active

    while True:
        
        last_avg += 1
        
        vals[active] = [v+s for v,s in zip(vals[active],read_sensor()[0])]
                
        if last_avg == 2:
            
            t = microbit.running_time()
            
            time_diff = t - timer
            
            timer = t
            
            for i in (0,1,2,3):
                
                for a in (0,1,2):
                    
                    ori[i][a] += round(time_diff/1000*round((vals[i][a]/last_avg)-cal[i][a]),1)
                    
                    #print(vals,time_diff)
                    
                    print(ori)
            
            vals = [[0,0,0] for n in range(0,4)]
            
            last_avg = 0
            
        microbit.sleep(20)
        
print(microbit.i2c.scan())

write_addr(dev_addr,"power",0b00000000)

write_addr(dev_addr,"fs_sel",0b00001000)

write_addr(dev_addr,"fs_sel",0b00010000)

reset()
        
gyro()
