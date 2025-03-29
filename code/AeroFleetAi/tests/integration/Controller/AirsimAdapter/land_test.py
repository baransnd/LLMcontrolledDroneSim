import airsim
import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
import time

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
    #view_controller.airsim_adapter.takeoff() # technically shouldnt depend on other functions, but here, it has to
    #time.sleep(5)
    init_pos = view_controller.airsim_adapter.get_drone_position()
    print("Initial pos: ", init_pos)
    view_controller.airsim_adapter.fly_to_xyz([0,0,35])
    time.sleep(5)
    view_controller.airsim_adapter.land()
    
    new_pos = view_controller.airsim_adapter.get_drone_position()
    print("New pos: ", new_pos)
    assert new_pos[2] > init_pos[2]
    print("++++++++++++++++++++Test passed! Landed!++++++++++++++++++++++++")

    
    sys.exit()

if __name__ == '__main__':
    
    test_takeoff()
