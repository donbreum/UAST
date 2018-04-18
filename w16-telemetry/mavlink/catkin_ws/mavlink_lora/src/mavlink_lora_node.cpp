/***************************************************************************
# MavLink LoRa node (ROS)
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

Requires ros serial package (sudo apt install ros-kinetic-serial)

Please notice that the serial device and baudrate are currently hardcoded
in the source below.

Revision
2018-04-17 KJ First released test version
****************************************************************************/
/* includes */
#include <ros/ros.h>
#include <serial/serial.h>
#include <std_msgs/String.h>
#include <mavlink_lora/mavlink_lora_msg.h>	

extern "C"
{
	#include "mavlink_lora_lib.h"
}
/***************************************************************************/
/* global variables */

serial::Serial ser;
unsigned long secs_init;
ros::Publisher msg_pub;
uint8_t rx_buffer[4096];

/***************************************************************************/
void mavlink_tx_callback(const mavlink_lora::mavlink_lora_msg::ConstPtr& msg)
{
	unsigned char *payload =  (unsigned char *) &msg->payload.front();
	ml_queue_msg_generic(msg->msg_id, msg->payload_len, payload);
	ml_tx_update();
}
/***************************************************************************/
void ml_parse_msg(unsigned char *msg)
{
  mavlink_lora::mavlink_lora_msg m;
  m.header.stamp = ros::Time::now();
  m.payload_len = msg[ML_POS_PAYLOAD_LEN];
  m.seq = msg[ML_POS_PACKET_SEQ];
  m.sys_id = msg[ML_POS_SYS_ID];
  m.comp_id = msg[ML_POS_COMP_ID];
  m.msg_id = msg[ML_POS_MSG_ID];
  
  int i;
  for (i=0; i<m.payload_len; i++)
  	m.payload.push_back(msg[ML_POS_PAYLOAD + i]);
  
	unsigned char crc_lsb = msg[6 + m.payload_len];
	unsigned char crc_msb = msg[7 + m.payload_len];
	m.checksum = (8 << crc_msb) | crc_lsb;
  
  msg_pub.publish(m);
}
/***************************************************************************/
void ml_tx_update (void)
{
    int bytes_written = ser.write((const uint8_t *) txbuf, txbuf_cnt);
		txbuf_cnt = 0; 
}
/***************************************************************************/
unsigned long millis(void)
{
    struct timeval te; 
    gettimeofday(&te, NULL); /* get current time */

	if (secs_init == 0)
	{
		secs_init = te.tv_sec;
	}

	return ((unsigned long) (te.tv_sec - secs_init)*1000 + te.tv_usec/1000);
}
/***************************************************************************/
int main (int argc, char** argv)
{
    ros::init(argc, argv, "mavlink_lora_node");
    ros::NodeHandle nh;

    ros::Time begin = ros::Time::now();

    ros::Subscriber write_sub = nh.subscribe("mavlink_tx", 10, mavlink_tx_callback);
    msg_pub = nh.advertise<mavlink_lora::mavlink_lora_msg>("mavlink_rx", 1);

    try
    {
        ser.setPort("/dev/ttyUSB0");
        ser.setBaudrate(57600);
        serial::Timeout to = serial::Timeout::simpleTimeout(100);
        ser.setTimeout(to);
        ser.open();
    }
    catch (serial::IOException& e)
    {
        ROS_ERROR_STREAM("Unable to open port ");
        return -1;
    }

    if(ser.isOpen())
    {
        ROS_INFO_STREAM("Serial Port initialized");
    }
    else
    {
        return -1;
    }
    
    ml_init();
		ml_set_monitor_all();

    ros::Rate loop_rate(100);
    while(ros::ok())
    {
        ros::spinOnce();

        if(ser.available())
        {
        		unsigned long cnt = ser.read(rx_buffer, ser.available()); 
            ml_rx_update(millis(), rx_buffer, cnt);
        }
        loop_rate.sleep();
    }
}
/***************************************************************************/

