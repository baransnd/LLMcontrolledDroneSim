import airsim
import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication

path_root = Path(__file__).parents[4]
sys.path.append(str(path_root))

from Controller.ViewController.view_controller import ViewController



# Also tests move_to_position_async


    
"""
Tests the ability of the Airsim Adapter to fly to a specific xyz position.
"""
def test_fly_to_xyz():
    # Initialize View Controller
    app = QApplication(sys.argv)
    view_controller = ViewController()
        
    adapter = view_controller.airsim_adapter
    current_pos = view_controller.airsim_adapter.get_drone_position()
    init_x =  current_pos[0]
    init_y =  current_pos[1]
    init_z =  current_pos[2]
    view_controller.airsim_adapter.fly_to_xyz([init_x+10,init_y,init_z])
    dest_pos = view_controller.airsim_adapter.get_drone_position()
    des_x = init_x + 10
    assert -10 < dest_pos[0] - des_x < 10
    print("++++++++++++++++++++++++++Test passed! The drone is in the destination position!+++++++++++++++++++++++++++++++++++")
    
   

    
    sys.exit()

if __name__ == '__main__':
    
    test_fly_to_xyz()
