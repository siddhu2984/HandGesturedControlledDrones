
import firebase_admin
from firebase_admin import credentials, db
import time
from dronekit import connect, VehicleMode
from pymavlink import mavutil
import time
import socket
import argparse

vehicle = None

def connectMycopter():
   parser = argparse.ArgumentParser(description='commands')
   parser.add_argument('--connect')
   args = parser.parse_args()
   connection_string = args.connect
   vehicle = connect(connection_string, wait_ready=True)
   return vehicle
def arm_and_takeoff(aTargetAltitude):
   #  while not vehicle.is_armable:
   #      print("Waiting for vehicle to become armable")
   #      time.sleep(1)
    
   print("Vehicle is armable. Arming motors...")
   vehicle.mode = VehicleMode("GUIDED")
   vehicle.armed = True
    
   #  while not vehicle.armed:
   #      print("Waiting for vehicle to arm")
   #      time.sleep(1)
    
   print("Vehicle is armed. Taking off...")
   vehicle.simple_takeoff(aTargetAltitude)
    
   while True:
      print("Altitude: ", vehicle.location.global_relative_frame.alt)
      if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
         print("Target altitude reached")
         break
      time.sleep(1)

def send_body_ned_velocity(velocity_x, velocity_y, velocity_z, duration=0):
   msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_BODY_NED, # frame Needs to be MAV_FRAME_BODY_NED for forward/back left/right control.
        0b0000111111000111, # type_mask
        0, 0, 0, # x, y, z positions (not used)
        velocity_x, velocity_y, velocity_z, # m/s
        0, 0, 0, # x, y, z acceleration
        0, 0)
   for x in range(0,duration):
      vehicle.send_mavlink(msg)
      time.sleep(1)
def land_and_disarm():
   vehicle.mode = VehicleMode("LAND")
   while vehicle.location.global_relative_frame.alt > 0.1:
      time.sleep(1)
   vehicle.armed = False
   while vehicle.armed:
      time.sleep(1)
   vehicle.mode = VehicleMode("STABILIZE")



# Initialize Firebase
vehicle = connectMycopter()

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://hand-gesture-drone-controller-default-rtdb.asia-southeast1.firebasedatabase.app/"})

# Reference to the "instructions" node in the database
ref = db.reference('/')

while True:
   try:
      data = ref.get()
      last_key = list(data.keys())[-1]
      last_element = data[last_key]
      instruction_value = last_element.get('instruction', '')
      if instruction_value == "Take Off" and TakeOff == False:
         TakeOff = True
         arm_and_takeoff(3)
      elif instruction_value == "Take Off" and TakeOff == True:
         send_body_ned_velocity(0,0,2,5)
      elif instruction_value == "Backward":
         send_body_ned_velocity(-2,0,0,5)
      elif instruction_value == "Forward":
         send_body_ned_velocity(2,0,0,5)
      elif instruction_value == "Left":
         send_body_ned_velocity(0,-2,0,5)
      elif instruction_value == "Right":
         send_body_ned_velocity(0,2,0,5)
      elif instruction_value == "Hover":
         send_body_ned_velocity(0,0,0,5)   
      elif instruction_value == "Stop":
         land_and_disarm()
         break
      print(instruction_value)
      time.sleep(2)


   except KeyboardInterrupt:
      print("Program terminated by user.")
      break