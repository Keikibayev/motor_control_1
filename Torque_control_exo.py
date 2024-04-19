import odrive
import time
import sys
import io
import odrive.shell
import kbhit

AXIS_STATE_FULL_CALIBRATION_SEQUENCE = 3
AXIS_STATE_CLOSED_LOOP_CONTROL = 8
AXIS_STATE_IDLE = 1
run_gait_flag = False
torque = 0.34
knee_torque_forward = -0.07
knee_torque_backward = 0.07
run_gait_flag = False
gaitStartTime = 0
current_time = 0
current_time2 = 0
negative = -1
gaitDuration = 1 # in minutes
interval = 1.2
fast_interval = 0
int_counter = 0
directionKL = 1
edge = 2.8
fast_time = 0
fast_interval_value = 0.1

def Move():
    global torque
    global negative
    global odrvR
    global odrvL
    global int_counter
    global knee_torque_forward
    global knee_torque_backward
    global edge
    global torque_value_HL
    
    odrvL.axis0.controller.input_torque = torque
    odrvR.axis0.controller.input_torque = torque

    actual_pos_HL = odrvL.axis0.encoder.pos_estimate
    actual_pos_HR = odrvR.axis0.encoder.pos_estimate
    curr_HL = odrvL.axis0.motor.current_control.Iq_measured
    curr_HR = odrvR.axis0.motor.current_control.Iq_measured

    if torque > 0:
        if (1 < actual_pos_HL < 1.5):
            odrvL.axis1.controller.input_torque = 0
        if (1.5 < actual_pos_HL < edge):
            odrvL.axis1.controller.input_torque = knee_torque_forward*0.8
        if (actual_pos_HL > edge):
            torque = torque*negative
            print()
            odrvL.axis1.controller.input_torque = knee_torque_forward
            odrvR.axis1.controller.input_torque = knee_torque_forward
            int_counter = 0
        elif (int_counter > 3):
            torque = torque*negative
            print("Turning on forward")
            odrvL.axis1.controller.input_torque = knee_torque_forward
            odrvR.axis1.controller.input_torque = knee_torque_forward
            int_counter = 0
        else:
            int_counter += 1
        print("\nForward. \nLeft: {0:4.5f},\nRight: {1:4.5f}\n".format(curr_HL, curr_HR))
    
    else:
        if (1 < actual_pos_HR < 1.5):
            odrvR.axis1.controller.input_torque = 0
        if (1.5 < actual_pos_HR < edge):
            odrvR.axis1.controller.input_torque = knee_torque_forward*0.8
        if (actual_pos_HR < -edge):
            torque = torque*negative
            odrvL.axis1.controller.input_torque = knee_torque_backward
            odrvR.axis1.controller.input_torque = knee_torque_backward

            int_counter = 0
        elif (int_counter > 3):
            torque = torque*negative
            print("Turning on backward")
            odrvL.axis1.controller.input_torque = knee_torque_backward
            odrvR.axis1.controller.input_torque = knee_torque_backward
            int_counter = 0
        else:
            int_counter += 1
            
        print("\nBackward. \nLeft: {0:4.5f},\nRight: {1:4.5f}\n".format(curr_HL, curr_HR))

def Calibrate(inp_text):
    global run_gait_flag
    global odrvR
    global odrvL
    run_gait_flag = False
    if inp_text == "Yes" or inp_text == "yes" or inp_text == "Y" or inp_text == "y":
        print("Calibration")
        odrvR.clear_errors()
        odrvL.clear_errors()
        time.sleep(1)
        odrvR.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
        odrvL.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
        time.sleep(1)
        odrvR.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
        odrvL.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
        time.sleep(15)

def StopGait():
    global odrvR
    global odrvL
    global run_gait_flag
    run_gait_flag = False
    
    odrvL.axis0.controller.input_torque = 0
    odrvL.axis1.controller.input_torque = 0
    odrvR.axis0.controller.input_torque = 0
    odrvR.axis1.controller.input_torque = 0
    time.sleep(2)
    
    odrvR.axis0.requested_state = AXIS_STATE_IDLE
    odrvR.axis1.requested_state = AXIS_STATE_IDLE
    odrvL.axis0.requested_state = AXIS_STATE_IDLE
    odrvL.axis1.requested_state = AXIS_STATE_IDLE

def GaitLoop():
    global first_time_to_run_exo
    global run_gait_flag
    global current_time
    global gaitStartTime
    global torque
    global negative
    global odrvR
    global odrvL
    global int_counter
    global interval
    global knee_torque_forward
    global knee_torque_backward
    global edge
    global fast_time
    global torque_value_HL

    print("Searching for ODrive...")
    fast_interval = fast_interval_value

    odrvR = odrive.find_any(serial_number="2085319C5553")
    odrvL = odrive.find_any(serial_number="206031995553")

    # odrvL.axis0.controller.config.vel_limit = 1
    # odrvL.axis1.controller.config.vel_limit = 6

    # odrvL.axis0.controller.config.vel_limit = 1
    # odrvL.axis1.controller.config.vel_limit = 6

    ask_calib_for_calib = input("Is calibration needed? (Y, if needed, else just Enter)  ")
    print()
    Calibrate(ask_calib_for_calib)

    command = input("Enter the command (run, calibrate, stop, exit, torque, interval, edge) ")
    print()

    gaitDuration = 2
    
    while True:
        if not isinstance(gaitDuration, int):
            print("Incorrect format of gait duration. Enter only numbers.")
            gaitDuration = int(input("Enter Gait duration in minutes:  "))
            print()
        else:
            break
    
    waiter = kbhit.KBHit()

    while True:
        try:
            if waiter.kbhit():
                command = input("Enter the command (run, calibrate, stop, exit, torque, interval, edge) ")
                print()

            match command:
                case "run":
                    print("running...")
                    print()
                    run_gait_flag = True
                    first_time_to_run_exo = time.time()
                    gaitStartTime = time.time()
                    fast_time = time.time()
                    odrvR.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
                    odrvR.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
                    odrvL.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
                    odrvL.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
                    
                case "calibrate":
                    Calibrate(inp_text = "Y")
                    command = input("Enter the command (run, calibrate, stop, exit, torque, interval, edge) ")
                    print()
                
                case "stop":
                    StopGait()
                    command = input("Enter the command (run, calibrate, stop, exit, torque, interval, edge) ")
                    print()
                
                case "torque":
                    torque = float(input("Enter the torque value (0.3 max) "))
                    if torque >= 0.3:
                        print("Too much torque! Setting to 0.1...")
                        torque = 0.1
                    else:
                        print("Torque set to {0:4.3f}".format(torque))
                    print()
                
                case "edge":
                    edge = float(input("Enter the amplitude value (1.5 - 4 max) "))
                    if edge > 4:
                        print("Too much amplitude! Setting to 4...")
                        edge = 4
                    else:
                        print("Amplitude set to {0:4.3f}".format(edge))
                    print()
                
                case "interval":
                    interval = float(input("Enter the speed value (time to cycle)(0.4-1s) "))
                    if interval > 1:
                        print("Too slow! Setting to 1s...")
                        interval = 1
                    elif interval < 0.4:
                        print("Too fast! Setting to 0.4s")
                        interval = 0.4
                    elif 0.8 >= interval >= 1:
                        odrvL.axis0.controller.config.vel_limit = 4
                        odrvR.axis0.controller.config.vel_limit = 4
                        print("Speed set to {0:4.2f}s".format(interval))
                    elif 0.6 >= interval >= 0.79:
                        odrvL.axis0.controller.config.vel_limit = 5
                        odrvR.axis0.controller.config.vel_limit = 5
                        print("Speed set to {0:4.2f}s".format(interval))
                    elif 0.4 >= interval >= 0.59:
                        odrvL.axis0.controller.config.vel_limit = 6
                        odrvR.axis0.controller.config.vel_limit = 6
                    else:
                        print("Speed set to {0:4.2f}s".format(interval))
                    print()

                case "exit":
                    print("exiting...")
                    run_gait_flag = False
                    odrvL.axis0.controller.input_torque = 0
                    odrvL.axis1.controller.input_torque = 0
                    odrvR.axis0.controller.input_torque = 0
                    odrvR.axis1.controller.input_torque = 0
                    time.sleep(2)
                    odrvR.axis0.requested_state = AXIS_STATE_IDLE
                    odrvR.axis1.requested_state = AXIS_STATE_IDLE
                    odrvL.axis0.requested_state = AXIS_STATE_IDLE
                    odrvL.axis1.requested_state = AXIS_STATE_IDLE
                    sys.exit(1)
                
                case "":
                    pass
                
                case _:
                    print("incorrect command")
                
            command = ""

            current_time = time.time()
            if run_gait_flag and (current_time-first_time_to_run_exo) >= interval:                
                Move()
                fast_interval = fast_interval_value
                first_time_to_run_exo = current_time

            current_time2 = time.time()
            if run_gait_flag and (current_time2-fast_time) >= fast_interval:
                torque_value_HL = odrvL.axis0.motor.current_control.Iq_measured
                torque_value_HR = odrvR.axis0.motor.current_control.Iq_measured

                if abs(torque_value_HL) > 6.5 or abs(torque_value_HR) > 6.5: # TODO: change current value
                    torque = torque*negative
                    Move()
                    print("Too much current!")
                    fast_interval = interval
                
                fast_time = current_time2

            # if (current_time - gaitStartTime) >= gaitDuration*60 and run_gait_flag == True:
            #     print ("{} minutes passed. Idle mode".format(gaitDuration))
            #     command = "stop"
                    
        except KeyboardInterrupt:
            print ('Interrupted from keyboard')
            print()
            odrvL.axis0.controller.input_torque = 0
            odrvL.axis1.controller.input_torque = 0
            odrvR.axis0.controller.input_torque = 0
            odrvR.axis1.controller.input_torque = 0
            time.sleep(2)
            odrvR.axis0.requested_state = AXIS_STATE_IDLE
            odrvR.axis1.requested_state = AXIS_STATE_IDLE
            odrvL.axis0.requested_state = AXIS_STATE_IDLE
            odrvL.axis1.requested_state = AXIS_STATE_IDLE
            sys.exit(1)
        
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            print()
            odrvL.axis0.controller.input_torque = 0
            odrvL.axis1.controller.input_torque = 0
            odrvR.axis0.controller.input_torque = 0
            odrvR.axis1.controller.input_torque = 0
            time.sleep(1)
            odrvR.axis0.requested_state = AXIS_STATE_IDLE
            odrvR.axis1.requested_state = AXIS_STATE_IDLE
            odrvL.axis0.requested_state = AXIS_STATE_IDLE
            odrvL.axis1.requested_state = AXIS_STATE_IDLE
            sys.exit(1)
            raise

if __name__ == "__main__":
    GaitLoop()