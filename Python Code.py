import can
import math
import time

#Functions
def get_RPM():
    recv_msg = bus.recv()
    ID = hex(recv_msg.arbitration_id)
    recv_data = recv_msg.data
    recv_data_str = recv_data.hex(' ').upper().replace(" ","")
    recv_eRPM = recv_data_str[:8]
    recv_RPM = math.trunc(int(recv_eRPM,16)/7)
    return ID,recv_RPM

#Setting interface
filters = [{"can_id":0x905, "can_mask":0x7ff,"extended":True},{"can_id":0x909, "can_mask":0x7ff,"extended":True}]
bus = can.interface.Bus(channel='can0',bustype='socketcan',bitrate='500000',can_filters=filters)

#RPM input
RPM_5 = 4000
RPM_9 = 4000
eRPM_5 = RPM_5*7
eRPM_9 = RPM_9*7
eRPM_5_hex = eRPM_5.to_bytes(4,'big')
eRPM_9_hex = eRPM_9.to_bytes(4,'big')

#Send CAN
send_RPM_5 = can.Message(arbitration_id=0x305,data=eRPM_5_hex,is_extended_id=True)
send_RPM_9 = can.Message(arbitration_id=0x309,data=eRPM_9_hex,is_extended_id=True)
bus.send_periodic(send_RPM_5, 0.02)#50Hz
bus.send_periodic(send_RPM_9, 0.02)


#Receive CAN
ID1 = '0x905'
ID2 = '0x909'
recv_RPM_5 =recv_RPM_9 = 0
while(True):
    [ID, recv_RPM] = get_RPM()
#     print("\n")
    if (ID == ID1):
        recv_RPM_5 = recv_RPM
    elif (ID == ID2):
        recv_RPM_9 = recv_RPM
    [ID, recv_RPM] = get_RPM()
    if (ID == ID1):
        recv_RPM_5 = recv_RPM
    elif (ID == ID2):
        recv_RPM_9 = recv_RPM
    print(recv_RPM_5,recv_RPM_9)