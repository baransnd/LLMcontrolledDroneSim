
import time
from turtle import speed
import airsim
import math
import random
import numpy as np
from Controller.DroneController.AirsimAdapter.object_detector import ObjectDetectionAPI4AI
from Controller.DroneController.AirsimAdapter.drone_surveyor import *
from PySide6.QtCore import Signal, QObject, QMetaObject, Qt, Q_ARG, Slot
from Controller.DroneController.Utils.message import Roles
from Controller.DroneController.Utils.message import Message
from types import SimpleNamespace
import keyboard


class AirsimAdapter(QObject):
    display_signal = Signal(Message)

    def __init__(self, view_controller, drone_surveyor):
        super().__init__()
        self.client = airsim.MultirotorClient()
        self.client.confirmConnection()
        self.view_controller = view_controller
        self.drone_surveyor = drone_surveyor
        self.display_signal.connect(self.view_controller.display)       # Kolin: show the answers of the methods on the UI
      
    def list_drones(self):
        drone_list = self.client.listVehicles()
        message = f"Current drone list: {drone_list}"
        self.display_signal.emit(Message(Roles.SYSTEM, message))        
        print(message) 
        return drone_list
 
    
    """
    @Kolin: Adds a drone to the unreal environment with random coordinates.
    """
    def add_drone(self, drone_name):

        drone_list = self.client.listVehicles()
        if len(drone_list) > 5:                                 # Kolin: Limit the drone number.
            message = f"There are already 6 drones, add drone failed."
            self.display_signal.emit(Message(Roles.SYSTEM, message))            
            print(message)
            return

        # If no name was given, call it DroneX with X being the new number of drones
        if drone_name == False or drone_name == None:
            drone_count = self.drone_surveyor.drones_count                               
            drone_count += 1                                    # Kolin: Increment drone_count , works better this way.                           
            drone_name = "Drone" + str(drone_count)             # Kolin: '_' deleted, as too many methods use default name 'Drone1'...


        if drone_name not in drone_list:
            self.client.simAddVehicle(vehicle_name=drone_name, vehicle_type="simpleflight", pose=airsim.Pose())          
            pos_x = random.uniform(-240, 240)
            pos_y = random.uniform(-240, 240)
            self.set_position([pos_x, pos_y, 0], 0, drone_name)        # Kolin: Add drones to random position.
            self.client.armDisarm(True, vehicle_name=drone_name)

            self.view_controller.add_drone_to_ui(drone_name)

            current_gps = self.get_drone_geopoint(drone_name)
            message = f"{drone_name} added on gps: {current_gps}"
            self.display_signal.emit(Message(Roles.SYSTEM, message))
            self.list_drones()
            print(message)
            
            self.drone_surveyor.drones_count += 1
            

    """
    @Kolin: Adds multiple drones with the specified number of drones.
    """
    def add_multiple_drones(self, drones_count):
        for i in range(drones_count):
            self.add_drone(None)
        
        
    """
    @Kolin: Adds a drone to the unreal environment with random coordinates.
    """
    def switch_to_camera(self, drone_name='Drone1'):
        self.view_controller.image_update_worker.current_drone_name = drone_name
        
        message = f"Switched camera to: {drone_name}"
        self.display_signal.emit(Message(Roles.SYSTEM, message))
        print(message)
        

        

    """
    @Isik: Adds a Person to the unreal environment in the specified coordinates
    """
    def add_person(self, pos_x = 0, pos_y = 0, pos_z = 0):
         # Calculate the Euclidean distance from the origin to the given point
        distance = math.sqrt(pos_x**2 + pos_y**2)
        scale = 1
        dir = 0
            
        # Check if the distance is within the 250 meters limit
        if distance > 250:
            message = f"The point ({pos_x}, {pos_y}, {pos_z}) is more than 250 meters away from the origin. Distance: {distance} meters."
            self.display_signal.emit(Message(Roles.SYSTEM, message))  # Show the result on the UI
            print(message)
            return False
            
        object_name = "Person"
        asset_name = "Person"     # Name of the asset (mesh) in the project database
        spawn_pose = airsim.Pose(airsim.Vector3r(pos_x, pos_y, pos_z), airsim.to_quaternion(dir, dir, dir))  # Desired pose of the object
        scale = airsim.Vector3r(scale, scale, scale)  # Desired scale of the object (1, 1, 1 means original scale)
        physics_enabled = True         # Enable physics for the object
        is_blueprint = False           # Whether the object is a blueprint or an actor
        spawned_object_name = self.client.simSpawnObject(object_name, asset_name, spawn_pose, scale, physics_enabled, is_blueprint)
        if spawned_object_name:
            message ="Successfully spawned object '{spawned_object_name}' in the environment."
            self.display_signal.emit(Message(Roles.SYSTEM, message))        
            print(message)  
            
        else:
            message = "Failed to spawn object '{object_name}' in the environment."
            self.display_signal.emit(Message(Roles.SYSTEM, message))        
            print(message)  

            
    """
    @Isik: Adds a Person to the unreal environment at a random position within a 500x500 square centered at (0,0,0)
    """
    def add_person_random(self):
        try:
            
            pos_x = random.uniform(-250, 250)
            pos_y = random.uniform(-250, 250)
            pos_z = 0  # Set z to ground level (needs testing)

            
            object_name = "Person"
            asset_name = "Person"  # Ensure this matches the name of the asset in the Unreal Engine project
            spawn_pose = airsim.Pose(airsim.Vector3r(pos_x, pos_y, pos_z), airsim.to_quaternion(0, 0, 0)) 
            scale = airsim.Vector3r(1, 1, 1)  
            physics_enabled = True  
            is_blueprint = False  

            # Attempt to spawn the object in the environment
            spawned_object_name = self.client.simSpawnObject(object_name, asset_name, spawn_pose, scale, physics_enabled, is_blueprint)

            
            if spawned_object_name:
                message = f"Successfully spawned object '{spawned_object_name}' at ({pos_x}, {pos_y}, {pos_z})"
                self.display_signal.emit(Message(Roles.SYSTEM, message)) 
                print(message)
                return True
            else:
                message = f"Failed to spawn object '{object_name}' at ({pos_x}, {pos_y}, {pos_z})"
                self.display_signal.emit(Message(Roles.SYSTEM, message))  
                print(message)
                return False

        except Exception as e:
            # Handle any exceptions that occur
            error_message = f"An error occurred while spawning the object: {e}"
            self.display_signal.emit(Message(Roles.SYSTEM, error_message))  
            print(error_message)
            return False


    """
    @Isik: Deletes the object that was created with the given name.
    """    
    def delete_object(self, object_name):
        try:
            result = self.client.simDestroyObject(object_name)
            if result:
                message = f"Successfully deleted object '{object_name}' in the environment."
                self.display_signal.emit(Message(Roles.SYSTEM, message)) 
                print(message)
            else:
                message = f"Failed to delete object '{object_name}' in the environment."
                self.display_signal.emit(Message(Roles.SYSTEM, message))  
                print(message)
        except Exception as e:
            message = f"An error occurred while trying to delete object '{object_name}': {e}"
            self.display_signal.emit(Message(Roles.SYSTEM, message)) 
            print(message)

        
    def takeoff(self, drone_name='Drone1'):
        self.client.enableApiControl(True, vehicle_name=drone_name)
        message = f"{drone_name} taking off..."
        self.display_signal.emit(Message(Roles.SYSTEM, message))        # Kolin: Show the result on the UI.
        print(message)        

        self.client.takeoffAsync(vehicle_name=drone_name).join()

    def land(self, drone_name='Drone1'):
        self.client.enableApiControl(True, vehicle_name=drone_name)
        message = f"{drone_name} landing..."
        self.display_signal.emit(Message(Roles.SYSTEM, message))        # Kolin: Show the result on the UI.
        print(message) 
        
        self.client.landAsync(vehicle_name=drone_name).join()      

    
    """
    @Kolin: Get the xyz coordinate of a drone.

    """  
    def get_drone_position(self, drone_name='Drone1'):
        pose = self.client.simGetVehiclePose(vehicle_name=drone_name)
        coordinate = [pose.position.x_val, pose.position.y_val, pose.position.z_val]

        return coordinate

    
    """
    @Kolin: Get the GPS of the drone. Help-method.

    """  
    def get_drone_geopoint(self, drone_name='Drone1'):
        gps_data = self.client.getGpsData(vehicle_name=drone_name)
        latitude = gps_data.gnss.geo_point.latitude
        longitude = gps_data.gnss.geo_point.longitude
        altitude = gps_data.gnss.geo_point.altitude
        
        drone_geopoint = airsim.GeoPoint()
        drone_geopoint.latitude = latitude
        drone_geopoint.longitude = longitude
        drone_geopoint.altitude = altitude

        return drone_geopoint

    
    """
    @Kolin: Display the content or answer from the Server on the UI.

    """  
    def display_content_from_server(self, content):
        self.display_signal.emit(Message(Roles.ASSISTANT, content))       
        

    """
    @Kolin: Asynchron fly method based on xyz coordinate system.

    """    
    def fly_to_xyz_asnychron(self, point, drone_name='Drone1', speed=5): # @Teo: fix asnych typo
        self.client.enableApiControl(True, vehicle_name=drone_name)       
        
        self.client.moveToPositionAsync(point[0], point[1], point[2], speed, vehicle_name=drone_name)

    
    """
    @Kolin: The basic method for the flying in the xyz coordinate system. Adjusted the original method from chatgpt_airsim, the original had issues.

    """    
    def fly_to_xyz(self, point, drone_name='Drone1', speed=5):
        self.client.enableApiControl(True, vehicle_name=drone_name)
        
        start_pos = self.get_drone_position(drone_name)
        target_pos = point
        yaw_degrees = self.calculate_yaw_angle_with_pos(start_pos, target_pos)
        self.set_yaw(yaw_degrees, drone_name)
        
        message = f"{drone_name} Moving to xyz Coordinate: x: {point[0]}, y: {point[1]}, z: {point[2]}"
        self.display_signal.emit(Message(Roles.SYSTEM, message))        # Kolin: Show the result on the UI.
        print(message)
        
        self.client.moveToPositionAsync(point[0], point[1], point[2], speed, vehicle_name=drone_name).join()
 
   
    """
    @Kolin: The basic method for the flying in the GPS coordinate system.

    """           
    def fly_to_geopoint(self, end_geo, drone_name='Drone1', speed=5):
        self.client.enableApiControl(True, vehicle_name=drone_name)
        
        drone_geopoint = self.get_drone_geopoint(drone_name)       
        yaw_degrees = self.calculate_yaw_angle_with_gps(drone_geopoint, end_geo)
        self.set_yaw(yaw_degrees, drone_name)
       
        message = f"{drone_name} Moving to GPS: Latitude: {end_geo.latitude}, Longitude: {end_geo.longitude}, Altitude: {end_geo.altitude}"
        self.display_signal.emit(Message(Roles.SYSTEM, message))        # Kolin: Show the result on the UI.
        print(message)
        
        self.client.moveToGPSAsync(end_geo.latitude, end_geo.longitude, end_geo.altitude, speed, vehicle_name=drone_name).join()
               

    """
    @Kolin: The basic method for the flying along a path in the xyz coordinate system.

    """   
    def fly_path_xyz(self, path_xyz, drone_name='Drone1', speed=5):
        for xyz_point in path_xyz:
            self.fly_to_xyz(xyz_point, drone_name, speed)
            
    """
    @Kolin: The basic method for the flying along a path in the gps coordinate system.

    """   
    def fly_path_gps(self, path_gps, drone_name='Drone1', speed=5):
        for gps_point in path_gps:
            self.fly_to_geopoint(gps_point, drone_name, speed)

 
    """
    @Kolin: Method to change the location of a specified drone.

    """        
    def set_position(self, point, yaw=0, drone_name='Drone1'):
        self.client.enableApiControl(True, vehicle_name=drone_name)
        
        pose = airsim.Pose(airsim.Vector3r(point[0], point[1], point[2]), airsim.to_quaternion(0, 0, math.radians(yaw)))
        self.client.simSetVehiclePose(pose, True, vehicle_name=drone_name)
        
        time.sleep(1.5)
        self.client.moveToPositionAsync(point[0], point[1], point[2], 5, vehicle_name=drone_name)

    """
    @Kolin: Set yaw of the drone, asynchronous.

    """     
    def set_yaw_asynchron(self, yaw_degrees, drone_name='Drone1', speed=5):
        self.client.rotateToYawAsync(yaw_degrees, speed, vehicle_name=drone_name)

    """
    @Kolin: Set yaw of the drone.

    """     
    def set_yaw(self, yaw_degrees, drone_name='Drone1', speed=5):
        self.client.rotateToYawAsync(yaw_degrees, speed, vehicle_name=drone_name).join()
        self.display_signal.emit(Message(Roles.SYSTEM, f"{drone_name} Change Yaw to: {yaw_degrees} degrees to the east."))       


    def get_yaw(self, drone_name='Drone1'):
        orientation_quat = self.client.simGetVehiclePose(vehicle_name=drone_name).orientation
        yaw_radians  = airsim.to_eularian_angles(orientation_quat)[2]
        yaw_degrees = math.degrees(yaw_radians)
        
        return yaw_degrees
    
    """
    @Kolin: Method to take a picture and show the result on the UI

    """        
    def take_photo(self, drone_name='Drone1'):
        object_detector = ObjectDetectionAPI4AI(self.client, api_mode='demo', rapidapi_key='a73564f61cmsh64e5459995ac69fp12616cjsn49a349a54798')
        object_detector.get_and_save_camera_image(drone_name)
        self.display_signal.emit(Message(Roles.SYSTEM, r"A Photo is made, go to Controller\DroneController\AirsimAdapter\Pictures from Camera\current_scene.png to check the picture."))
        #QMetaObject.invokeMethod(self.view_controller.openai_communicate_worker, "ask", Qt.QueuedConnection, Q_ARG(str, "System message: take photo completed."))
        

    """
    @Isik: Method for a drone to follow another drone with the given distance for the given duration. I found 5 meters to be a good distance
           for collision avoidance.
    """
    def follow_drone(self, follower_drone_name, followed_drone_name, follow_distance=7.0,follow_duration=60):

        # Enable API control and arm both drones
        self.client.enableApiControl(True, follower_drone_name)
        self.client.armDisarm(True, follower_drone_name)
            
        # Track the start time
        start_time = time.time()


        while time.time() - start_time < follow_duration:
            # Retrieve the current position of the followed drone
            followed_drone_pose = self.client.simGetVehiclePose(vehicle_name=followed_drone_name)


            if followed_drone_pose:
                target_x = followed_drone_pose.position.x_val
                target_y = followed_drone_pose.position.y_val
                target_z = followed_drone_pose.position.z_val

                    
                follower_drone_pose = self.client.simGetVehiclePose(vehicle_name=follower_drone_name)
                distance = self.get_distance(follower_drone_pose.position, followed_drone_pose.position)
                if distance > follow_distance:
                    # Calculate the direction vector from the follower drone to the followed drone
                    direction_vector = airsim.Vector3r(
                        target_x - follower_drone_pose.position.x_val,
                        target_y - follower_drone_pose.position.y_val,
                        target_z - follower_drone_pose.position.z_val
                    )

                    # Normalize the direction vector
                    length = (direction_vector.x_val**2 + direction_vector.y_val**2 + direction_vector.z_val**2)**0.5
                    direction_vector = airsim.Vector3r(
                        direction_vector.x_val / length,
                        direction_vector.y_val / length,
                        direction_vector.z_val / length
                    )

                    target_x = follower_drone_pose.position.x_val + direction_vector.x_val * follow_distance
                    target_y = follower_drone_pose.position.y_val + direction_vector.y_val * follow_distance
                    target_z = follower_drone_pose.position.z_val + direction_vector.z_val * follow_distance

                    # Kolin: i recommand to use the methode from ourselfs. The follower drone clipped on the followed drone and so the followed cant move anyway.
                    # i use a calculate_xyz_with_direction_and_distance from ourself here to give it an offset. Check the function behinde for more details.
                    start_pos = self.get_drone_position(followed_drone_name)
                    end_pos = self.get_drone_position(follower_drone_name)
                    destination_pos = self.calculate_xyz_with_direction_and_distance(end_pos, 5, 0, start_pos)     # Kolin: this should be the destination for the follower drone.

                    self.client.moveToPositionAsync(destination_pos[0], destination_pos[1], destination_pos[2], 3, vehicle_name=follower_drone_name)
                    print(f"Moving {follower_drone_name} to position ({destination_pos[0]}, {destination_pos[1]}, {destination_pos[2]}) to follow {followed_drone_name}")
                else:
                    pass
                    #message = f"We are close to: {followed_drone_name}"    # Kolin: temporaly filterd it out. Too many feedbacks on console.
                    #self.display_signal.emit(Message(Roles.SYSTEM, message))
            # Add a short delay to avoid overwhelming the simulator
            time.sleep(0.1)

        message = f"followed {followed_drone_name} for {follow_duration} seconds"
        print(message)
        self.display_signal.emit(Message(Roles.SYSTEM, message))
            
            

    """
    @Isik: Calculate distance.
    """
    def get_distance(self, position1, position2):
        return math.dist(position1, position2)


    
    """
    @Kolin: Calculate the target gps with xyz system.
            Warning: The unreal gps system, where lon means north and lat means lat, is totally inverted to the real world....

    """              
    def calculate_new_geo_point(self, start_geo, north_meters=0, east_meters=0, up_meters=0):
        meters_per_deg_lat = 111320
        meters_per_deg_lon = 40075000 * math.cos(math.radians(start_geo.latitude)) / 360
    
        delta_lat = east_meters / meters_per_deg_lat
        delta_lon = north_meters / meters_per_deg_lon
        delta_alt = up_meters
        
        new_geopoint = airsim.GeoPoint()
        new_geopoint.latitude = start_geo.latitude + delta_lat
        new_geopoint.longitude = start_geo.longitude - delta_lon
        new_geopoint.altitude = start_geo.altitude + delta_alt
        
        return new_geopoint
    

    """
    @Kolin: Calculate the from gps difference in GPS system to xy difference in xyz system.

    """              
    def calculate_deltas_in_meters(self, start_lat, start_lon, end_lat, end_lon):
        # Umrechnungsfaktor von Grad zu Metern für die Breite
        meters_per_degree_lat = -102101.66220559966869162283333511  # Ein Grad Breite entspricht etwa 111 km
        meters_per_degree_lon = 65823.979912113609737449300568569

        # Delta-Berechnungen in Metern
        delta_y = (end_lat - start_lat) * meters_per_degree_lat
        delta_x = (end_lon - start_lon) * meters_per_degree_lon

        return delta_x, delta_y

 
    """
    @Kolin: Calculate the angle betweens 2 gps points.

    """      
    def calculate_yaw_angle_with_gps(self, start_geo, end_geo):
        # Convert latitude and longitude from degrees to radians
        lat1 = math.radians(start_geo.latitude)
        lon1 = math.radians(start_geo.longitude)
        lat2 = math.radians(end_geo.latitude)
        lon2 = math.radians(end_geo.longitude)

        # Calculate the difference in longitude
        delta_lon = lon2 - lon1

        # Calculate the x and y components
        x = math.sin(delta_lon) * math.cos(lat2)
        y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(delta_lon))

        # Calculate the initial bearing
        yaw_radians = math.atan2(x, y)

        # Convert bearing from radians to degrees
        yaw_degrees = math.degrees(yaw_radians)
        yaw_degrees = (yaw_degrees + 360) % 360  # Normalize to 0-360 degrees

        return yaw_degrees

    """
    @Kolin: Calculate the angle betweens 2 xyz coordinates.

    """    
    def calculate_yaw_angle_with_pos(self, start_pos, target_pos):
        delta_x = target_pos[0] - start_pos[0]
        delta_y = target_pos[1] - start_pos[1]
        yaw_radians = math.atan2(delta_y, delta_x)
        yaw_degrees = math.degrees(yaw_radians)
        yaw_degrees = (yaw_degrees + 360) % 360  # Normalize to 0-360 degrees    
        
        return yaw_degrees
    

    """
    @Kolin: Calculate sub-search area and return it.

    """    
    def divide_into_subareas(self):
         try:
             self.drone_surveyor.set_start_gps(self.get_drone_geopoint("Drone1"))       # Kolin: the position of the default drone defines the search area.
             starting_gps = self.drone_surveyor.start_gps
             corner_gps_list = []
             drone_count = len(self.list_drones())

             # If there's only one drone, the entire area is covered by the starting point.
             if drone_count == 1:
                 corner_gps = self.calculate_new_geo_point(starting_gps, north_meters=250, east_meters=-250)
                 corner_gps_list.append(corner_gps)

             # If there are two drones, divide the area into two horizontal rectangles.
             elif drone_count == 2:
                 corner_gps_upper = self.calculate_new_geo_point(starting_gps, north_meters=250, east_meters=-250)
                 corner_gps_lower = self.calculate_new_geo_point(starting_gps, north_meters=0, east_meters=-250)
                 corner_gps_list.extend([corner_gps_upper, corner_gps_lower])

             # If there are three drones, divide the area into three horizontal rectangles.
             elif drone_count == 3:
                 offset = 500 / 3
                 corner_gps_upper = self.calculate_new_geo_point(starting_gps, north_meters=250, east_meters=-250)
                 corner_gps_middle = self.calculate_new_geo_point(starting_gps, north_meters=250 - offset, east_meters=-250)
                 corner_gps_lower = self.calculate_new_geo_point(starting_gps, north_meters=250 - (2 * offset), east_meters=-250)
                 corner_gps_list.extend([corner_gps_upper, corner_gps_middle, corner_gps_lower])

             elif drone_count == 4:
                 # Calculate middle points for each quadrant
                 corner_gps_top_left = self.calculate_new_geo_point(starting_gps, north_meters=250, east_meters=-250)
                 corner_gps_top_right = self.calculate_new_geo_point(starting_gps, north_meters=250, east_meters=0)
                 corner_gps_bottom_left = self.calculate_new_geo_point(starting_gps, north_meters=0, east_meters=-250)
                 corner_gps_bottom_right = self.calculate_new_geo_point(starting_gps, north_meters=0, east_meters=0)
                 corner_gps_list.extend([corner_gps_top_left, corner_gps_top_right, corner_gps_bottom_left, corner_gps_bottom_right])

             elif drone_count == 5:
                 # Calculate middle points for each quadrant
                 corner_gps_first_rectangle = self.calculate_new_geo_point(starting_gps, north_meters=250, east_meters=-250)
                 corner_gps_second_rectangle = self.calculate_new_geo_point(starting_gps, north_meters=150, east_meters=-250)
                 corner_gps_third_rectangle = self.calculate_new_geo_point(starting_gps, north_meters=50, east_meters=-250)
                 corner_gps_fourth_rectangle = self.calculate_new_geo_point(starting_gps, north_meters=-50, east_meters=-250)
                 corner_gps_fifth_rectangle = self.calculate_new_geo_point(starting_gps, north_meters=-150, east_meters=-250)
                 corner_gps_list.extend(corner_gps_first_rectangle, corner_gps_second_rectangle, corner_gps_third_rectangle, corner_gps_fourth_rectangle, corner_gps_fifth_rectangle)

             elif drone_count == 6:
                 offset = 500 / 3
                 # Calculate middle points for each quadrant
                 corner_gps_top_left = self.calculate_new_geo_point(starting_gps, north_meters=250, east_meters=-250)
                 corner_gps_top_right = self.calculate_new_geo_point(starting_gps, north_meters=250, east_meters=0)
                 corner_gps_middle_left = self.calculate_new_geo_point(starting_gps, north_meters=250 - offset, east_meters=-250)
                 corner_gps_middle_right = self.calculate_new_geo_point(starting_gps, north_meters=250 - offset, east_meters=0)
                 corner_gps_bottom_left = self.calculate_new_geo_point(starting_gps, north_meters=250 - (offset * 2), east_meters=-250)
                 corner_gps_bottom_right = self.calculate_new_geo_point(starting_gps, north_meters=250 - (offset * 2), east_meters=0)
                 corner_gps_list.extend([corner_gps_top_left, corner_gps_top_right, corner_gps_middle_left, corner_gps_middle_right, corner_gps_bottom_left, corner_gps_bottom_right])
                 

             return corner_gps_list

         except Exception as e:
             print(f"An error occurred while dividing into subareas: {e}")
             return []
         

    """
    @Kolin: Move all the drones to their search position and prepare for searching.

    """    
    def all_drones_get_in_search_position(self, speed=20):
        try:
            all_in_position = False
            drones_and_their_reach_corner_results = SimpleNamespace()
            drone_list = self.list_drones()
            top_left_corners_of_their_searching_area = self.divide_into_subareas()
        
            for drone, top_left_gps in zip(drone_list, top_left_corners_of_their_searching_area):
                self.client.enableApiControl(True, vehicle_name=drone)
                setattr(drones_and_their_reach_corner_results, drone, False)          # Kolin: mark the drones, whether are they already in destinaition or not.
 
                if self.detect_collisions(top_left_gps, drone):
                    # Kolin: if collision detected, send it to chatGPT to avoid this collision.
                    #QMetaObject.invokeMethod(self.view_controller.openai_communicate_worker, "ask", Qt.QueuedConnection, Q_ARG(str, f"Collision detected for the {drone}, use the collision_avoidance_calculation function with destination gps: {top_left_gps} in speed {speed}."))
                    self.collision_avoidance_calculation(top_left_gps, drone, speed)
                else:
                    # Kolin: asynchron movement.
                    self.client.moveToGPSAsync(top_left_gps.latitude, top_left_gps.longitude, top_left_gps.altitude, speed, vehicle_name=drone)
                    
                    message = f"moving {drone}, to {top_left_gps}..."
                    self.display_signal.emit(Message(Roles.SYSTEM, message))
                    print(message)
                    
            while not all_in_position:                              # Kolin: report the drone, if it get it position.
                for drone, top_left_gps in zip(drone_list, top_left_corners_of_their_searching_area):
                    current_gps = self.get_drone_geopoint(drone)
                    delta_x, delta_y = self.calculate_deltas_in_meters(current_gps.longitude, current_gps.latitude, top_left_gps.longitude, top_left_gps.latitude)
                    
                    if (-20 < delta_x < 20) and (-20 < delta_y < 20):
                        if getattr(drones_and_their_reach_corner_results, drone) != True:
                            setattr(drones_and_their_reach_corner_results, drone, True)
                            message = f"{drone}: get in position and prepare for search!!"
                            self.display_signal.emit(Message(Roles.SYSTEM, message))
                            print(message)
                        
                false_count = sum(1 for value in drones_and_their_reach_corner_results.__dict__.values() if value is False)  # Kolin: count how much False.
                if false_count == 0:
                    all_in_position = True
                    
                time.sleep(2)
                
            if all_in_position:
                message = f"All drones are in position for searching!!"
                self.display_signal.emit(Message(Roles.SYSTEM, message))
                print(message)

                    
        except Exception as e:
            print(f"An error occurred during moving to survey area: {e}")     
          
            
    """
    @Kolin: Fly a drone to the target position with collision avoidance and get_in_position report.

    """    
    @Slot('QVariantList', str)
    def fly_to_xyz_with_collision_avoidance_and_get_in_position_report(self, target_position, drone_name='Drone1', speed=30):
        in_position = False
        start_gps = self.view_controller.unreal_start_geopoint
        target_gps = self.calculate_new_geo_point(start_gps, -target_position[1], target_position[0])
 
        if self.detect_collisions(target_gps, drone_name):
            # Kolin: if collision detected, send it to chatGPT to avoid this collision.
            self.collision_avoidance_calculation(target_gps, drone_name)
        else:
            self.fly_to_xyz(target_position, drone_name, speed)
                    
        while not in_position:                              # Kolin: report the drone, if it get it position.
            current_gps = self.get_drone_geopoint(drone_name)
            delta_x, delta_y = self.calculate_deltas_in_meters(current_gps.longitude, current_gps.latitude, target_gps.longitude, target_gps.latitude)

            if (-20 < delta_x < 20) and (-20 < delta_y < 20):
                message = f"{drone_name}: get in new position!!"
                self.display_signal.emit(Message(Roles.SYSTEM, message))
                print(message)

                self.drone_surveyor.drones_arrives_count += 1
                in_position = True
                
            time.sleep(2)

    """
    @Kolin: Fly a drone to the target gps with collision avoidance and get_in_position report.

    """    
    def fly_to_gps_with_collision_avoidance_and_get_in_position_report(self, target_gps, drone_name='Drone1', speed=30):
        in_position = False
 
        if self.detect_collisions(target_gps, drone_name):
            # Kolin: if collision detected, send it to chatGPT to avoid this collision.
            self.collision_avoidance_calculation(target_gps, drone_name)
        else:
            self.fly_to_geopoint(target_gps, drone_name, speed)
                    
        while not in_position:                              # Kolin: report the drone, if it get it position.
            current_gps = self.get_drone_geopoint(drone_name)
            delta_x, delta_y = self.calculate_deltas_in_meters(current_gps.longitude, current_gps.latitude, target_gps.longitude, target_gps.latitude)

            if (-20 < delta_x < 20) and (-20 < delta_y < 20):
                message = f"{drone_name}: get in new position!!"
                self.display_signal.emit(Message(Roles.SYSTEM, message))
                print(message)

                self.drone_surveyor.drones_arrives_count += 1
                in_position = True
                
            time.sleep(2)



    """
    @Kolin: Move all the drones to their new search area.

    """    
    @Slot('QVariantList')
    def all_drones_move_to_new_search_area(self, new_position, speed=30):
        all_in_position = False
        drones_and_get_in_position_results = SimpleNamespace()
        drone_list = self.list_drones()
        start_gps = self.view_controller.unreal_start_geopoint
            
        # Kolin: this is a ring formation for the drone to the new search area.
        drone_gps_ring = {
            self.calculate_new_geo_point(start_gps, -new_position[1], new_position[0] + 20),        # Kolin: Cautious! positiv y means negativ north!
            self.calculate_new_geo_point(start_gps, -new_position[1] + 10, new_position[0] + 10),
            self.calculate_new_geo_point(start_gps, -new_position[1] + 10, new_position[0] - 10),
            self.calculate_new_geo_point(start_gps, -new_position[1] - 10, new_position[0] + 10),
            self.calculate_new_geo_point(start_gps, -new_position[1] - 10, new_position[0] - 10),
            self.calculate_new_geo_point(start_gps, -new_position[1], new_position[0] - 20)
        }
        
        for drone, gps in zip(drone_list, drone_gps_ring):
            self.client.enableApiControl(True, vehicle_name=drone)
            setattr(drones_and_get_in_position_results, drone, False)          # Kolin: mark the drones, whether are they already in destinaition or not.
 
            if self.detect_collisions(gps, drone):
                # Kolin: if collision detected, send it to chatGPT to avoid this collision.
                #QMetaObject.invokeMethod(self.view_controller.openai_communicate_worker, "ask", Qt.QueuedConnection, Q_ARG(str, f"Collision detected for the {drone}, use the collision_avoidance_calculation function with destination gps: {gps} in speed {speed}."))
                self.collision_avoidance_calculation(gps, drone)
            else:
                # Kolin: asynchron movement.
                self.client.moveToGPSAsync(gps.latitude, gps.longitude, gps.altitude, speed, vehicle_name=drone)
                    
                message = f"moving {drone}, to {gps}..."
                self.display_signal.emit(Message(Roles.SYSTEM, message))
                print(message)
                    
        while not all_in_position:                              # Kolin: report the drone, if it get it position.
            for drone, distination_gps in zip(drone_list, drone_gps_ring):
                current_gps = self.get_drone_geopoint(drone)
                delta_x, delta_y = self.calculate_deltas_in_meters(current_gps.longitude, current_gps.latitude, distination_gps.longitude, distination_gps.latitude)
                    
                if (-20 < delta_x < 20) and (-20 < delta_y < 20):
                    if getattr(drones_and_get_in_position_results, drone) != True:
                        setattr(drones_and_get_in_position_results, drone, True)
                        message = f"{drone}: get in new position!!"
                        self.display_signal.emit(Message(Roles.SYSTEM, message))
                        print(message)
                        
            false_count = sum(1 for value in drones_and_get_in_position_results.__dict__.values() if value is False)  # Kolin: count how much False.
            if false_count == 0:
                all_in_position = True
                    
            time.sleep(2)
                
        if all_in_position:
            message = f"All drones are in position in new search area!!"
            self.display_signal.emit(Message(Roles.SYSTEM, message))
            print(message)
                    



    """
    @Kolin: Survey pattern zik-zak.

    """       
    def zik_zak_survey(self, drone_name='Drone1',length=60, width=30, strip_width=6, speed=10):
        self.reset_survey_counter(drone_name)

        message = "Starting lawnmower pattern survey..."
        print(message)
        self.display_signal.emit(Message(Roles.SYSTEM, message))        # Kolin: show the massage on the UI.

        current_geoponit = self.get_drone_geopoint(drone_name)          # Kolin: use geopoint instead of using Position xyz.
                
        if drone_name == "Drone1":
            strips_count = self.drone_surveyor.strips_count_drone_1     # Kolin: load the strip count from drone_surveyor
        elif drone_name == "Drone2":
            strips_count = self.drone_surveyor.strips_count_drone_2
        elif drone_name == "Drone3":
            strips_count = self.drone_surveyor.strips_count_drone_3
        elif drone_name == "Drone4":
            strips_count = self.drone_surveyor.strips_count_drone_4
        elif drone_name == "Drone5":
            strips_count = self.drone_surveyor.strips_count_drone_5
        elif drone_name == "Drone6":
            strips_count = self.drone_surveyor.strips_count_drone_6
                
        while strips_count < (width / strip_width):                               
                    
            if strips_count % 2 == 0:  # Even strip, move right
                target_geopoint = self.calculate_new_geo_point(current_geoponit, north_meters=-strip_width, east_meters=length) # Kolin: calculate the geopoints of the target position for single trip.

            else:  # Odd strip, move left
                target_geopoint = self.calculate_new_geo_point(current_geoponit, north_meters=-strip_width, east_meters=-length) 

            message = f"{drone_name} reciving person detection analyse data from Server..."
            print(message)
            self.display_signal.emit(Message(Roles.SYSTEM, message))        # Kolin: show the massage on the UI.

            # Kolin: if the person ist found
            if self.drone_surveyor.person_detected and drone_name in self.drone_surveyor.person_found_by_drone_list:
                message = f"**********The person is found by {drone_name}!!! {drone_name} Moving to his position...**********"
                print(message)
                self.display_signal.emit(Message(Roles.SYSTEM, message))        # Kolin: show the massage on the UI.

                person_location = self.drone_surveyor.person_location
                drone_location = self.get_drone_position(drone_name)
                person_location = self.calculate_xyz_with_direction_and_distance(person_location, 15, direction_or_destination=drone_location)      # Kolin: move the destination 10 meters before the person and not punch directly the person.
                    
                delta_x = person_location[0] - drone_location[0]
                delta_y = person_location[1] - drone_location[1]
                delta_z = drone_location[2] - person_location[2]            # Kolin: Warning: The height in xyz is inverted.
                    
                drone_gps = self.get_drone_geopoint(drone_name)             # Kolin: Change to gps system to detect collision.
                person_gps = self.calculate_new_geo_point(drone_gps, delta_y, delta_x, delta_z)
                    
                if self.detect_collisions(person_gps, drone_name):          # Kolin: If the way to the person has collision.
                    # Kolin: If there is a collision, then avoid it.
                    message = f"calculating a path to avoid the collision for {drone_name}.."
                    print(message)
                    self.display_signal.emit(Message(Roles.SYSTEM, message))        # Kolin: show the massage on the UI.

                    self.collision_avoidance_calculation(person_gps, drone_name)
                    self.reset_survey_counter()
                else:
                    self.fly_to_xyz(person_location, drone_name)
                        
                        
                message ="Hura!!"
                print(message)
                self.display_signal.emit(Message(Roles.SYSTEM, message))        # Kolin: show the massage on the UI.
                break  
            
            elif self.drone_surveyor.person_detected:
                message =f"Search report from {drone_name}: the person is found by other drones, stop searching and stay in position for further orders."
                print(message)
                self.display_signal.emit(Message(Roles.SYSTEM, message))        # Kolin: show the massage on the UI.
                break
                
            if self.detect_collisions(target_geopoint, drone_name):
                # Kolin: If there is a collision, then send a calculate request.
                message = f"{drone_name} Asking openAI to calculate a path to avoid the collision.."
                print(message)
                self.display_signal.emit(Message(Roles.SYSTEM, message))        # Kolin: show the massage on the UI.
                    
                #QMetaObject.invokeMethod(self.view_controller.openai_communicate_worker, "ask", Qt.QueuedConnection, Q_ARG(str, f"Collision detected for the {drone_name}, use the collision_avoidance_calculation function with destination gps: {target_geopoint}, and then continue survey in a area {length} meters length, {width} meters width with a Strip width {strip_width} meters in a speed {speed}."))
                self.collision_avoidance_calculation(target_geopoint, drone_name)        # Kolin: canceled the communication between funktions and OpenAI. Use self written collision avoidance.
                #break
            else:                    
                self.fly_to_geopoint(target_geopoint, drone_name, speed)    # Kolin: fly to target position an start the next sptrip..
                strips_count = self.drone_surveyor.count(drone_name)        # Kolin: Update the stips count of this drone.
                current_geoponit = target_geopoint
                             

            
    """
    @Kolin: Detect a collision between the drone itself and the target gps and send back the report.

    """   
    def detect_collisions(self, end_geo, drone_name='Drone1'):
        # Test line of sight
        result = self.client.simTestLineOfSightToPoint(end_geo, drone_name)
        if not result:
            message = f"Collision detected in the path from {drone_name}!"
            self.display_signal.emit(Message(Roles.SYSTEM, message))        # Kolin: show the result on the UI. True means collision detected.
            print(message)
            return True                                                     # Kolin: True means collision detected.
        else:
            message = f"No Collision detected from {drone_name}."
            self.display_signal.emit(Message(Roles.SYSTEM, message))        # Kolin: show the result on the UI. False means no collision.
            print(message)            
            return False

    """
    @Kolin: Detect a collision between the drone itself and the target gps without any report.

    """   
    def detect_collisions_without_report(self, end_geo, drone_name='Drone1'):
        # Test line of sight
        result = self.client.simTestLineOfSightToPoint(end_geo, drone_name)
        if not result:
            return True                                                     # Kolin: True means collision detected.
        else:         
            return False
        

    """
    @Kolin: Calculate a path to avoid the collision for a drone.

    """   
    def collision_avoidance_calculation(self, end_geopoint, drone_name='Drone1', speed=10):
        path = []
        path.append(end_geopoint)
        start_gps = end_geopoint
        middle_gps = None
        node_counts = 0

        #while self.detect_collisions_with_2_gps(current_geopoint, end_geopoint) is True:
            #half_way = airsim.GeoPoint()
            #half_way.latitude = (end_geopoint.latitude + current_geopoint.latitude) / 2
            #half_way.longitude = (end_geopoint.longitude + current_geopoint.longitude) / 2
            #half_way.altitude = ((end_geopoint.altitude + current_geopoint.altitude) / 2) + 10

            #while self.detect_collisions_with_2_gps(current_geopoint, half_way) is True:
                #half_way.altitude += 20
    
            #path.append(half_way)
            #current_geopoint = half_way

        while True:
            is_middle_gps_valid = False
            while not is_middle_gps_valid:
                north_meters_offset = random.uniform(-20, 20)
                east_meters_offset = random.uniform(-20, 20)
                altitude_offset = random.uniform(-20, 20)

                middle_gps = self.calculate_new_geo_point(start_gps, north_meters_offset, east_meters_offset, altitude_offset)
                if not self.detect_collisions_with_2_gps(start_gps, middle_gps):
                    is_middle_gps_valid = True
                    start_gps = middle_gps
                    path.append(middle_gps)
                    node_counts += 1

            if node_counts > 5:             # Kolin: limit the nodes amount in the path to avoid to much middle waypoints.
                start_gps = end_geopoint    # in this case, re-calculate the path.
                middle_gps = None
                path = []
                path.append(end_geopoint)

            if not self.detect_collisions_without_report(start_gps, drone_name):
                path.reverse()
                self.set_path(path, drone_name, speed)
                return


        
    """
    @Kolin: Detect a collision between 2 gps points.

    """   
    def detect_collisions_with_2_gps(self, start_geo, end_geo):
        # Test line of sight
        result = self.client.simTestLineOfSightBetweenPoints(start_geo, end_geo)
        if not result:            
            return True

        else:            
            return False


    """
    @Kolin: This is for the ChatGPT to set a calculated path to avoid a detected collision and then fly along it.
    """   
    def set_path(self, path_gps, drone_name='Drone1', speed=10):
        message = f"A Collision-Avoid path for {drone_name} is calculated!"
        self.display_signal.emit(Message(Roles.SYSTEM, message))        # Kolin: Show the result on the UI.
        print(message)
        
        message = f"{drone_name} Moving to avoid the collision..."
        self.display_signal.emit(Message(Roles.SYSTEM, message))        # Kolin: Show the massage on the UI.
        print(message)

        self.fly_path_gps(path_gps, drone_name, speed=speed)            # Kolin: Fly along the path
        

        count = self.drone_surveyor.count(drone_name)
        message = f"Strips of {drone_name}: {count}"
        self.display_signal.emit(Message(Roles.SYSTEM, message))
        print(message)

        
        
    """
    @Kolin: Reset the strips number
    """   
    def reset_survey_counter(self, drone_name='all'):
        if drone_name == "all":
            self.drone_surveyor.calibrate_all()
            message = f"Strips of all the drones calibrated."

        else:
            self.drone_surveyor.calibrate(drone_name)
            message = f"Strips of {drone_name} have been calibrated."

        self.display_signal.emit(Message(Roles.SYSTEM, message))        # Kolin: Show the result on the UI.
        print(message)
        
        
    """
    @Kolin: Method to enable manual control of a drone.
    """   
    def manual_controll(self, drone_name='Drone1', speed=5): # fix: controll typo
        message = f"Switched to Manual Control mode of {drone_name}! Press 'w', 's', 'a', 'd' for flying forward, backword, left, right, press y for flying up and x for down. Press 'q' to yaw counterclockwise and 'e' to yaw clockwise. Press 'p' to quit manual controll mode."
        self.display_signal.emit(Message(Roles.SYSTEM, message))        # Kolin: Show the result on the UI.
        print(message)
        
        speed = speed

        while not self.drone_surveyor.person_detected:                  # Kolin: Person detection added.
            current_position = self.get_drone_position(drone_name)     
            current_yaw = self.get_yaw(drone_name)

            if keyboard.is_pressed('y'):    # up
                target_pos = self.calculate_xyz_with_direction_and_distance(current_position, 5, current_yaw, "up")
                self.fly_to_xyz_asnychron(target_pos, drone_name, speed)
            elif keyboard.is_pressed('x'):  # down
                target_pos = self.calculate_xyz_with_direction_and_distance(current_position, 5, current_yaw, "down")
                self.fly_to_xyz_asnychron(target_pos, drone_name, speed)
            elif keyboard.is_pressed('a'):  # left
                target_pos = self.calculate_xyz_with_direction_and_distance(current_position, 5, current_yaw, "left")
                self.fly_to_xyz_asnychron(target_pos, drone_name, speed)
            elif keyboard.is_pressed('d'):  # right
                target_pos = self.calculate_xyz_with_direction_and_distance(current_position, 5, current_yaw, "right")
                self.fly_to_xyz_asnychron(target_pos, drone_name, speed)
            elif keyboard.is_pressed('w'):  # forward
                target_pos = self.calculate_xyz_with_direction_and_distance(current_position, 5, current_yaw, "forward")
                self.fly_to_xyz_asnychron(target_pos, drone_name, speed)
            elif keyboard.is_pressed('s'):  # backword
                target_pos = self.calculate_xyz_with_direction_and_distance(current_position, 5, current_yaw, "backword")
                self.fly_to_xyz_asnychron(target_pos, drone_name, speed)
            elif keyboard.is_pressed('q'):  # yaw counterclockwise
                self.set_yaw_asynchron(current_yaw - 15, drone_name)                   
            elif keyboard.is_pressed('e'):  # backword
                self.set_yaw_asynchron(current_yaw + 15, drone_name)      
            elif keyboard.is_pressed('p'):  # yaw clockwise
                message = f"Cancel Manual Control mode of {drone_name}!"
                self.display_signal.emit(Message(Roles.SYSTEM, message))        # Kolin: Show the result on the UI.
                print(message)
                break                

            time.sleep(0.1)  # Small delay to avoid sending too many commands at once.
                
            if self.drone_surveyor.person_detected and drone_name in self.drone_surveyor.person_found_by_drone_list:                             # Kolin: if person detected, move to his position.
                message = f"**********The person is found by {drone_name}!!! {drone_name} Moving to his position...**********"
                print(message)
                self.display_signal.emit(Message(Roles.SYSTEM, message))        # Kolin: show the massage on the UI.

                person_location = self.drone_surveyor.person_location
                drone_location = self.get_drone_position(drone_name)
                person_location = self.calculate_xyz_with_direction_and_distance(person_location, 15, direction_or_destination=drone_location)      # Kolin: move the destination 10 meters before the person and not punch directly the person.
                    
                delta_x = person_location[0] - drone_location[0]
                delta_y = person_location[1] - drone_location[1]
                delta_z = drone_location[2] - person_location[2]            # Kolin: Warning: The height in xyz is inverted.
                    
                drone_gps = self.get_drone_geopoint(drone_name)             # Kolin: Change to gps system to detect collision.
                person_gps = self.calculate_new_geo_point(drone_gps, delta_y, delta_x, delta_z)
                    
                if self.detect_collisions(person_gps, drone_name):          # Kolin: If the path to the person includes a collision.
                    # Kolin: If there is a collision, then avoid it.
                    message = f"calculating a path to avoid the collision for {drone_name}.."
                    print(message)
                    self.display_signal.emit(Message(Roles.SYSTEM, message))        # Kolin: Show the massage on the UI.

                    self.collision_avoidance_calculation(person_gps, drone_name)
                    self.reset_survey_counter()
                else:
                    self.fly_to_xyz(person_location, drone_name)
                        
                message ="Hura!!"
                print(message)
                self.display_signal.emit(Message(Roles.SYSTEM, message))        # Kolin: Show the massage on the UI.

      


    def switch_current_drone_shown(self, drone_name):
        self.view_controller.current_drone_shown = drone_name


    def free_camera(self):
        pass

    def delete_drone(self, drone_name):
        self.view_controller.delete_drone_from_ui(drone_name)

    def switch_current_drone(self, drone_name):
        self.view_controller.current_drone = drone_name
        
    """
    @Kolin: Line formation for the drones. Just a method for testing purposes.

    """    
    def all_drones_get_in_line_formation(self, speed=20):
        try:
            all_in_position = False
            drones_and_their_reach_corner_results = SimpleNamespace()
            drone_list = self.list_drones()
            start_position = [0, 0, 0]
            positions_in_line = [
                start_position,
                [start_position[0], start_position[1] + 10, start_position[2]],
                [start_position[0], start_position[1] - 10, start_position[2]],
                [start_position[0], start_position[1] + 20, start_position[2]],
                [start_position[0], start_position[1] - 20, start_position[2]],
                [start_position[0], start_position[1] + 30, start_position[2]]
            ]
        
            for drone, position in zip(drone_list, positions_in_line):
                self.client.enableApiControl(True, vehicle_name=drone)
                setattr(drones_and_their_reach_corner_results, drone, False)          # Kolin: Mark the drones, whether they are already in the destination or not.
 
                # Kolin: asynchron movement.
                self.client.moveToPositionAsync(position[0], position[1], position[2], speed, vehicle_name=drone)
                    
                message = f"moving {drone}, to {position}..."
                self.display_signal.emit(Message(Roles.SYSTEM, message))
                print(message)
                    
            while not all_in_position:                              # Kolin: Report the drone, if it gets in position.
                for drone, position in zip(drone_list, positions_in_line):
                    current_pos = self.get_drone_position(drone)
                    delta_x = position[0] - current_pos[0]
                    delta_y = position[1] - current_pos[1]
                    
                    if (-20 < delta_x < 20) and (-20 < delta_y < 20):
                        if getattr(drones_and_their_reach_corner_results, drone) != True:
                            setattr(drones_and_their_reach_corner_results, drone, True)
                            message = f"{drone}: get in line position!!"
                            self.display_signal.emit(Message(Roles.SYSTEM, message))
                            print(message)
                        
                false_count = sum(1 for value in drones_and_their_reach_corner_results.__dict__.values() if value is False)  # Kolin: Count how many return false.
                if false_count == 0:
                    all_in_position = True
                    
                time.sleep(2)
                
            if all_in_position:
                message = f"All drones are in position of the line!!"
                self.display_signal.emit(Message(Roles.SYSTEM, message))
                print(message)

                    
        except Exception as e:
            print(f"An error occurred during moving to survey area: {e}")


    """
    @Kolin: Calculate a target position with the given start yaw digrees, start position, destination position or a direction to the target position and the distance towards it.

    """                
    def calculate_xyz_with_direction_and_distance(self, start_pos, distance='10', start_yaw='0', direction_or_destination='forward'):
        target_yaw = start_yaw
        delta_z = 0

        if direction_or_destination == "forward":
            pass     
        elif direction_or_destination == "backward":
            target_yaw = (target_yaw + 180) % 360
        elif direction_or_destination == "left":
            target_yaw = (target_yaw - 90) % 360
        elif direction_or_destination == "right":
            target_yaw = (target_yaw + 90) % 360
        elif direction_or_destination == "up":
            delta_z = -distance
            distance = 0    # Kolin: make the xy offset to 0.
        elif direction_or_destination == "down":
            delta_z = distance
            distance = 0    # Kolin: make the xy offset to 0.
        else:
            # Kolin: if the input is a position.
            target_yaw = self.calculate_yaw_angle_with_pos(start_pos, direction_or_destination)     # Kolin: horizon winkel.
            vertical_angle = self.calculate_vertical_angle(start_pos, direction_or_destination)     # Kolin: verticle winkel.
            delta_z = distance * math.sin(vertical_angle)   # Kolin: calculate delta_z.

            

        yaw_radians = math.radians(target_yaw)

        delta_x = distance * math.cos(yaw_radians)      # Kolin: calculate delta_x.
        delta_y = distance * math.sin(yaw_radians)      # Kolin: calculate delta_y.

        target_pos = [start_pos[0] + delta_x, start_pos[1] + delta_y, start_pos[2] + delta_z]
        return target_pos

    """
    @Kolin: Calculate a verticle angle in radians between 2 xyz coordinates.

    """   
    def calculate_vertical_angle(self, start_pos, end_pos):
        horizontal_distance = math.sqrt((end_pos[0] - start_pos[0])**2 + (end_pos[1] - start_pos[1])**2)
        vertical_difference = end_pos[2] - start_pos[2]
        return math.atan2(vertical_difference, horizontal_distance)  # Returns angle in radians
    

   
        
        
