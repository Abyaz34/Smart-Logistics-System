# Speed settings to tune maqueen's smoothness
base_speed = 50        # Speed for going straight
outer_wheel_speed = 50 # Speed of the fast wheel during a turn
inner_wheel_speed = 20  # Slower speed for the inside wheel to make an arc

last_turn = 0

def on_forever():
    global last_turn
    
    left = maqueen.read_patrol(maqueen.Patrol.PATROL_LEFT)
    right = maqueen.read_patrol(maqueen.Patrol.PATROL_RIGHT)
    
    # This checks if both sensors are on the thick black bar.
    # We add a tiny pause and check again to make sure it's not just a thin cross-line.
    if left == 0 and right == 0:
        basic.pause(50) # Tiny delay to see if we are still on black
        left = maqueen.read_patrol(maqueen.Patrol.PATROL_LEFT)
        right = maqueen.read_patrol(maqueen.Patrol.PATROL_RIGHT)
        if left == 0 and right == 0:
            maqueen.motor_stop(maqueen.Motors.ALL)
            # This 'return' stops the rest of the code from running so it stays stopped.
            return
    if left == 0 and right == 0:
        # Perfectly on the line
        maqueen.motor_run(maqueen.Motors.ALL, maqueen.Dir.CW, base_speed)
        last_turn = 0
        
    elif left == 0 and right == 1:
        # Drifting slightly right (left sensor on black)
        maqueen.motor_run(maqueen.Motors.M2, maqueen.Dir.CW, outer_wheel_speed)
        maqueen.motor_run(maqueen.Motors.M1, maqueen.Dir.CW, inner_wheel_speed)
        last_turn = 1
        
    elif left == 1 and right == 0:
        # Drifting slightly left (right sensor on black)
        maqueen.motor_run(maqueen.Motors.M1, maqueen.Dir.CW, outer_wheel_speed)
        maqueen.motor_run(maqueen.Motors.M2, maqueen.Dir.CW, inner_wheel_speed)
        last_turn = 2
        
    elif left == 1 and right == 1:
        # Lost the line entirely = Sharp 90-degree corner
        if last_turn == 1:
            maqueen.motor_run(maqueen.Motors.M2, maqueen.Dir.CW, outer_wheel_speed)
            maqueen.motor_stop(maqueen.Motors.M1)
        elif last_turn == 2:
            maqueen.motor_run(maqueen.Motors.M1, maqueen.Dir.CW, outer_wheel_speed)
            maqueen.motor_stop(maqueen.Motors.M2)
        else:
            maqueen.motor_stop(maqueen.Motors.ALL)

basic.forever(on_forever)
