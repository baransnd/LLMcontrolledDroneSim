

from PySide6.QtCore import QObject, Signal, Slot


from Controller.DroneController.OpenAIAdapter.openai_adapter import OpenAiAdapter
from Controller.DroneController.Utils.message import Roles
from Controller.DroneController.Utils.message import Message





# Diese Klasse ist als Worker in einem QThread gedacht, der eine Anfrage an OpenAI sendet, ohne den MainThread zu blockieren.
# This class serves as a worker in a QThread that sends a request to OpenAI without blocking the main thread.
class OpenAiAskWorker(QObject):
    
    response_signal = Signal(Message)
    finished = Signal()



    def __init__(self, openai_adapter):
        super().__init__()
        self.openai_adapter = openai_adapter
        

    @Slot(str)
    def ask(self, prompt):
        # Your long-running task goes here ...
        response = self.openai_adapter.ask(prompt)
#        self.response_signal.emit(Message(Roles.ASSISTANT, response)) # fix commented code
        self.response_signal.emit(response)
        
        



