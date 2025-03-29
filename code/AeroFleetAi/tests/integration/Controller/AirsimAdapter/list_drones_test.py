import airsim
import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
import time

path_root = Path(__file__).parents[4]
sys.path.append(str(path_root))

from Controller.ViewController.view_controller import ViewController



# Problem: test starts with takeoff/starting position. No need to move at all.

    
"""
Tests the ability of the Airsim Adapter to list available drones correctly
"""
def test_list_drones():
    # Initialize View Controller
    app = QApplication(sys.argv)
    view_controller = ViewController()
    adapter = view_controller.airsim_adapter
    init_list = adapter.list_drones()
    print("Init list: ", init_list)
    assert len(init_list) == 1 and "Drone1" in init_list and "Drone2" not in init_list

    view_controller.airsim_adapter.add_drone("Drone2")
    new_list = view_controller.airsim_adapter.list_drones()
    print("New list: ", new_list)
    assert len(new_list) == 2 and "Drone1" in new_list and "Drone2" in new_list
    print("Test passed!")

    
    sys.exit()

if __name__ == '__main__':
    
    test_list_drones()
