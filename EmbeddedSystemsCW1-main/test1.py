import time
from smbus2 import SMBus, i2c_msg
import json
import time
import board
import busio
import adafruit_vl53l0x
import paho.mqtt.client as mqtt
import ssl



client=mqtt.Client()
client.connect("test.mosquitto.org", port=1883)

# client.publish("IC.embedded/Power_Puff_Girls/test", "15 feb 2021")

# meas_dist=i2c_msg.write(0x29, [1,2,3,4])
# read_dist=i2c_msg.read(0x29, 32)
# on=1
#
# with SMBus(1) as bus:
#     bus.i2c_rdwr(meas_dist)
#     time.sleep(0.1)
#     bus.i2c_rdwr(read_dist)
#
# meas_dist=list(meas_dist)
# read_dist=list(read_dist)
# print("WRITE")
# for value in meas_dist:
#     print(value)
# print("READ")
# for value in read_dist:
#     print(value)
#
# distance=json.dumps({'name':'distance1','distancerecord':read_dist})
# print(distance)
##########


# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
# Simple demo of the VL53L0X distance sensor.
# Will print the sensed range/distance every second.

# Initialize I2C bus and sensor.
i2c = busio.I2C(board.SCL, board.SDA)
vl53 = adafruit_vl53l0x.VL53L0X(i2c)
# Optionally adjust the measurement timing budget to change speed and accuracy.
# See the example here for more details:
#   https://github.com/pololu/vl53l0x-arduino/blob/master/examples/Single/Single.ino
# For example a higher speed but less accurate timing budget of 20ms:
# vl53.measurement_timing_budget = 20000
# Or a slower but more accurate timing budget of 200ms:
# vl53.measurement_timing_budget = 200000
# The default timing budget is 33ms, a good compromise of speed and accuracy.
# Main loop will read the range and print it every second.
# while True:

def getStatusReg():
    STATUS_REG = i2c_msg.write(0x18, [0x27])   #STATUS_REG(27h)
    STATUS_REG_read = i2c_msg.read(0x18, data_size)
    bus.i2c_rdwr(STATUS_REG, STATUS_REG_read)
    return STATUS_REG_read

def checkBit3(status_reg):
    BIT_3_MASK = 0b00001000
    reg = bin(int.from_bytes(status_reg, "little"))
    value = reg and BIT_3_MASK
    if value is 0b0001000: return 1
    elif value is not 0: return 0
    #read status_reg
    # if status_reg(3) = 0 then read status_reg again
    # if status_reg(7) = 1 then get x y z

def checkBit7(status_reg):
    BIT_7_MASK = 0b10000000
    reg = bin(int.from_bytes(status_reg, "little"))
    value = reg and BIT_7_MASK
    if value == 0b10000000:
        return true
    else:
        return false



def getX():
    OUT_X_L = i2c_msg.write(0x18, [0x28])   #OUT_X_L(28h)
    OUT_X_L_read = i2c_msg.read(0x18, data_size)
    bus.i2c_rdwr(OUT_X_L, OUT_X_L_read)
    OUT_X_H = i2c_msg.write(0x18, [0x29])   #OUT_X_H(29h) 
    OUT_X_H_read = i2c_msg.read(0x18, data_size)
    bus.i2c_rdwr(OUT_X_H, OUT_X_H_read)
    x_l = int.from_bytes(OUT_X_L_read,'little')
    x_h = int.from_bytes(OUT_X_H_read,'little')

    out_x = x_h*256 + x_l
    out_x = twosComplementAdjust(out_x)
    return out_x

def getY():
    OUT_Y_L = i2c_msg.write(0x18, [0x2a])   #OUT_Y_L(2Ah)
    OUT_Y_L_read = i2c_msg.read(0x18, data_size)
    bus.i2c_rdwr(OUT_Y_L, OUT_Y_L_read)
    OUT_Y_H = i2c_msg.write(0x18, [0x2b])   #OUT_Y_H(2Bh)
    OUT_Y_H_read = i2c_msg.read(0x18, data_size)
    bus.i2c_rdwr(OUT_Y_H, OUT_Y_H_read)
    y_l = int.from_bytes(OUT_Y_L_read,"little")
    y_h = int.from_bytes(OUT_Y_H_read,'little')
    out_y = y_h*256 + y_l
    out_y = twosComplementAdjust(out_y)
    return out_y

def getZ():
    OUT_Z_L = i2c_msg.write(0x18, [0x2c])   #OUT_Y_L(2Ch)
    OUT_Z_L_read = i2c_msg.read(0x18, data_size)
    bus.i2c_rdwr(OUT_Z_L, OUT_Z_L_read)
    OUT_Z_H = i2c_msg.write(0x18, [0x2d])   #OUT_Y_H(2Dh)
    OUT_Z_H_read = i2c_msg.read(0x18, data_size)
    bus.i2c_rdwr(OUT_Z_H, OUT_Z_H_read)
    z_l = int.from_bytes(OUT_Z_L_read,"little")
    z_h = int.from_bytes(OUT_Z_H_read,'little')
    out_z = z_h*256 + z_l
    out_z = twosComplementAdjust(out_z)
    return out_z

def twosComplementAdjust(x):
    binary_number = int("{0:016b}".format(x))
    flipped_binary_number = ~ binary_number
    flipped_binary_number = flipped_binary_number + 1
    str_twos_complement = str(flipped_binary_number)
    twos_complement = int(str_twos_complement, 2)
    # print(twos_complement)
    # if x > 32767:
    #     x = x - 65536
    # else
    #     continue
    # x*=9.81
    return twos_complement

# initial=i2c_msg.write_byte_data(0x18, [0x03], 0)
# initial2=i2c_msg.write_byte_data(0x18, [0x04], 0)
count=0
data_size=1
# meas_x=i2c_msg.write(0x18, [0x29])
# meas_y=i2c_msg.write(0x18, [0x2B])
# meas_z=i2c_msg.write(0x18, [0x2D])
# read_x=i2c_msg.read(0x18, data_size)
# read_y=i2c_msg.read(0x18, data_size)
# read_z=i2c_msg.read(0x18, data_size)


l1=[]
with SMBus(1) as bus:
    # Setting Control Registers
    bus.write_byte_data(0x18, 0x03, 1)
    bus.write_byte_data(0x18, 0x04, 0)
    bus.write_byte_data(0x18, 0x1e, 16)
    bus.write_byte_data(0x18, 0x20, 159) #119
    bus.write_byte_data(0x18, 0x23, 0)
    bus.write_byte_data(0x18, 0x21, 200)
    bus.write_byte_data(0x18, 0x22, 0)
    bus.write_byte_data(0x18, 0x24, 0)
    bus.write_byte_data(0x18, 0x25, 0)
    bus.write_byte_data(0x18, 0x34, 0)
    bus.write_byte_data(0x18, 0x30, 0)

# Write CTRL_REG1
# Write CTRL_REG2
# Write CTRL_REG3
# Write CTRL_REG4
# Write CTRL_REG5
# Write CTRL_REG6
# Write REFERENCE
# Write INTx_THS
# Write INTx_DUR
# Write INTx_CFG
# Write CTRL_REG5

    while True:
        # setup()
        # l1=bus.read_byte_data(0x18, 0x27)
        # bus.i2c_rdwr(meas_x)
        # bus.i2c_rdwr(meas_y)
        # bus.i2c_rdwr(meas_z)

        # time.sleep(0.25)
        # bus.i2c_rdwr(read_x)
        # bus.i2c_rdwr(read_y)
        # bus.i2c_rdwr(read_z)
        # text_x=str(read_x)
        # text_y=str(read_y)
        # text_z=str(read_z)
        # number_x = ord(text_x)-63
        # number_y = ord(text_y)-63
        # number_z = ord(text_z)-63
        # print(l1, number_z, number_y, number_x, )
        # print("Range: {0}mm".format(vl53.range))
        time.sleep(0.5)
        # range=int(vl53.range)
        # distance="distance:"+str(vl53.range)+"mm"
        # coords="x:" +str(number_x)+" y:" +str(number_y)+" z:"+str(number_z)
        # # print(coords, distance)
        # reading=coords+" "+distance
        # data=json.dumps({
        # "number_x":number_x,
        # "number_y":number_y,
        # "number_z":number_z,
        # "distance":range
        # })
        # print(data)
        status_reg = getStatusReg()
        # print(bin(int.from_bytes(status_reg, "little")))
        bitchecker=checkBit3(status_reg)
        print(bitchecker)
-       while bitchecker is True: 
            time.sleep(0.1)
            status_reg = getStatusReg()

        if checkBit7(status_reg):
            test_x=int(getX())
            test_y=int(getY())
            test_z=int(getZ())
            test_x=round(test_x, 0)
            test_y=round(test_y, 0)
            test_z=round(test_z, 0)

#             print("x:" +str(test_x)+" y:" +str(test_y)+" z:"+str(test_z))
        # client.publish("IC.embedded/Power_Puff_Girls/test", data)
        # print(text)


##### "READING" is a concatonated number_z + number_y + number_z + distance
# mqtt.error_string(MSG_INFO.rc) #MSG_INFO is result of publish()

client.tls_set(ca_certs="mosquitto.org.crt",
certfile="client.crt",keyfile="client.key",
tls_version=ssl.PROTOCOL_TLSv1_2)

def on_message(client,userdata,message):
    print("Received message:{} on topic{}".format(message.payload, message.topic))

client.on_message=on_message

client.subscribe("IC.embedded/Power_Puff_Girls/#")

client.loop()
#  data=json.dumps({"number_x":number_x, "number_y":number_y, "number_z":number_z,
# "distance": range })
# print(data)