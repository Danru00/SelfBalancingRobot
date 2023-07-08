#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float64
from sensor_msgs.msg import Imu
from math import atan2, asin

pub_rw = rospy.Publisher('/robot_assembly/rw_velocity_controller/command', Float64, queue_size=10)
pub_lw = rospy.Publisher('/robot_assembly/lw_velocity_controller/command', Float64, queue_size=10)


def quat2pitch(quat_orientation):

    x = quat_orientation.x
    y = quat_orientation.y
    z = quat_orientation.z
    w = quat_orientation.w

    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 -2.0 * (x * x + y * y)
    roll_x = atan2(t0, t1)

    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    pitch_y = asin(t2)
    
    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    yaw_z = atan2(t3, t4)

    rospy.loginfo(rospy.get_caller_id() + "roll_x: {}, pitch_y: {}, yaw_z: {}".format(roll_x, pitch_y, yaw_z))

    return roll_x

def imu_elaboration(msg):
    th = 3.1415/2
    quat_orientation = msg.orientation
    pitch = quat2pitch(quat_orientation)
    vel_out = sbr_pid.getCorrection(pitch)
    if pitch > th+30*3.14/180 or pitch < th-30*3.14/180:
     return 0
    else: 
     if pitch > th:
      return vel_out
     else:
      return -vel_out


class PidGenerator(object):

    def __init__(self, Kp, Ki, Kd):
        
        # Parameters
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        
        # State variables
        self.Eprev = 0
        self.Stdt = 0
        self.t = 0

        self.target = 3.1415/2

    def tune(self,KpNew,KiNew,KdNew):
        self.Kp = KpNew
        self.Ki = KiNew
        self.Kd = KdNew
        
    def getCorrection(self, actual):
        
        dt = 1/100

        # Error
        E = self.target - actual

        # Error derivative
        dEdt = (E - self.Eprev) / dt if self.t > 0 else 0
        
        # Error integral  
        self.Stdt += E*dt if self.t > 0 else 0
   
        # Correcting
        correction = self.Kp*E + self.Ki*self.Stdt + self.Kd*dEdt
    
        # Update
        self.t += 1
        self.Eprev = E

        return correction

def callback(msg):

    target_vel = imu_elaboration(msg)
    vel_cmd = Float64()
    vel_cmd.data = target_vel
    pub_rw.publish(vel_cmd)
    pub_lw.publish(vel_cmd)
    
    rospy.loginfo(rospy.get_caller_id() + "Output  {}".format(vel_cmd.data))
    
def PidController():

    rospy.init_node('pid_controller', anonymous=True)
  
    rospy.Subscriber("/imu", Imu, callback)
  
    rospy.spin()

  
if __name__ == '__main__':
    sbr_pid = PidGenerator(10, 5, 0.075)

    PidController()
