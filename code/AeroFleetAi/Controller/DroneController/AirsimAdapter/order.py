
from PySide6.QtCore import QObject, Signal, Slot, QMetaObject, Qt, Q_ARG
import airsim


from Controller.DroneController.AirsimAdapter.airsim_adapter import AirsimAdapter
from Controller.DroneController.Utils.message import Roles
from Controller.DroneController.Utils.message import Message



class Order(QObject):
    
    execution_done_signal = Signal(Message)
    finished = Signal()

    def __init__(self, drone_instructions, view_controller, drone_surveyor):
        super().__init__()
        self.drone_instructions = drone_instructions
        self.view_controller = view_controller
        self.airsim_adapter = AirsimAdapter(view_controller, drone_surveyor)    # Kolin: AirsimAdapter need now view_controller to display the results on the UI.

    @Slot()
    def execute(self):
        try:
            exec(self.drone_instructions)
            self.execution_done_signal.emit(Message(Roles.SYSTEM, "Finished execution"))
        except Exception as e:
            error_message = f"Execution Failed! An error occurred while executing the code: {e}"
            self.execution_done_signal.emit(Message(Roles.SYSTEM, error_message))
        finally:
            self.finished.emit()
    

    def get_involved_drones(self):
        pass
    
    
    def is_done(self):
        pass
    

    def get_result(self):
        pass