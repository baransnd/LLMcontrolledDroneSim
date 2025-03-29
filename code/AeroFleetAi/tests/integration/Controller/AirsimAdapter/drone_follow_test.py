from unittest import result
import airsim
import time
import sys
from unittest.mock import Mock, MagicMock
from pathlib import Path
from PySide6.QtCore import Slot, QThread, QMetaObject, Qt, QCoreApplication, QUrl, Q_ARG
from PySide6.QtWidgets import QApplication
import math

path_root = Path(__file__).parents[4]
sys.path.append(str(path_root))


from Controller.ViewController.view_controller import ViewController


def test_follow():
    app = QApplication(sys.argv)
    view_controller = ViewController()
        
    adapter = view_controller.airsim_adapter   
    
    # add a second drone if it does not already exist.
    if "Drone2" not in adapter.list_drones():
        adapter.add_drone("Drone2")
    print("added follower drone")
    
    print("setting position of the new drone")
    spawn_position = adapter.get_drone_position("Drone1")
    spawn_position[0] += 5
    adapter.set_position(spawn_position,0,"Drone2")
    print("position set")
    
    
    
    
    
    print("moving drone 2")
    target_coordinate = adapter.get_drone_position("Drone2")
    target_coordinate[0] += 100
    target_coordinate[1] += 40
    target_coordinate[2] -= 60
    adapter.fly_to_xyz_asnychron(target_coordinate, "Drone2")
    
    print("giving follow command")
    adapter.follow_drone("Drone1", "Drone2",10,30)
    print("follow command given")
    
    
    
    
    print("wait over")
    
    drone1_pos = adapter.client.simGetVehiclePose("Drone1").position
    drone2_pos = adapter.client.simGetVehiclePose("Drone2").position
    
    distance_between = math.dist(drone1_pos, drone2_pos)
    print(drone1_pos, drone2_pos, distance_between)
    assert distance_between < 20 ,"The following drone should be in 20 meters of the followed drone."
    
 
    
if __name__ == '__main__':
    
    test_follow()
        
    
    