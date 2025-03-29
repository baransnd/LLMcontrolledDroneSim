import airsim
import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication

path_root = Path(__file__).parents[4]
sys.path.append(str(path_root))

from Controller.ViewController.view_controller import ViewController





    
"""
Tests the ability of the Airsim Adapter to place a person as a search object.
"""
def test_place_object():
    # Initialize View Controller
    app = QApplication(sys.argv)
    view_controller = ViewController()    

    adapter = view_controller.airsim_adapter   
    airsim_client = airsim.MultirotorClient()
    
    # Confirm that there is no person in the sumulation environment before adding it
    assert "Person" not in airsim_client.simListAssets(), "Person already exists before the test"
    #assert "Person" not in adapter.client.simListSceneObjects("Person")

    adapter.add_person()
    
    # Confirm person exists after being added
    assert "Person" in airsim_client.simListAssets(), "Person was not added to the environment"
        
    sys.exit()

if __name__ == '__main__':
    
    test_place_object()
