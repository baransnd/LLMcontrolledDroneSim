import airsim
import time
import sys
from unittest.mock import Mock, MagicMock
from pathlib import Path

path_root = Path(__file__).parents[4]
sys.path.append(str(path_root))

from Controller.DroneController.AirsimAdapter.airsim_adapter import AirsimAdapter
from Controller.DroneController.AirsimAdapter.airsim_adapter import DroneSurveyor
from Controller.DroneController.AirsimAdapter.airsim_adapter import ObjectDetectionAPI4AI
from Controller.ViewController.view_controller import ViewController

"""
@Isik: Tests the ability of the Airsim Adapter to add a new drone with the given name to the simulation environment.
"""
def test_add_drone():
    # Initialize Airsim Client and Adapter
    mock_view_controller = Mock()
    mock_drone_surveyor = MagicMock(spec=DroneSurveyor)
        
    # Initialize drones_count to simulate state, this causes an error
    # if not handled
    mock_drone_surveyor.drones_count = 0
        
    # Initialize AirsimAdapter with mocks
    adapter = AirsimAdapter(mock_view_controller, mock_drone_surveyor)
    
    drone_name = 'test_drone'
    existing_drones_before = set(adapter.list_drones())
    
    adapter.add_drone(drone_name)

    # Wait for the drone to be added
    time.sleep(2)  

    drones_after_addition = set(adapter.list_drones())
    assert drones_after_addition == existing_drones_before | {drone_name}, "The drone list after addition should be the initial list plus the new drone."

    print("Drones currently in the environment:")
    print(drones_after_addition)

if __name__ == '__main__':
    
    test_add_drone()
