# Speed settings to tune maqueen's smoothness
base_speed = 50        
outer_wheel_speed = 50 
inner_wheel_speed = 20  

last_turn = 0
has_block = False

# Start with the claw open
maqueen.servo_run(maqueen.Servos.S1, 20)

# TWO PHASE SENSOR SPIN 
def turn_until_line():
    # Start the differential spin in place
    maqueen.motor_run(maqueen.Motors.M1, maqueen.Dir.CW, 50)
    maqueen.motor_run(maqueen.Motors.M2, maqueen.Dir.CCW, 50)
    
    # 1: ESCAPE THE BLACK LINE
    # Keep spinning until BOTH sensors see white (1)
    while True:
        l_sensor = maqueen.read_patrol(maqueen.Patrol.PATROL_LEFT)
        r_sensor = maqueen.read_patrol(maqueen.Patrol.PATROL_RIGHT)
        if l_sensor == 1 and r_sensor == 1:
            break # We are in the clear
            
    # 2: FIND THE RETURN LINE
    # Keep spinning until EITHER sensor sees black (0) again
    while True:
        l_sensor = maqueen.read_patrol(maqueen.Patrol.PATROL_LEFT)
        r_sensor = maqueen.read_patrol(maqueen.Patrol.PATROL_RIGHT)
        if l_sensor == 0 or r_sensor == 0:
            break # Found the line!
            
    # Stop motors so the main line-following logic can take over smoothly
    maqueen.motor_stop(maqueen.Motors.ALL)


def on_forever():
    global last_turn, has_block
    
    # 1. ULTRASONIC GRAB LOGIC (Only runs if empty-handed)
    if not has_block:
        distance = maqueen.ultrasonic()
        
        if distance > 0 and distance < 6:
            maqueen.motor_stop(maqueen.Motors.ALL)
            basic.pause(200)
            
            # Clenching part
            maqueen.servo_run(maqueen.Servos.S1, 100)
            basic.pause(1000)
            
            # Update state to carrying
            has_block = True
            
            # Execute the two phase 180 spin
            turn_until_line()
            return

    # 2. LINE FOLLOWING & STOP LOGIC
    left = maqueen.read_patrol(maqueen.Patrol.PATROL_LEFT)
    right = maqueen.read_patrol(maqueen.Patrol.PATROL_RIGHT)
    
    # STOP LOGIC 
    if left == 0 and right == 0:
        basic.pause(50) 
        left = maqueen.read_patrol(maqueen.Patrol.PATROL_LEFT)
        right = maqueen.read_patrol(maqueen.Patrol.PATROL_RIGHT)
        
        if left == 0 and right == 0:
            maqueen.motor_stop(maqueen.Motors.ALL)
            
            # DROP OFF SHENANIGANS 
            if has_block:
                # Hold for 5 seconds
                basic.pause(5000)
                
                # Drop it
                maqueen.servo_run(maqueen.Servos.S1, 20)
                basic.pause(500)
                
                # Update state to empty-handed
                has_block = False
                
                # Use the two-phase spin to escape the stop line
                turn_until_line()
            
            return

    # Normal Line Following
    if left == 0 and right == 0:
        maqueen.motor_run(maqueen.Motors.ALL, maqueen.Dir.CW, base_speed)
        last_turn = 0
        
    elif left == 0 and right == 1:
        maqueen.motor_run(maqueen.Motors.M2, maqueen.Dir.CW, outer_wheel_speed)
        maqueen.motor_run(maqueen.Motors.M1, maqueen.Dir.CW, inner_wheel_speed)
        last_turn = 1
        
    elif left == 1 and right == 0:
        maqueen.motor_run(maqueen.Motors.M1, maqueen.Dir.CW, outer_wheel_speed)
        maqueen.motor_run(maqueen.Motors.M2, maqueen.Dir.CW, inner_wheel_speed)
        last_turn = 2
        
    elif left == 1 and right == 1:
        if last_turn == 1:
            maqueen.motor_run(maqueen.Motors.M2, maqueen.Dir.CW, outer_wheel_speed)
            maqueen.motor_stop(maqueen.Motors.M1)
        elif last_turn == 2:
            maqueen.motor_run(maqueen.Motors.M1, maqueen.Dir.CW, outer_wheel_speed)
            maqueen.motor_stop(maqueen.Motors.M2)
        else:
            maqueen.motor_stop(maqueen.Motors.ALL)

basic.forever(on_forever)