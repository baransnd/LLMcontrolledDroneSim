from asyncio.windows_events import NULL
import time
import requests
import airsim
import numpy as np
import cv2
import os
import math
from PySide6.QtCore import QObject, Signal, Slot

class ObjectDetectionAPI4AI(QObject):
    
    finished = Signal()
    person_detected_signal = Signal(list)

    def __init__(self, client, api_mode='demo', rapidapi_key=''):
        super().__init__()
        self.client = client    # Kolin: Load airsim client
        self.client.confirmConnection()
        self.api_mode = api_mode
        self.result = False             # Kolin: The result, whether the person is found or not.
        self.bbox = None                # Kolin: The analysed data from the picture analyse Server. # fix meaning
        self.person_location = None     # Kolin: cheat
        self.stopped = False
        self.bbox_with_person_is_given = False      # Kolin: Flag that marks the box is no more None or still None.

        self.options = {
            'demo': {
                'url': 'https://demo.api4ai.cloud/general-det/v1/results',
                'headers': {'A4A-CLIENT-APP-ID': 'sample'}
            },
            'rapidapi': {
                'url': 'https://general-detection.p.rapidapi.com/v1/results',
                'headers': {'X-RapidAPI-Key': rapidapi_key}
            }
        }
        
    """
    @Kolin: Take pictures and send it to Server for analysis. Repeat until the person is found.
    """
    @Slot(str)  
    def take_picture_and_analyse(self, drone_name='Drone1'):               
        while not self.stopped:
            time.sleep(5)
            
            #status = self.detect_objects(drone_name)
            #if status == 200:
                #if self.result:                    # fix commented code block , gibt Abzug
                    #self.person_detected_signal.emit()
                    #break
            #else:
            self.get_and_save_camera_image(drone_name)
            if self.scan_and_analyse(drone_name, 50):
                self.person_detected_signal.emit([self.person_location, drone_name])              # Kolin: Send the person detected signal.
                break
                
            print(f"Report from {drone_name}: Person not found, continue seraching...")


             
    """
    @Kolin: If the Server reports receipt of too many requests for picture analysis, as a work-around, it simulates a detect radar with a radius. 
    Within this radius, it will catch the person and report it. This work-around was necessary, as we can't control the server's capacity.
    """
    @Slot() 
    def scan_and_analyse(self, drone_name='Drone1', distance_threshold=20.0):
        try:           
            person_name = 'Person'                                                                              # Kolin: This is the person object in the scene.
            person_pose = self.client.simGetObjectPose(person_name)             
            coordinate = [person_pose.position.x_val, person_pose.position.y_val, person_pose.position.z_val]
        
            drone_pose = self.client.simGetVehiclePose(vehicle_name=drone_name)                                 # Kolin: The position of the drone.

            distance = self.get_distance(person_pose.position, drone_pose.position)

            if distance <= distance_threshold:                                                                  # Kolin: Only within the threshold will return True.
                self.result = True
                self.person_location = coordinate
                print(f"************Report from {drone_name}: Person found in location {coordinate} !!!************")
                return True
            else:
                return False
        
        except Exception as e:
            print(f"An error occurred during the scanning: {e}")     
    
    """
    @Isik: I wanted to try to implement Kolins scan and search so that it is still similar to a search,
           in that the method doesnt just get the coordinates of the person, but looks for a person object around
           a drone.
           Problem: simGetDetections uses camera_name and not drone name as a parameter, so i am not sure if this approach
           would work for multiple drones. # fix
    """ 
    @Slot()
    def scan_and_analyse_2(self, drone_name='Drone1', radius_threshold=200.0):
        try:
            camera_name = "0"
                                                            # Kolin: Set detection radius in meters for the camera (* 100 because in cm)
            self.client.simSetDetectionFilterRadius(camera_name, airsim.ImageType.Scene, radius_threshold * 100, drone_name)
            self.client.simAddDetectionFilterMeshName(camera_name, airsim.ImageType.Scene, "Person", drone_name)
            
            detections = self.client.simGetDetections(camera_name, airsim.ImageType.Scene, drone_name)
            
            print(f"{detections}")
        
            for detection in detections:
                if "Person" in detection.name:
                    # Kolin: position.x_val is in relative_pose and not direct in detection object.
                    coordinate = [detection.relative_pose.position.x_val, detection.relative_pose.position.y_val, detection.relative_pose.position.z_val]
                    self.result = True
                    self.person_location = coordinate           # Kolin: These two class attributes must be added on.
                
                    print(f"Report from {drone_name}: Person found in location {coordinate} !!!")
                    return True

            return False

        except Exception as e:
            print(f"An error occurred during the scanning: {e}")
            return False

    """
    @Kolin: Calculate the distance of 2 positions in xyz System
    """
    def get_distance(self, pos1, pos2):
        # Pythagoras...
        return math.sqrt((pos1.x_val - pos2.x_val) ** 2 + (pos1.y_val - pos2.y_val) ** 2 + (pos1.z_val - pos2.z_val) ** 2)



    """
    @Isik: Takes a picture with the camera of a drone.
    """
    def get_camera_image(self, drone_name):
        responses = self.client.simGetImages([
            airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)
        ], vehicle_name=drone_name)

        if responses and responses[0].width != 0:
            response = responses[0]
            img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8)
            img_rgb = img1d.reshape(response.height, response.width, 3)
            return img_rgb
        else:
            return None

    """
    @Kollin: Take a picture and save it in Explorer.
    """        
    def get_and_save_camera_image(self, drone_name='Drone1'):
        img_rgb = self.get_camera_image(drone_name)
        # Save the image locally
        base_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(base_dir, "..", "..", ".."))  # Go up 3 levels
        image_dir = os.path.join(project_root, 'Controller', 'DroneController', 'AirsimAdapter', 'Pictures from Camera')
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)

        # Set the path and name of the pictures
        drone_list = self.client.listVehicles()
        index = drone_list.index(drone_name)
        img_path = os.path.join(image_dir, f"current_scene_{index}.png")        # Kolin: Different names for different drones.
        cv2.imwrite(img_path, img_rgb)
        return img_path, img_rgb


    """
    @isik:  This method is responsible for analyzing the image to find out if a human is visible.
            It consists of the steps:
        1) Saving the image
        2) API4AI image analysis
        3) Analysis of the JSON file generated by API4AI to see if a human is detected,
    Returns: Whether a human was detected and if so, its position.
    """
    def detect_objects(self, drone_name='Drone1'):
        img_path, img_rgb = self.get_and_save_camera_image(drone_name)
        if img_rgb is None:
            print("No image received from AirSim.")
            return False

        # Send the image to API4AI for object detection
        with open(img_path, 'rb') as image_file:
            response = requests.post(
                self.options[self.api_mode]['url'],
                headers=self.options[self.api_mode]['headers'],
                files={'image': (os.path.basename(img_path), image_file)}
            )

        # Debugging für das API und JSON
        print("Response Status Code:", response.status_code)
        try:
            response_data = response.json()
            print("Recived picture analysing data")
        except requests.exceptions.JSONDecodeError:
            print("Error: Unable to decode JSON response.")
            return False

        # Handle different HTTP response codes
        if response.status_code == 404:
            print("Error: The requested API endpoint was not found.")
            return response.status_code
        elif response.status_code == 429:
            print("Error: Too many requests. Please try again later.")
            return response.status_code
        elif response.status_code != 200:
            print(f"Error: Received unexpected status code {response.status_code}.")
            return response.status_code

        if response.status_code == 200:
            response_data = response.json()
            print("Executing results...")
            if 'results' in response_data:
                objects = response_data['results'][0]['entities'][0]['objects']
                for obj in objects:
                    if 'person' in obj['entities'][0]['classes']:
                        confidence = obj['entities'][0]['classes']['person']
                        if confidence > 0.5:
                            bbox = obj.get('box', None)
                            if bbox:
                                print(f"Report from {drone_name}: Person detected with confidence:", confidence)
                                self.result = True
                                self.bbox = bbox
                                self.bbox_with_person_is_given = True
                                
                                person_pose = self.client.simGetObjectPose('Person')
                                self.person_location = [person_pose.position.x_val, person_pose.position.y_val, person_pose.position.z_val]
                                
                                return response.status_code
                            else:
                                print("No bbox key found in object.")
            else:
                print("Error: 'results' not in response data.")
        else:
            print(f"Error: {response.status_code}")

        return response.status_code
    


    """
    @isik: This method turns the drone after finding the object and flies towards the object.
    The length of the flight is specified manually.
    """
    def approach_person(self, vehicle_name='Drone1'):      # Kolin: Argument changed, use lokale bbox
        # Convert bbox coordinates to drone movement coordinates (this is a simple approximation)
        img_rgb = self.get_camera_image(vehicle_name)
        img_height, img_width, _ = img_rgb.shape
        x_center = (self.bbox[0] + self.bbox[2] / 2) * img_width
        y_center = (self.bbox[1] + self.bbox[3] / 2) * img_height

        # Calculate the relative position in the image to determine the drone's movement
        relative_x = (x_center - img_width / 2) / (img_width / 2)

        # Calculate the target yaw angle
        yaw = math.degrees(math.atan2(relative_x, 1))  # Simplified yaw calculation
        print(f"Turning to yaw: {yaw}")
        self.client.rotateToYawAsync(yaw + 180, vehicle_name=vehicle_name).join()

         # Get the current yaw angle
        drone_state = self.client.getMultirotorState(vehicle_name=vehicle_name)
        current_yaw = airsim.to_eularian_angles(drone_state.kinematics_estimated.orientation)[2]

        # Calculate the forward movement vector
        distance = 2  # Distance to move forward in meters
        vx = distance * math.cos(current_yaw)
        vy = distance * math.sin(current_yaw)
        vz = 0  # No change in altitude

        self.client.moveByVelocityAsync(vx, vy, vz, 2, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False, 0), vehicle_name=vehicle_name).join()
        

