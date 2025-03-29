# -*- coding: utf-8 -*-
import keyboard
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
    start_pos = view_controller.airsim_adapter.get_drone_position()
          
    time.sleep(2)
    with open("Test Prompts/test_manual_control.txt", "r") as f:
        test_prompt = f.read()
        
    message = Message(Roles.SYSTEM, test_prompt)
    view_controller.handle_openai_response(message)
    
    # now press w, s, a, d, q, e, y, x, w, w and then p to quit.
    
    
    
    while not keyboard.is_pressed('p'):
        time.sleep(1)
        
    end_position = view_controller.airsim_adapter.get_drone_position()
        
    print(f"++++++++++++++++++++ {end_position[0] - start_pos[0]} +++++++++++++++++")
    assert 9 < end_position[0] - start_pos[0] < 11, "The drone should be moved 10m forward."
    print(f"++++++++++++++++++++ Test seccessful, the drone is in right position! +++++++++++++++++")
        
    sys.exit()

if __name__ == '__main__':
    
    test_search()
