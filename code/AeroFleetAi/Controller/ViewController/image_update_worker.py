

import time
from PySide6.QtCore import QObject, Signal, Slot
import numpy as np
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Signal
import os
import cv2



from Controller.DroneController.OpenAIAdapter.openai_adapter import OpenAiAdapter


# Diese Klasse ist als Worker in einem QThread gedacht, der in kurzen zeitlichen Abstaenden das Kamerabild aktualisiert, ohne den MainThread zu blockieren.
class ImageUpdateWorker(QObject):
    
    image_signal = Signal(QPixmap)
    finished = Signal()



    def __init__(self, view_controller, airsim_client):
        super().__init__()
        self.view_controller = view_controller
        self.stopped = False
        self.client = airsim_client
        self.current_drone_name = "Drone1"

        

    @Slot()
    def update(self):
        
        while not self.stopped:
            # Retrieve camera image from view controller
            img_rgb = self.view_controller.get_image(self.client, self.current_drone_name)
            
            # BGR zu RGB konvertieren
            img_rgb = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2RGB)


            
            # Adjust image to QPixmap
            height, width, channel = img_rgb.shape
            bytes_per_line = 3 * width
            q_img = QImage(img_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
            q_pixmap = QPixmap.fromImage(q_img)

            # Send QPixmap out
            self.image_signal.emit(q_pixmap)

            