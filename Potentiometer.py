import microbit

microbit.display.off()

microbit.pin0.write_digital(0)

microbit.pin1.write_digital(0)

microbit.pin2.write_digital(0)

microbit.pin6.write_digital(0)

microbit.pin7.write_digital(0)

microbit.pin8.write_digital(0)

# Pins: 1 = Grabbing, 2 = Wrist elevation, 3 = Elbow

pot_range = 270 # potentiometer angle limits

sens_1 = microbit.pin0

sens_2 = microbit.pin1

sens_3 = microbit.pin2

servo_1 = microbit.pin6

servo_2 = microbit.pin7

servo_3 = microbit.pin8

servo_1.set_analog_period(20)
servo_2.set_analog_period(20)
servo_3.set_analog_period(20)

angle_limit_1 =90

angle_limit_2 = 90

angle_limit_3 = 150

range_1 = 180

range_2 = 135

# microbit.pin8.write_digital(1)

def read_pots():
    
    global pot_1,pot_2,pot_3,sens_1,sens_2,sens_3
    
    pot_1 = (sens_1.read_analog()/1024)

    pot_2 = (sens_2.read_analog()/1024)

    pot_3 = (sens_3.read_analog()/1024)

def servo(servo,angle,pwm_lim = (1,2)):
    
    if angle >= 0 and angle <= 180: 
        
        mult = 1023 * (1/20)
    
        angle = (pwm_lim[0] + (pwm_lim[1]-pwm_lim[0]) * (angle/180)) * mult
        
        servo.write_analog(angle)
    
    else:
        
        pass
    
while True:
    
    read_pots()
    
    microbit.sleep(40)
        
    servo(servo_1,(180*(1-(1-pot_1)*(pot_range/angle_limit_1))),(0.5,2.4))
    
    servo(servo_2,(180*(1-(1-pot_2)*(pot_range/angle_limit_2))),(0.5,2.4))
    
    servo(servo_3,(pot_range-(pot_3*(pot_range)-20)))
