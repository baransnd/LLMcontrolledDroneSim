import airsim
import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication

path_root = Path(__file__).parents[4]
sys.path.append(str(path_root))

from Controller.ViewController.view_controller import ViewController





    
"""
Tests the ability of the Airsim Adapter to delete the person from the environment
"""
def test_delete_object():
    # Initialize View Controller
    app = QApplication(sys.argv)
    view_controller = ViewController()    

    adapter = view_controller.airsim_adapter   
    airsim_client = airsim.MultirotorClient()
    adapter.add_person()
    
    # Confirm that there is a person in the sumulation environment before testing deletion
    assert "Person" in airsim_client.simListAssets(), "Person doesn't exist before the test"
    #assert "Person" in adapter.client.simListSceneObjects("Person")

    adapter.delete_object("Person")
    
    # Confirm person does not exist after being deleted
    assert "Person" not in airsim_client.simListAssets(), "Person was not deleted from the environment"
        
    sys.exit()

if __name__ == '__main__':
    
    test_delete_object()
