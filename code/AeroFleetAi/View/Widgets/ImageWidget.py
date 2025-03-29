#import numpy as np
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QLabel
#import airsim


class ImageWidget(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setScaledContents(True)
        #self.airsim_client = airsim.MultirotorClient()
        #self.airsim_client.confirmConnection()

    def update_image(self, pixmap):
        #img_np = self.get_image()
        #height, width, channel = img_np.shape
        #bytes_per_line = 3 * width
        #q_img = QImage(img_np.data, width, height, bytes_per_line, QImage.Format_RGB888)
        #self.setPixmap(QPixmap.fromImage(q_img))
        self.setPixmap(pixmap)


    # Get image from AirSim . Es muss hier geändert werden eventuell wegen der Verbindung airsim.MultirotorClient()
#    def get_image(self):
#        responses = self.airsim_client.simGetImages(
#            [airsim.ImageRequest("0", airsim.ImageType.Scene, False, False) ])
#        response = responses[0]
#        img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8)
#        img_rgb = img1d.reshape(response.height, response.width, 3)  # Change 4 to 3
#        return img_rgb