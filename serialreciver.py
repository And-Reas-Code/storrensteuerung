#!/usr/bin/env python3
import serial
import pickle

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)
    ser.reset_input_buffer()

    init_file_switch = open("/root/scripts/steuerung/status/switches.txt", "wb")
    # Values: [ WIND-RAIN-AUTO, SUN-AUTO ] 
    init_states = ["TRUE", "TRUE"] 
    pickle.dump(init_states, init_file_switch) 
    init_file_switch.flush()
    init_file_switch.close()

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            # RAIN, WIND, SUN
            serial_states = line.split(';')
            rain = serial_states[0].__eq__('TRUE')
            wind = int(serial_states[1])
            sun = int(serial_states[2])

            file = open("/root/scripts/steuerung/status/variables.txt", "wb")
            pickle.dump(serial_states, file) 
            file.flush()
            file.close()

            file_switch = open("/root/scripts/steuerung/status/switches.txt", "rb")
            switch = pickle.load(file_switch) 
            wind_rain_auto = switch[0].__eq__('TRUE')
            sun_auto = switch[1].__eq__('TRUE')

            # file2 = open("/root/scripts/steuerung/status/variables.txt", 'rb')
            # mya = pickle.load(file2) 
            # print(mya[0])
            # print(mya[1])
            # print(mya[2])

            # print("Wind: " + str(wind) + "; Sun: " + str(sun))
            # 
            # if (rain):
            #     print("Es regnet!")
            # else:
            #     print("Es regnet nicht!")
            # 
            # if (wind_rain_auto):
            #     print("Auto Wind!")
            # else:
            #     print("Kein Auto Wind!")
            # 
            # if (sun_auto):
            #     print("Auto Sun!")
            # else:
            #     print("Kein Auto Sun!")

            if (wind_rain_auto & rain):
                print("Storre fährt ein - Regen!")

            if (wind_rain_auto & (wind >= 10)):
                print("Storre fährt ein - Wind!")

            if (sun_auto & (sun <= 80)):
                print("Storre fährt aus - Sonne!")


