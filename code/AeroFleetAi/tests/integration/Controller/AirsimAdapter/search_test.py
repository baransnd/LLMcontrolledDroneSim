from unittest import result
import airsim
import time
import sys
from unittest.mock import Mock, MagicMock
from pathlib import Path
from PySide6.QtCore import Slot, QThread, QMetaObject, Qt, QCoreApplication, QUrl, Q_ARG
from PySide6.QtWidgets import QApplication

path_root = Path(__file__).parents[4]
sys.path.append(str(path_root))


from Controller.DroneController.AirsimAdapter.airsim_adapter import AirsimAdapter
from Controller.DroneController.AirsimAdapter.airsim_adapter import DroneSurveyor
from Controller.DroneController.AirsimAdapter.airsim_adapter import ObjectDetectionAPI4AI
from Controller.ViewController.view_controller import ViewController
from Controller.DroneController.Utils.message import Message
from Controller.DroneController.Utils.message import Roles


    
"""
@Kolin: Tests the ability of the Airsim Adapter to order the drones go searching.
"""
def test_search():
    # Initialize View Controller
    app = QApplication(sys.argv)
    view_controller = ViewController()
        
    adapter = view_controller.airsim_adapter    
    
    adapter.add_multiple_drones(5)      # Kolin: add 5 drones.

    # Wait for the drone to be added. Kolin: if add a drone cost 2s, i set it to 10s because of 5 drones.
    time.sleep(6)  

    with open("Test Prompts/test_get_in_line_position.txt", "r") as f:
        test_prompt = f.read()
        
    message = Message(Roles.SYSTEM, test_prompt)
    view_controller.handle_openai_response(message)
    
    time.sleep(1)
    
    adapter.set_position([0, 0, 50], drone_name="Drone1")
    
    time.sleep(15)      # Kolin: wait them for get in position.
    
    with open("Test Prompts/test_search.txt", "r") as f:
        test_prompt = f.read()
        
    message = Message(Roles.SYSTEM, test_prompt)
    view_controller.handle_openai_response(message)
    
    time.sleep(60)      # Kolin: wait for searching result.
    
    person_found_count = 0
    for object_detector in view_controller.object_detector_container:
        if object_detector.result:
            person_found_count += 1
    
            
    assert person_found_count != 0, "The person should be found by at least one drone."
    print(f"++++++++++++++++++++ Seach seccessful with {person_found_count} times person found by drones. +++++++++++++++++")

    
    sys.exit()

if __name__ == '__main__':
    
    test_search()
