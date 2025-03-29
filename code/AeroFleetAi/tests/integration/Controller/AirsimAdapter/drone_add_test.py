import airsim
import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication

path_root = Path(__file__).parents[4]
sys.path.append(str(path_root))

from Controller.ViewController.view_controller import ViewController


    
"""
Tests the ability of the Airsim Adapter to add a drone
"""
def test_add_drone():
    # Initialize View Controller
    app = QApplication(sys.argv)
    view_controller = ViewController()
        
    adapter = view_controller.airsim_adapter    
    
    # Confirm that Drone2 does not exist before the test
    assert "Drone2" not in adapter.list_drones(), "Drone2 already exists before the test."
    
    adapter.add_drone("Drone2")
    
    # Confirm that Drone2 exists after the test
    assert "Drone2" in adapter.list_drones(), "Drone2 was not added."

    
    sys.exit()

if __name__ == '__main__':
    
    test_add_drone()

