from queue import Full
from types import SimpleNamespace
import re
from PySide6.QtCore import Slot, QThread, QMetaObject, Qt, QCoreApplication, QUrl, Q_ARG
from Controller.DroneController.AirsimAdapter.instruction_worker import InstructionWorker
from Controller.DroneController.Utils.message import Message
from Controller.DroneController.Utils.message import Roles

import math
import numpy as np
import json
import time



class CodeExecutor:
    
    def __init__(self, view_controller, drone_surveyor):
        self.view_controller = view_controller
        self.drone_surveyor = drone_surveyor
        self.code_block_regex = re.compile(r"----------------(.*?)----------------------------------------", re.DOTALL)
        self.threads = []
        self.workers = []
        


    def extract_and_run(self, code_text):

        code_blocks = self.extract_python_code(code_text)
        print(code_blocks)
        if code_blocks is not None:
            for drone_name, code in vars(code_blocks).items():          
                # Create worker thread
                worker = InstructionWorker(code, self.view_controller, self.drone_surveyor)    # Kolin: AirsimAdapter in the InstructionWorker class now needs view_controller to display the results on the UI and a drone_surveyor                
                thread = QThread()                                                 # Within an object_detector to receive a person_detected signal.
                worker.moveToThread(thread)
            
                #self.thread.started.connect(self.worker.execute)
                worker.finished.connect(thread.quit)
                worker.finished.connect(worker.deleteLater)
                thread.finished.connect(thread.deleteLater)
                
                self.threads.append(thread)         # Kolin: Save the thread and worker and make them not deleted earlier.
                self.workers.append(worker)
                
                thread.start()
                QMetaObject.invokeMethod(worker, "execute", Qt.QueuedConnection)

                worker.execution_done_signal.connect(self.view_controller.display)
                

        else:
            self.view_controller.display(Message(Roles.SYSTEM, "There was no code to execute."))
            


    def extract_python_code(self, content):
        blocks = self.code_block_regex.findall(content)
        
        code_blocks = SimpleNamespace()
        for block in blocks:
            block = block.replace("```", "")
            block = block.replace("python", "")
            parts = block.split('----------------')
            drone_name = parts[0].strip()
            code = parts[1]
            setattr(code_blocks, drone_name, code)
            
        return code_blocks            
           
        
        
