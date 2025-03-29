import airsim
import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
import time
import math

path_root = Path(__file__).parents[4]
sys.path.append(str(path_root))

from Controller.ViewController.view_controller import ViewController



# Problem: test starts with takeoff, starting position should be from the ground

    
"""
Tests the ability of the Airsim Adapter to take off the drone
"""
def test_takeoff():
    # Initialize View Controller
    app = QApplication(sys.argv)
    view_controller = ViewController()
    adapter = view_controller.airsim_adapter
    view_controller.airsim_adapter.fly_to_xyz([0,0,35])
    time.sleep(5)
    view_controller.airsim_adapter.land()       # Kolin: first landing.
    time.sleep(15)
    init_pos = adapter.get_drone_position()
    print("Initial pos: ", init_pos)
    adapter.takeoff()
    time.sleep(5)
    new_pos = adapter.get_drone_position()
    print("New pos: ", new_pos)
    assert new_pos[2] < init_pos[2]
    print("Test passed!")

    
    sys.exit()

if __name__ == '__main__':
    
    test_takeoff()
