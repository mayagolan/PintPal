import time
from smbus2 import SMBus, i2c_msg
import json

#
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

# initial=i2c_msg.write_byte_data(0x18, [0x03], 0)
# initial2=i2c_msg.write_byte_data(0x18, [0x04], 0)
count=0
data_collect=1
meas_x=i2c_msg.write(0x18, [0x29])
meas_y=i2c_msg.write(0x18, [0x2B])
meas_z=i2c_msg.write(0x18, [0x2D])
read_x=i2c_msg.read(0x18, data_collect)
read_y=i2c_msg.read(0x18, data_collect)
read_z=i2c_msg.read(0x18, data_collect)


l1=[]
with SMBus(1) as bus:
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


    while True:
        l1=bus.read_byte_data(0x18, 0x27)
        bus.i2c_rdwr(meas_x)
        bus.i2c_rdwr(meas_y)
        bus.i2c_rdwr(meas_z)

        time.sleep(0.25)
        bus.i2c_rdwr(read_x)
        bus.i2c_rdwr(read_y)
        bus.i2c_rdwr(read_z)
        text_x=str(read_x)
        text_y=str(read_y)
        text_z=str(read_z)
        number_x = ord(text_x)-63
        number_y = ord(text_y)-63
        number_z = ord(text_z)-63
        print(l1, number_z, number_y, number_x)
        # print(text)



# meas_accel=list(meas_accel)
# print(meas_accel)
# print(l1)
        # print("WRITE")
        # for value in meas_accel:
        #     print(value)
        # print("READ")
        # for value in read_accel:
        #     print(value)

# accel=json.dumps({'name':'accel1','acclrecord':read_accel})
# print(accel)
