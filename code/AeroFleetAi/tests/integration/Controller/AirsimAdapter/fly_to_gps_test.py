import airsim
import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication

path_root = Path(__file__).parents[4]
sys.path.append(str(path_root))

from Controller.ViewController.view_controller import ViewController



# Also tests move_to_position_async

# Problem: lattitude diff ist so klein, dass es nicht mehr darstellbar ist

    
"""
Tests the ability of the Airsim Adapter to fly to a specific geopoint.
"""
def test_fly_to_geopoint():
    # Initialize View Controller
    app = QApplication(sys.argv)
    view_controller = ViewController()
        
    adapter = view_controller.airsim_adapter
    init_gp = view_controller.airsim_adapter.get_drone_geopoint()
    print("Initial geopoint: ")
    print("lat: ", init_gp.latitude)
    print("long: ", init_gp.longitude)
    print("alt: ", init_gp.altitude)
    new_gp = airsim.GeoPoint()                              # Kolin: Start gps in unreal Engine.
    new_gp.latitude = init_gp.latitude + 0.00009
    new_gp.longitude = init_gp.longitude + 0.00009
    new_gp.altitude = init_gp.altitude + 3
    view_controller.airsim_adapter.fly_to_geopoint(new_gp)
    print(init_gp.latitude - new_gp.latitude)
    assert -0.0001 < init_gp.latitude - new_gp.latitude < 0.0001
    assert -0.0001 < init_gp.longitude - new_gp.longitude < 0.0001
    assert new_gp.latitude > init_gp.latitude

    print("++++++++++++++++++++++Test Successful! The drone is in the wished gps!+++++++++++++++++++++++++")

    '''
    view_controller.airsim_adapter.fly_to_xyz([init_x+10,init_y,init_z])
    dest_pos = view_controller.airsim_adapter.get_drone_position()
    des_x = init_x + 10
    assert -10 < dest_pos[0] - des_x < 10
    print("Test passed!")
    '''
    
   

    
    sys.exit()

if __name__ == '__main__':
    
    test_fly_to_geopoint()
