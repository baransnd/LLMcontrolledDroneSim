

from tkinter import Y
from PySide6.QtCore import QObject, Signal, Slot, QMetaObject, Q_ARG, Qt


from Controller.DroneController.OpenAIAdapter.openai_adapter import OpenAiAdapter
from Controller.DroneController.Utils.message import Roles
from Controller.DroneController.Utils.message import Message
import re




"""
@Kolin: the self made ai.
"""
class ManualAiAskWorker(QObject):
    display_signal = Signal(Message)
    response_signal = Signal(Message)
    finished = Signal()



    def __init__(self, airsim_adapter, view_controller):
        super().__init__()
        self.airsim_adapter = airsim_adapter
        self.view_controller = view_controller
        self.display_signal.connect(self.view_controller.display)       # Kolin: show the answers of the methods on the UI

    @Slot(str)
    def ask(self, prompt):
        codes_packed_together = []
        codes_for_Drone_1 = []
        codes_for_Drone_2 = []
        codes_for_Drone_3 = []
        codes_for_Drone_4 = []
        codes_for_Drone_5 = []
        codes_for_Drone_6 = []
        codes_for_drones = []
        codes_for_drones.append(codes_for_Drone_1)
        codes_for_drones.append(codes_for_Drone_2)
        codes_for_drones.append(codes_for_Drone_3)
        codes_for_drones.append(codes_for_Drone_4)
        codes_for_drones.append(codes_for_Drone_5)
        codes_for_drones.append(codes_for_Drone_6)


        codes_for_Drone_1.append("""----------------Drone1----------------""")
        codes_for_Drone_2.append("""----------------Drone2----------------""")
        codes_for_Drone_3.append("""----------------Drone3----------------""")
        codes_for_Drone_4.append("""----------------Drone4----------------""")
        codes_for_Drone_5.append("""----------------Drone5----------------""")
        codes_for_Drone_6.append("""----------------Drone6----------------""")

        matches = re.findall(r'\[(.*?)\]', prompt)
        modified_matches = [match.replace(',', ';') for match in matches]   # Kolin: replace all the commas in the brackets with ";" for the sake, not to influense the commas in the main sentance.
        for original, modified in zip(matches, modified_matches):
            prompt = prompt.replace(f'[{original}]', f'[{modified}]')

        sub_prompts = re.split(r'\s*then\s*|\s*,\s*', prompt)
        message = None 

        all_drones_list = ["Drone1", "Drone2", "Drone3", "Drone4", "Drone5", "Drone6"]
        followed_drone = None

        for prompt in sub_prompts:
            if "all" in prompt:
                drone_list = self.airsim_adapter.list_drones()

            elif "follow" in prompt:
                # Regex to find 'follow' immediately followed by any drone name
                follow_pattern = r"follow\s+(" + '|'.join(re.escape(drone) for drone in all_drones_list) + r")\b"
                if "follows" in prompt:
                    follow_pattern = r"follows\s+(" + '|'.join(re.escape(drone) for drone in all_drones_list) + r")\b"
                match = re.search(follow_pattern, prompt)
                if match:
                    followed_drone = match.group(1)  # Add the found drone name after 'follow'

                prompt = prompt.split("follow")[0]      # Kolin: split the followed drone out.
                prompt += " follow"                     # Kolin: add the mark 'follow' back.
                pattern = r'\b(' + '|'.join(re.escape(drone) for drone in all_drones_list) + r')\b'     # Kolin: match all the drone_name
                drone_list = re.findall(pattern, prompt)

                for drone_name in drone_list:
                    prompt = prompt.replace(drone_name, "")     # Kolin: replace the drone with empty, for the sake, not to influense the parameters in the main sentance.

            elif any(drone in prompt for drone in all_drones_list):
                pattern = r'\b(' + '|'.join(re.escape(drone) for drone in all_drones_list) + r')\b'     # Kolin: match all the drone_name
                drone_list = re.findall(pattern, prompt)

                for drone_name in drone_list:
                    prompt = prompt.replace(drone_name, "")     # Kolin: replace the drone with empty, for the sake, not to influense the parameters in the main sentance.

            else:
                drone_name = "Drone1"                       # Kolin: Default situation.
                drone_list = []
                drone_list.append("Drone1")

            
            # Kolin: *************************************the part of manual ai*************************************************************************************

            # Kolin: take off.
            if "takeoff" in prompt or "take_off" in prompt or "take off" in prompt:
                for drone in drone_list:
                    match = re.findall(r'\d', drone)
                    drone_number = int(match[0])
                    index = drone_number - 1

                    codes_for_drones[index].append(f"""
self.airsim_adapter.takeoff("{drone}")
""")

            # Kolin: land.
            if "land" in prompt:
                for drone in drone_list:
                    match = re.findall(r'\d', drone)
                    drone_number = int(match[0])
                    index = drone_number - 1

                    codes_for_drones[index].append(f"""
self.airsim_adapter.land("{drone}")
""")

            # Kolin: get 
            if "give" in prompt or "tell" in prompt:

                # Kolin: the position of the drone.
                if "pos" in prompt or "coor" in prompt or "xyz" in prompt:
                    for drone in drone_list:
                        match = re.findall(r'\d', drone)
                        drone_number = int(match[0])
                        index = drone_number - 1

                        codes_for_drones[index].append(f"""
pos = self.airsim_adapter.get_drone_position("{drone}")
message = f"The position(Vector 3D) of the drone Drone1 is: \\n [ x: {{pos[0]}} ]\\n [ y: {{pos[1]}} ] \\n [ z: {{pos[2]}} ]"
self.airsim_adapter.display_content_from_server(message)
""")
                # Kolin: the gps of the drone.
                if "gps" in prompt or "geo" in prompt:
                    for drone in drone_list:
                        match = re.findall(r'\d', drone)
                        drone_number = int(match[0])
                        index = drone_number - 1

                        codes_for_drones[index].append(f"""
gps = self.airsim_adapter.get_drone_geopoint("{drone}")
message = f"The GPS of the drone Drone1 is: \\n [ latitude: {{gps.latitude}} ] \\n [ longitude: {{gps.longitude}} ] \\n [ altitude: {{gps.altitude}} ]"
self.airsim_adapter.display_content_from_server(message)
""")
                # Kolin: the yaw of the drone.
                if "yaw" in prompt or "wink" in prompt or "dig" in prompt:
                    for drone in drone_list:
                        match = re.findall(r'\d', drone)
                        drone_number = int(match[0])
                        index = drone_number - 1

                        codes_for_drones[index].append(f"""
yaw_degrees = self.airsim_adapter.get_yaw("{drone}")
self.airsim_adapter.display_content_from_server(f"The Yaw of Drone1 is: {{yaw_degrees}} degrees.")
""")

            # Kolin: turn the drone with a given yaw degrees.
            if "turn" in prompt:
                match = re.search(r"[-+]?\d*\.\d+|[-+]?\d+", prompt)    # Kolin: only if the degree is given, will precceed.
                if match:
                    yaw_degree = float(match.group(0))
                    for drone in drone_list:
                        match = re.findall(r'\d', drone)
                        drone_number = int(match[0])
                        index = drone_number - 1

                        codes_for_drones[index].append(f"""
yaw = self.airsim_adapter.get_yaw("{drone}")
yaw = (yaw + {yaw_degree}) % 360
self.airsim_adapter.set_yaw(yaw, "{drone}")
""")
            # Kolin: list the drones.
            if "list" in prompt:
                codes_for_drones[0].append(f"""
self.airsim_adapter.list_drones()
""")
            # Kolin: move forward.
            if "forw" in prompt:
                numbers = re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", prompt)
                if numbers:
                    meters = float(numbers[0])  # Convert first number to float, this is the move distance.
                    speed = 5                   # Kolin: default speed.
                    if len(numbers) > 1:
                        speed = float(numbers[1])   # Convert second number to float

                    for drone in drone_list:
                        match = re.findall(r'\d', drone)
                        drone_number = int(match[0])
                        index = drone_number - 1

                        codes_for_drones[index].append(f"""
current_pos = self.airsim_adapter.get_drone_position("{drone}")
drone_yaw = self.airsim_adapter.get_yaw("{drone}")
target_pos = self.airsim_adapter.calculate_xyz_with_direction_and_distance(current_pos, {meters}, drone_yaw)

self.airsim_adapter.fly_to_xyz_with_collision_avoidance_and_get_in_position_report(target_pos, "{drone}", {speed})
""")
            # Kolin: move backward.
            if "bac" in prompt:
                numbers = re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", prompt)
                if numbers:
                    meters = float(numbers[0])  # Convert first number to float
                    speed = 5
                    if len(numbers) > 1:
                        speed = float(numbers[1])   # Convert second number to float

                    for drone in drone_list:
                        match = re.findall(r'\d', drone)
                        drone_number = int(match[0])
                        index = drone_number - 1

                        codes_for_drones[index].append(f"""
current_pos = self.airsim_adapter.get_drone_position("{drone}")
drone_yaw = self.airsim_adapter.get_yaw("{drone}")
target_pos = self.airsim_adapter.calculate_xyz_with_direction_and_distance(current_pos, {meters}, drone_yaw, "backward")

self.airsim_adapter.fly_to_xyz_with_collision_avoidance_and_get_in_position_report(target_pos, "{drone}", {speed})
""")
            # Kolin: move left.
            if "lef" in prompt:
                numbers = re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", prompt)
                if numbers:
                    meters = float(numbers[0])  # Convert first number to float
                    speed = 5
                    if len(numbers) > 1:
                        speed = float(numbers[1])   # Convert second number to float

                    for drone in drone_list:
                        match = re.findall(r'\d', drone)
                        drone_number = int(match[0])
                        index = drone_number - 1

                        codes_for_drones[index].append(f"""
current_pos = self.airsim_adapter.get_drone_position("{drone}")
drone_yaw = self.airsim_adapter.get_yaw("{drone}")
target_pos = self.airsim_adapter.calculate_xyz_with_direction_and_distance(current_pos, {meters}, drone_yaw, "left")

self.airsim_adapter.fly_to_xyz_with_collision_avoidance_and_get_in_position_report(target_pos, "{drone}", {speed})
""")
            # Kolin: move right.
            if "righ" in prompt:
                numbers = re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", prompt)
                if numbers:
                    meters = float(numbers[0])  # Convert first number to float
                    speed = 5
                    if len(numbers) > 1:
                        speed = float(numbers[1])   # Convert second number to float

                    for drone in drone_list:
                        match = re.findall(r'\d', drone)
                        drone_number = int(match[0])
                        index = drone_number - 1

                        codes_for_drones[index].append(f"""
current_pos = self.airsim_adapter.get_drone_position("{drone}")
drone_yaw = self.airsim_adapter.get_yaw("{drone}")
target_pos = self.airsim_adapter.calculate_xyz_with_direction_and_distance(current_pos, {meters}, drone_yaw, "right")

self.airsim_adapter.fly_to_xyz_with_collision_avoidance_and_get_in_position_report(target_pos, "{drone}", {speed})
""")
            # Kolin: move up.
            if "up" in prompt:
                numbers = re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", prompt)
                if numbers:
                    meters = float(numbers[0])  # Convert first number to float
                    speed = 5
                    if len(numbers) > 1:
                        speed = float(numbers[1])   # Convert second number to float

                    for drone in drone_list:
                        match = re.findall(r'\d', drone)
                        drone_number = int(match[0])
                        index = drone_number - 1

                        codes_for_drones[index].append(f"""
current_pos = self.airsim_adapter.get_drone_position("{drone}")
drone_yaw = self.airsim_adapter.get_yaw("{drone}")
target_pos = self.airsim_adapter.calculate_xyz_with_direction_and_distance(current_pos, {meters}, drone_yaw, "up")

self.airsim_adapter.fly_to_xyz_with_collision_avoidance_and_get_in_position_report(target_pos, "{drone}", {speed})
""")
            # Kolin: move down.
            if "down" in prompt:
                numbers = re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", prompt)
                if numbers:
                    meters = float(numbers[0])  # Convert first number to float
                    speed = 5
                    if len(numbers) > 1:
                        speed = float(numbers[1])   # Convert second number to float

                    for drone in drone_list:
                        match = re.findall(r'\d', drone)
                        drone_number = int(match[0])
                        index = drone_number - 1

                        codes_for_drones[index].append(f"""
current_pos = self.airsim_adapter.get_drone_position("{drone}")
drone_yaw = self.airsim_adapter.get_yaw("{drone}")
target_pos = self.airsim_adapter.calculate_xyz_with_direction_and_distance(current_pos, {meters}, drone_yaw, "down")

self.airsim_adapter.fly_to_xyz_with_collision_avoidance_and_get_in_position_report(target_pos, "{drone}", {speed})
""")
            # Kolin: move north.
            if "nort" in prompt:
                numbers = re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", prompt)
                if numbers:
                    meters = float(numbers[0])  # Convert first number to float
                    speed = 5
                    if len(numbers) > 1:
                        speed = float(numbers[1])   # Convert second number to float

                    for drone in drone_list:
                        match = re.findall(r'\d', drone)
                        drone_number = int(match[0])
                        index = drone_number - 1

                        codes_for_drones[index].append(f"""
current_gps = self.airsim_adapter.get_drone_geopoint("{drone}")
target_gps = self.airsim_adapter.calculate_new_geo_point(current_gps, {meters})

self.airsim_adapter.fly_to_gps_with_collision_avoidance_and_get_in_position_report(target_gps, "{drone}", {speed})
""")
            # Kolin: move south.
            if "sout" in prompt:
                numbers = re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", prompt)
                if numbers:
                    meters = float(numbers[0])  # Convert first number to float
                    speed = 5
                    if len(numbers) > 1:
                        speed = float(numbers[1])   # Convert second number to float

                    for drone in drone_list:
                        match = re.findall(r'\d', drone)
                        drone_number = int(match[0])
                        index = drone_number - 1

                        codes_for_drones[index].append(f"""
current_gps = self.airsim_adapter.get_drone_geopoint("{drone}")
target_gps = self.airsim_adapter.calculate_new_geo_point(current_gps, {-meters})

self.airsim_adapter.fly_to_gps_with_collision_avoidance_and_get_in_position_report(target_gps, "{drone}", {speed})
""")
            # Kolin: move east.
            if "east" in prompt:
                numbers = re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", prompt)
                if numbers:
                    meters = float(numbers[0])  # Convert first number to float
                    speed = 5
                    if len(numbers) > 1:
                        speed = float(numbers[1])   # Convert second number to float

                    for drone in drone_list:
                        match = re.findall(r'\d', drone)
                        drone_number = int(match[0])
                        index = drone_number - 1

                        codes_for_drones[index].append(f"""
current_gps = self.airsim_adapter.get_drone_geopoint("{drone}")
target_gps = self.airsim_adapter.calculate_new_geo_point(current_gps, 0, {meters})

self.airsim_adapter.fly_to_gps_with_collision_avoidance_and_get_in_position_report(target_gps, "{drone}", {speed})
""")
            # Kolin:  move west.
            if "west" in prompt:
                numbers = re.findall(r"\-?\d+\.?\d*", prompt)
                if numbers:
                    meters = float(numbers[0])  # Convert first number to float
                    speed = 5
                    if len(numbers) > 1:
                        speed = float(numbers[1])   # Convert second number to float

                    for drone in drone_list:
                        match = re.findall(r'\d', drone)
                        drone_number = int(match[0])
                        index = drone_number - 1

                        codes_for_drones[index].append(f"""
current_gps = self.airsim_adapter.get_drone_geopoint("{drone}")
target_gps = self.airsim_adapter.calculate_new_geo_point(current_gps, 0, {-meters})

self.airsim_adapter.fly_to_gps_with_collision_avoidance_and_get_in_position_report(target_gps, "{drone}", {speed})
""")
            
            # Kolin: set position.
            if "set" in prompt:
                if "pos" in prompt:
                    bracket_contents = re.findall(r'\[(.*?)\]', prompt)
    
                    # Kolin: This will store all the numbers found within all bracket instances
                    all_numbers = []
    
                    # Kolin: Extract numbers from each bracketed content
                    for content in bracket_contents:
                        # Kolin: Find all numbers in the content
                        numbers = re.findall(r'\-?\d+\.?\d*', content)
                        all_numbers.extend(numbers)  # Kolin: Add these numbers to the main list

                    if all_numbers:
                        x, y, z = map(float, all_numbers)  # Convert strings to floats
                        coord = [x, y, z]

                        for drone in drone_list:
                            match = re.findall(r'\d', drone)
                            drone_number = int(match[0])
                            index = drone_number - 1

                            codes_for_drones[index].append(f"""
self.airsim_adapter.set_position({coord}, 0, "{drone}")
""")

            # Kolin: fly the drone to a givem [x, y, z] coordinate.
            if "[" in prompt and "set" not in prompt:
                
                bracket_contents = re.findall(r'\[(.*?)\]', prompt)
    
                # Kolin: This will store all the numbers found within all bracket instances
                all_numbers = []
    
                # Kolin: Extract numbers from each bracketed content
                for content in bracket_contents:
                    # Kolin: Find all numbers in the content
                    numbers = re.findall(r'\-?\d+\.?\d*', content)
                    all_numbers.extend(numbers)  # Kolin: Add these numbers to the main list

                if all_numbers:
                    x, y, z = map(float, all_numbers)  # Convert strings to floats

                    # Remove the bracketed part from the prompt
                    prompt = re.sub(r"\[(.*?)\]", "", prompt)

                    # Find the remaining number, assuming it's the speed
                    remaining_numbers = re.findall(r"\-?\d+\.?\d*", prompt)
                    speed = 5
                    if remaining_numbers:
                        speed = float(remaining_numbers[0])  # Convert the first found number to float

                    # Prepare coordinates list
                    coord = [x, y, z]

                    for drone in drone_list:
                        match = re.findall(r'\d', drone)
                        drone_number = int(match[0])
                        index = drone_number - 1
                    # Append the code snippet to the drone's code list
                        codes_for_drones[index].append(f"""
target_pos = {coord}
self.airsim_adapter.fly_to_xyz_with_collision_avoidance_and_get_in_position_report(target_pos, "{drone}", {speed})
""")
            # Kolin: manual control
            if "manua" in prompt:
                for drone in drone_list:
                    match = re.findall(r'\d', drone)
                    drone_number = int(match[0])
                    index = drone_number - 1

                    codes_for_drones[index].append(f"""
self.airsim_adapter.manual_controll("{drone}")
""")
            # Kolin: switch camera.
            if "switch" in prompt:
                for drone in drone_list:
                    match = re.findall(r'\d', drone)
                    drone_number = int(match[0])
                    index = drone_number - 1

                    codes_for_drones[index].append(f"""
self.airsim_adapter.switch_to_camera("{drone}")
""")
            # Kolin: add drones.By default add 1 drone. It will be specially handled and not as code executed.
            if "add" in prompt:
                numbers = re.findall(r"add\s+(\d+)", prompt)
                number = 1
                if numbers:
                    number = numbers[0]

                message = f"{number} drone(s) added."
                self.display_signal.emit(Message(Roles.ASSISTANT, message))        
                print(message) 

            # Kolin: let the drones get in line position.
            if "line" in prompt:
                start_position = self.airsim_adapter.get_drone_position("Drone1")
                positions = [
                    start_position,
                    [start_position[0], start_position[1] + 10, start_position[2]],
                    [start_position[0], start_position[1] - 10, start_position[2]],
                    [start_position[0], start_position[1] + 20, start_position[2]],
                    [start_position[0], start_position[1] - 20, start_position[2]],
                    [start_position[0], start_position[1] + 30, start_position[2]]
                    ]

                QMetaObject.invokeMethod(self.view_controller.drone_surveyor, "start_drone_arrives_count", Qt.QueuedConnection, Q_ARG(int, len(drone_list)))
                numbers = re.findall(r"\-?\d+\.?\d*", prompt)
                speed = 20
                if numbers:
                    speed = float(remaining_numbers[0])  # Convert the first found number to float

                drone_list = self.airsim_adapter.list_drones()
                for drone, pos in zip(drone_list, positions):
                    match = re.findall(r'\d', drone)
                    drone_number = int(match[0])
                    codes_for_drones[drone_number - 1].append(f"""
self.airsim_adapter.fly_to_xyz_with_collision_avoidance_and_get_in_position_report([{pos[0]}, {pos[1]}, {pos[2]}], "{drone}", {speed})
""")



            # Kolin: let the drones move to their search position and prepare for searching.
            if "search " in prompt or "prepar" in prompt:
                corners = self.airsim_adapter.divide_into_subareas()

                # Kolin: start the counter with exactly the drone amounts.
                QMetaObject.invokeMethod(self.view_controller.drone_surveyor, "start_drone_arrives_count", Qt.QueuedConnection, Q_ARG(int, len(drone_list)))
                numbers = re.findall(r"\-?\d+\.?\d*", prompt)
                speed = 30
                if numbers:
                    speed = float(remaining_numbers[0])  # Convert the first found number to float


                for drone, corner in zip(drone_list, corners):
                    match = re.findall(r'\d', drone)
                    drone_number = int(match[0])
                    codes_for_drones[drone_number - 1].append(f"""
target_geopoint = airsim.GeoPoint()
target_geopoint.latitude = {corner.latitude}
target_geopoint.longitude = {corner.longitude}
target_geopoint.altitude = {corner.altitude}
self.airsim_adapter.fly_to_gps_with_collision_avoidance_and_get_in_position_report(target_geopoint, "{drone}", {speed})
""")

            # Kolin: let the drones beginns searching.
            if "begin" in prompt or "surv" in prompt or "go sear" in prompt:
                length = 60
                width = 30
                strip_width = 6
                speed = 10

                if "length" in prompt:
                    match_length = re.search(r'length\s+(\d+)', prompt)
                    if match_length:
                        length = float(match_length.group(1))
                if "width" in prompt:
                    match_width = re.search(r'width\s+(\d+)', prompt)
                    if match_width:
                        width = float(match_width.group(1))
                if "strip_width" in prompt:
                    match_strip_width = re.search(r'strip width\s+(\d+)', prompt)
                    if match_strip_width:
                        strip_width = float(match_strip_width.group(1))
                if "speed" in prompt:
                    match_speed = re.search(r'speed\s+(\d+)', prompt)
                    if match_speed:
                        speed = float(match_speed.group(1))


                for drone in drone_list:
                    match = re.findall(r'\d', drone)
                    drone_number = int(match[0])
                    codes_for_drones[drone_number - 1].append(f"""
self.airsim_adapter.zik_zak_survey("{drone}", {length}, {width}, {strip_width}, {speed})
""")

            # Kolin: a drone follow another drone.
            if "follow" in prompt:
                for drone in drone_list:
                    match = re.findall(r'\d', drone)
                    drone_number = int(match[0])
                    codes_for_drones[drone_number - 1].append(f"""
self.airsim_adapter.follow_drone("{drone}", "{followed_drone}")
""")

            drone_list = []     # Kolin: calibrate drone_list.

# **************************************************************************************************************************


        codes_for_Drone_1.append("""----------------------------------------""")
        codes_for_Drone_2.append("""----------------------------------------""")
        codes_for_Drone_3.append("""----------------------------------------""")
        codes_for_Drone_4.append("""----------------------------------------""")
        codes_for_Drone_5.append("""----------------------------------------""")
        codes_for_Drone_6.append("""----------------------------------------""")

        # Kolin: filter the empty code block out.
        if len(codes_for_Drone_1) > 2:
            codes_packed_together.extend(codes_for_Drone_1)
        if len(codes_for_Drone_2) > 2:
            codes_packed_together.extend(codes_for_Drone_2)
        if len(codes_for_Drone_3) > 2:
            codes_packed_together.extend(codes_for_Drone_3)
        if len(codes_for_Drone_4) > 2:
            codes_packed_together.extend(codes_for_Drone_4)
        if len(codes_for_Drone_5) > 2:
            codes_packed_together.extend(codes_for_Drone_5)
        if len(codes_for_Drone_6) > 2:
            codes_packed_together.extend(codes_for_Drone_6)

        final_code_string = ''.join(codes_packed_together)
        if "System" in prompt:
            message = Message(Roles.SYSTEM, final_code_string)
        else:
            message = Message(Roles.ASSISTANT, final_code_string)
        self.response_signal.emit(message)

        
        



