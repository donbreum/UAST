#!/usr/bin/python3
# Standard libraries
import struct
# Third-party libraries
import rospy
from mavlink_lora.msg import mavlink_lora_msg


# defines
MAVLINK_MSG_ID_PARAM_REQUEST_LIST = 21
MAVLINK_MSG_ID_PARAM_REQUEST_LIST_LEN = 2
MAVLINK_MSG_ID_PARAM_VALUE = 22

MAVLINK_MSG_ID_MISSION_REQUEST_LIST = 43
MAVLINK_MSG_ID_MISSION_REQUEST_LIST_LEN = 2
MAVLINK_MSG_ID_MISSION_ITEM = 39

MAVLINK_MSG_ID_PARAM_REQUEST_READ_LEN = 20
MAVLINK_MSG_ID_PARAM_REQUEST_READ = 20
MAVLINK_MSG_ID_BATTERY_STATUS = 147
bat_voltage = "BAT_CAPACITY"


# variables
msg = mavlink_lora_msg()

def on_mavlink_msg(msg):
    if msg.msg_id == MAVLINK_MSG_ID_MISSION_ITEM:
        (param_value, param_count, param_index, param_id, param_type) = struct.unpack('<fHH16sB', msg.payload)
        print param_id, param_value, param_count
    if msg.msg_id == MAVLINK_MSG_ID_PARAM_VALUE:
        (param_value, param_count, param_index, param_id, param_type) = struct.unpack('<fHH16sB', msg.payload)
        print param_id, param_value, param_count
    return


def send_mavlink_param_req_mission_list(mavlink_msg_pub):
    return


def send_mavlink_param_req_bat(mavlink_msg_pub):
    target_system = 1 # Pixhawk2 PX4
    target_component = 0
    param_id = MAVLINK_MSG_ID_BATTERY_STATUS
    param_index = -1
    msg.header.stamp = rospy.Time.now()
    msg.msg_id = MAVLINK_MSG_ID_PARAM_REQUEST_READ
    msg.payload_len = MAVLINK_MSG_ID_PARAM_REQUEST_READ_LEN
    # Create the payload/data field
    msg.payload = struct.pack('<BB16sh', target_system, target_component, 
                           bat_voltage, param_index)
    # msg.payload = struct.pack('<BBhh', target_system, target_component,
    #                           param_id, param_index)
    # Publish the message
    mavlink_msg_pub.publish(msg)
    return


def send_mavlink_param_req_list(mavlink_msg_pub):
    target_system = 1 # Pixhawk2 PX4
    target_component = 0
    # no need to set sys_id, comp_id or checksum, this is handled by the mavlink_lora node.
    msg.header.stamp = rospy.Time.now()
    msg.msg_id = MAVLINK_MSG_ID_PARAM_REQUEST_LIST
    msg.payload_len = MAVLINK_MSG_ID_PARAM_REQUEST_LIST_LEN
    msg.payload = struct.pack('<BB', target_system, target_component)
    mavlink_msg_pub.publish(msg)
    return


def main():
    request_sent = False
    mavlink_lora_sub_topic = '/mavlink_rx'
    mavlink_lora_pub_topic = '/mavlink_tx'
    update_interval = 1
    # launch node
    rospy.init_node('mavlink_lora_get_actions_list')
    mavlink_msg_pub = rospy.Publisher(mavlink_lora_pub_topic, mavlink_lora_msg, queue_size=0) # mavlink_msg publisher
    rospy.Subscriber(mavlink_lora_sub_topic, mavlink_lora_msg, on_mavlink_msg) # mavlink_msg subscriber
    rate = rospy.Rate(update_interval)
    rospy.sleep(1) # wait until everything is running

    # loop until shutdown
    while not (rospy.is_shutdown()):
        # do stuff
        if request_sent == False:
            print 'Requesting mission list'
            send_mavlink_param_req_bat(mavlink_msg_pub)
            request_sent = True	

        # sleep the defined interval
	rate.sleep()
    return


if __name__ == "__main__":
    main()
