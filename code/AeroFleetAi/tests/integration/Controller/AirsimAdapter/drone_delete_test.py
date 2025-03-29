import airsim
import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication

path_root = Path(__file__).parents[4]
sys.path.append(str(path_root))

from Controller.ViewController.view_controller import ViewController





    
"""
Tests the ability of the Airsim Adapter to delete a drone.
"""
def test_delete_drone():
    # Initialize View Controller
    app = QApplication(sys.argv)
    view_controller = ViewController()
        
    adapter = view_controller.airsim_adapter    
    adapter.add_drone("Drone2")
    
    # Confirm that Drone2 exists before the test
    assert "Drone2" in adapter.list_drones(), "Drone2 does not exist before the test."
    
    adapter.delete_object("Drone2")
    
    # Confirm that Drone2 does not exist after the test
    assert "Drone2" not in adapter.list_drones(), "Drone2 was not removed."

    
    sys.exit()

if __name__ == '__main__':
    
    test_delete_drone()
