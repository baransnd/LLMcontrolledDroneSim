import os

from PySide6.QtCore import QUrl, Slot, QCoreApplication
from PySide6.QtGui import QAction
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel

from View.UI_Windows_Form.MainWindowUiForm import Ui_MainWindow
from View.UI_Windows_Form.MapWindowUiForm import Ui_MapWindow

from View.Widgets.ImageWidget import ImageWidget



class ViewFormatter(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.map_ui = Ui_MapWindow()
        self.map_window = QMainWindow()
        self.map_ui.setupUi(self.map_window)

        self.main_ui = Ui_MainWindow()
        self.main_window = QMainWindow()
        self.main_ui.setupUi(self.main_window)




        '''Set up the MapWindow'''
        # Find and set up the QWebEngineView
        self.webEngineView = self.map_ui.webEngineView
        self.labelCoordinates = self.map_ui.labelCoordinates

        if self.webEngineView is None:
            raise ValueError("QWebEngineView widget not found in UI")

        # Set up the QWebEngineView
        if os.path.exists('View/UI_Windows_Form/open_street_map.html'):
            html_path = os.path.abspath('View/UI_Windows_Form/open_street_map.html')
        else:
            # Kolin: this path is for the integration test.
            html_path = os.path.abspath('../../../../View/UI_Windows_Form/open_street_map.html')
        print(f"Loading HTML from: {html_path}")  # Debugging output
        with open(html_path, "r") as f:
            html = f.read()
        self.webEngineView.setHtml(html)
        '''Set up the MapWindow'''




        '''Set up the MainWindow'''
        self.label_image = ImageWidget()
        self.main_ui.verticalLayout_left.replaceWidget(self.main_ui.label_image, self.label_image)
        self.main_ui.label_image.deleteLater()
        self.main_ui.label_image = self.label_image
        '''Set up the MainWindow'''





    def update_image(self, image):
        self.main_ui.label_image.update_image(image)

    def add_drone_to_ui(self, drone_name):
        # Add a new action for switching view to the new drone
        new_switch_action = QAction(self.main_window)
        new_switch_action.setObjectName("switch_view_" + drone_name)
        new_switch_action.setText(QCoreApplication.translate("MainWindow", drone_name, None))
        self.main_ui.menuChangeView.addAction(new_switch_action)

        # Add a new action for deleting the new drone
        new_delete_action = QAction(self.main_window)
        new_delete_action.setObjectName("delete_" + drone_name)
        new_delete_action.setText(QCoreApplication.translate("MainWindow", drone_name, None))
        self.main_ui.menuDelete_Drone.addAction(new_delete_action)
        
        # Kolin: Add a new action for manual control of the drone.
        new_manual_control_action = QAction(self.main_window)
        new_manual_control_action.setObjectName("manual_control_" + drone_name)
        new_manual_control_action.setText(QCoreApplication.translate("MainWindow", drone_name, None))
        self.main_ui.menuManual_Control.addAction(new_manual_control_action)
        
        # Kolin: Add a new action for get drone position of this drone.
        new_get_position_action = QAction(self.main_window)
        new_get_position_action.setObjectName("get_position_" + drone_name)
        new_get_position_action.setText(QCoreApplication.translate("MainWindow", drone_name, None))
        self.main_ui.menuGet_Drone_Position.addAction(new_get_position_action)
        
        # Kolin: Add a new action for get drone gps of this drone
        new_get_gps_action = QAction(self.main_window)
        new_get_gps_action.setObjectName("get_gps_" + drone_name)
        new_get_gps_action.setText(QCoreApplication.translate("MainWindow", drone_name, None))
        self.main_ui.menuGet_Drone_GPS.addAction(new_get_gps_action)

        return new_switch_action, new_delete_action, new_manual_control_action, new_get_position_action, new_get_gps_action

    def delete_drone_from_ui(self, drone_name):
        # Delete from camera switching menu.
        switch_action = self.main_ui.menuChangeView.findChild(QAction, "switch_view_" + drone_name)
        self.main_ui.menuChangeView.removeAction(switch_action)

        # Delete from drone deletion menu.
        delete_action = self.main_ui.menuDelete_Drone.findChild(QAction, "delete_" + drone_name)
        self.main_ui.menuDelete_Drone.removeAction(delete_action)

