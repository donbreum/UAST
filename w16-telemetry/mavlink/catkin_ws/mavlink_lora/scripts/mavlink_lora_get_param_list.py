#!/usr/bin/env python
#/***************************************************************************
# MavLink LoRa node (ROS) example script
# Copyright (c) 2018, Kjeld Jensen <kjen@mmmi.sdu.dk> <kj@kjen.dk>
# SDU UAS Center, http://sdu.dk/uas 
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the copyright holder nor the names of its
#      contributors may be used to endorse or promote products derived from
#      this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#****************************************************************************
'''
This example script shows how to query a list of parameters from the flight
controller.

It has been tested using a Pixhawk 2.1 flight controller running PX4 and on
an AutoQuad flight controller. Please remember to set the correct
target_system value below.

Revision
2018-04-16 KJ First published version
'''
# parameters
mavlink_lora_sub_topic = '/mavlink_rx'
mavlink_lora_pub_topic = '/mavlink_tx'
update_interval = 1
target_system = 1 # Pixhawk2 PX4
#target_system = 66 # AutoQuad
target_component = 0

# defines
MAVLINK_MSG_ID_PARAM_REQUEST_LIST = 21
MAVLINK_MSG_ID_PARAM_REQUEST_LIST_LEN = 2
MAVLINK_MSG_ID_PARAM_VALUE = 22

# imports
import rospy
import struct
from mavlink_lora.msg import mavlink_lora_msg

# variables
msg = mavlink_lora_msg()
request_sent = False

def on_mavlink_msg (msg):
	if msg.msg_id == MAVLINK_MSG_ID_PARAM_VALUE:
		(param_value, param_count, param_index, param_id, param_type) = struct.unpack('<fHH16sB', msg.payload)	
		print param_id, param_value, param_count

def send_mavlink_param_req_list():
	# no need to set sys_id, comp_id or checksum, this is handled by the mavlink_lora node.
	msg.header.stamp = rospy.Time.now()
	msg.msg_id = MAVLINK_MSG_ID_PARAM_REQUEST_LIST
	msg.payload_len = MAVLINK_MSG_ID_PARAM_REQUEST_LIST_LEN
	msg.payload = struct.pack('<BB', target_system, target_component)
	mavlink_msg_pub.publish(msg)

# launch node
rospy.init_node('mavlink_lora_get_parameter_list')
mavlink_msg_pub = rospy.Publisher(mavlink_lora_pub_topic, mavlink_lora_msg, queue_size=0) # mavlink_msg publisher
rospy.Subscriber(mavlink_lora_sub_topic, mavlink_lora_msg, on_mavlink_msg) # mavlink_msg subscriber
rate = rospy.Rate(update_interval)
rospy.sleep (1) # wait until everything is running

# loop until shutdown
while not (rospy.is_shutdown()):
	# do stuff
	if request_sent == False:
		print 'Requesting parameter list'
		send_mavlink_param_req_list()
		request_sent = True	

	# sleep the defined interval
	rate.sleep()

