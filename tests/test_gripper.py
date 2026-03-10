 # Start with the claw open
maqueen.servo_run(maqueen.Servos.S1, 20)

while True:
    # Get the distance 
    distance = maqueen.ultrasonic()

    # Check if the object is in the sweet spot (between 1cm and 6cm)
    if distance > 0 and distance < 6:

        # Stop moving to avoid crashing
        maqueen.motor_stop(maqueen.Motors.ALL)
        basic.pause(200) 
        # CLENCH
        maqueen.servo_run(maqueen.Servos.S1, 100)
        basic.pause(1000)

    else:
        # Keep the claw open
        maqueen.servo_run(maqueen.Servos.S1, 20)
        # drive forward to hunt for an object (Speed 30)
        maqueen.motor_run(maqueen.Motors.ALL, maqueen.Dir.CW, 30) 