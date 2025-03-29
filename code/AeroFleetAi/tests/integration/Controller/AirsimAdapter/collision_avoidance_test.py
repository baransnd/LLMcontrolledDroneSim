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
def test_collision_avoidance():
    # Initialize View Controller
    app = QApplication(sys.argv)
    view_controller = ViewController()
    result = False
          
    time.sleep(2)
    with open("Test Prompts/test_collision_avoidence.txt", "r") as f:
        test_prompt = f.read()
        
    message = Message(Roles.SYSTEM, test_prompt)
    view_controller.handle_openai_response(message)

    time.sleep(30)                              # Kolin: time for the test prosess.
    
    while not result:                              # Kolin: report the drone, if it get it position.      
        current_pos = view_controller.airsim_adapter.get_drone_position()
        target_x = 40               # Kolin: test destination location
        target_y = 50
        delta_x = target_x - current_pos[0]
        delta_y = target_y - current_pos[1]
                    
        if (-10 < delta_x < 10) and (-10 < delta_y < 10):
            result = True
            message = "Drone1: get in position!!"
            print(message)                        
                    
        time.sleep(2)
        
    assert result == True, "The drone should be in right position."
    print(f"++++++++++++++++++++ Test seccessful, the drone is in right position! +++++++++++++++++")
    

    sys.exit()

if __name__ == '__main__':
    
    test_collision_avoidance()
