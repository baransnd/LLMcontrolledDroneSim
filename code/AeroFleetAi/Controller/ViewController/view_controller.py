from ast import Lambda
from cgitb import text
import os
import re

from PySide6.QtCore import Slot, QThread, QMetaObject, Qt, QCoreApplication, QUrl, Q_ARG
from PySide6.QtMultimedia import QAudioInput, QMediaCaptureSession, QMediaRecorder


from Controller.DroneController.OpenAIAdapter.openai_adapter import OpenAiAdapter
from Controller.DroneController.OpenAIAdapter.openai_ask_worker import OpenAiAskWorker
from Controller.DroneController.OpenAIAdapter.manual_ai_ask_worker import ManualAiAskWorker
from Controller.DroneController.AirsimAdapter.airsim_adapter import AirsimAdapter
from Controller.DroneController.AirsimAdapter.code_executor import CodeExecutor
from Controller.ViewController.view_formatter import ViewFormatter
from Controller.ViewController.image_update_worker import ImageUpdateWorker
from Controller.DroneController.Utils.message import Message
from Controller.DroneController.Utils.message import Roles
from Controller.DroneController.AirsimAdapter.object_detector import ObjectDetectionAPI4AI
from Controller.DroneController.AirsimAdapter.drone_surveyor import DroneSurveyor
from Controller.DroneController.OpenAIAdapter.speech_to_text_adapter import SpeechToTextAdapter

import airsim
import numpy as np


class ViewController:
    def __init__(self):
        self.view_formatter = ViewFormatter()
        self.openai_adapter = OpenAiAdapter()                               # Kolin: Url of local LLM deleted. Want to use openAi
        self.airsim_client = airsim.MultirotorClient()        
        self.object_detector_container = []
        self.airsim_adapters_container = []
        self.threads_container = []

        
        self.drone_surveyor = DroneSurveyor(self.object_detector_container, self)
        self.code_executor = CodeExecutor(self, self.drone_surveyor)        # Kolin: The AirsimAdapter now needs the view_controller as an argument to show some results of the functions in the
                                                                            # AirsimAdapter, and drone_surveyor within an object_detector to receive the person_detected signal.
        


        self.current_drone_shown = "Drone1"
        self.add_drone_to_ui("Drone1")

        self.airsim_adapter = AirsimAdapter(self, self.drone_surveyor)              # Kolin: Use the AirsimAdapter here to adjust the start location.
        self.airsim_adapter.set_position([0, 0, 0])                                # Kolin: Set the start position.
        self.drone_surveyor.set_start_gps(self.airsim_adapter.get_drone_geopoint()) # Kolin: Set the start gps for drone_surveyor.
        
        self.latitude = 49.012921                                          # Kolin: Start gps in real world: Schloss Karlsruhe.
        self.longitude = 8.404318
        
        self.unreal_start_geopoint = airsim.GeoPoint()                              # Kolin: Start gps in unreal Engine.
        self.unreal_start_geopoint.latitude = 47.64146799999743
        self.unreal_start_geopoint.longitude = -122.140165
        self.unreal_start_geopoint.altitude = 122




        # Connect functions to UI buttons
        self.view_formatter.main_ui.lineEdit_input.returnPressed.connect(self.on_return_main_window_pressed)
        self.view_formatter.main_ui.actionChange_Map.triggered.connect(self.show_map_window)
        self.view_formatter.main_ui.actionTest_One.triggered.connect(lambda: self.code_test(1))
        self.view_formatter.main_ui.actionTest_Two.triggered.connect(lambda: self.code_test(2))
        self.view_formatter.main_ui.pushButton_2.clicked.connect(self.toggle_audio_recording)

        self.view_formatter.main_ui.actionAdd_one_Drone.triggered.connect(self.airsim_adapter.add_drone)
        self.view_formatter.main_ui.actionAdd_two_Drone.triggered.connect(lambda: self.airsim_adapter.add_multiple_drones(2))
        self.view_formatter.main_ui.actionAdd_three_Drone.triggered.connect(lambda: self.airsim_adapter.add_multiple_drones(3))
        self.view_formatter.main_ui.actionAdd_four_Drone.triggered.connect(lambda: self.airsim_adapter.add_multiple_drones(4))
        self.view_formatter.main_ui.actionAdd_five_Drone.triggered.connect(lambda: self.airsim_adapter.add_multiple_drones(5))
        self.view_formatter.main_ui.actionList_Drones.triggered.connect(self.airsim_adapter.list_drones)

        self.view_formatter.main_ui.actionFree_Camera.triggered.connect(self.airsim_adapter.free_camera)



        self.view_formatter.map_ui.webEngineView.titleChanged.connect(self.on_new_coordinate_clicked)
        self.view_formatter.map_ui.pushButtonNext.clicked.connect(self.on_next_clicked)
        self.view_formatter.map_ui.pushButtonCancel.clicked.connect(self.on_cancel_clicked)



        # Create worker threads
        self.openai_ask_worker = OpenAiAskWorker(self.openai_adapter)
        self.openai_ask_thread = QThread()
        self.openai_ask_worker.moveToThread(self.openai_ask_thread)
            
        self.openai_ask_worker.finished.connect(self.openai_ask_thread.quit)
        self.openai_ask_worker.finished.connect(self.openai_ask_worker.deleteLater)
        self.openai_ask_thread.finished.connect(self.openai_ask_thread.deleteLater)
        self.openai_ask_thread.start()
        
        # Connect functions to signals from worker threads
        self.openai_ask_worker.response_signal.connect(self.handle_openai_response)
        

        # Kolin: Create new threads for handling the return value between airsim_adapter and openAi
        self.openai_communicate_worker = OpenAiAskWorker(self.openai_adapter)
        self.openai_communicate_thread = QThread()
        self.openai_communicate_worker.moveToThread(self.openai_communicate_thread)
            
        self.openai_communicate_worker.finished.connect(self.openai_communicate_thread.quit)
        self.openai_communicate_worker.finished.connect(self.openai_communicate_worker.deleteLater)
        self.openai_communicate_thread.finished.connect(self.openai_communicate_thread.deleteLater)
        self.openai_communicate_thread.start()
        
        # Connect functions to signals from worker threads
        self.openai_communicate_worker.response_signal.connect(self.handle_openai_response)


        # Kolin: create a thread for drone_surveyor
        self.drone_surveyor_thread = QThread()
        self.drone_surveyor.moveToThread(self.drone_surveyor_thread)

        self.drone_surveyor_thread.start()




        # Set up a timer in a new qthread to update the image periodically
        self.image_update_worker = ImageUpdateWorker(self, self.airsim_client) 
        self.image_update_thread = QThread()
        self.image_update_worker.moveToThread(self.image_update_thread)

        self.image_update_worker.finished.connect(self.image_update_thread.quit)
        self.image_update_worker.finished.connect(self.image_update_worker.deleteLater)
        self.image_update_thread.finished.connect(self.image_update_thread.deleteLater)
        self.image_update_thread.start()

        self.image_update_worker.image_signal.connect(self.view_formatter.update_image)    

        QMetaObject.invokeMethod(self.image_update_worker, "update", Qt.QueuedConnection)
        

        # Create an openai audio recording and transcription thread
        self.speech_to_text_worker = SpeechToTextAdapter()
        self.speech_to_text_thread = QThread()
        self.speech_to_text_worker.moveToThread(self.speech_to_text_thread)
            
        self.speech_to_text_worker.finished.connect(self.speech_to_text_thread.quit)
        self.speech_to_text_worker.finished.connect(self.speech_to_text_worker.deleteLater)
        self.speech_to_text_thread.finished.connect(self.speech_to_text_thread.deleteLater)
        self.speech_to_text_thread.start()
        
        self.speech_to_text_worker.status_signal.connect(self.display)
        self.speech_to_text_worker.response_signal.connect(self.handle_audio_response)





        # Show welcome message
        self.display(Message(Roles.ASSISTANT, "Welcome to the AirSim chatbot! I am ready to help you with your AirSim questions and commands."))




    def show_main_window(self):
        self.view_formatter.main_window.show()

    def show_map_window(self):
        self.view_formatter.map_window.show()


    @Slot()
    def display(self, message):
        if message.role == Roles.SYSTEM:
            self.view_formatter.main_ui.textBrowser.append(f"System: {message.content}\n\n")
        elif message.role == Roles.USER:
            self.view_formatter.main_ui.textBrowser.append(f"User: {message.content}\n\n")
        elif message.role == Roles.ASSISTANT:
            self.view_formatter.main_ui.textBrowser.append(f"Assistant: {message.content}\n\n")




    @Slot()
    def get_image(self, client, drone_name='Drone1'):
        # Retrieve camera image from airsim
        responses = client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)], vehicle_name=drone_name)
        response = responses[0]
        img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8)
        img_rgb = img1d.reshape(response.height, response.width, 3)  # Change 4 to 3

        return img_rgb
        


    @Slot()
    def on_return_main_window_pressed(self):
        prompt = self.view_formatter.main_ui.lineEdit_input.text()
        self.view_formatter.main_ui.lineEdit_input.clear()

        if prompt:
            self.display(Message(Roles.USER, prompt))            
            QMetaObject.invokeMethod(self.openai_ask_worker, "ask", Qt.QueuedConnection, Q_ARG(str, prompt))



    @Slot(str)
    def handle_audio_response(self, response):
        # Set the transcription into the user input field to editable
        self.view_formatter.main_ui.lineEdit_input.setText(response.content)



    @Slot(str)
    def handle_openai_response(self, response):
        self.display(response)
        
        self.code_executor.extract_and_run(response.content)



    @Slot(Message)
    def handle_code_execution_result(self, result):
        self.display(result)


    '''
    @Kolin: if clicked on the map window at a new position, the drones will move to this new position(search area)
    '''
    @Slot(str)
    def on_new_coordinate_clicked(self, title):
        coordinates = title.split(",")
        coordinates[0] = float(coordinates[0].strip())
        coordinates[1] = float(coordinates[1].strip())
        
        delta_x, delta_y = self.airsim_adapter.calculate_deltas_in_meters(self.latitude, self.longitude, coordinates[0], coordinates[1])
        print(f"x: {delta_x}, y: {delta_y}, z: 0")

        drone_list = self.airsim_adapter.list_drones()
        ring = [
            [delta_x - 20, delta_y, 0],
            [delta_x + 20, delta_y, 0],
            [delta_x - 10, delta_y - 10, 0],
            [delta_x + 10, delta_y - 10, 0],
            [delta_x - 10, delta_y + 10, 0],
            [delta_x + 10, delta_y + 10, 0]
            ]
        QMetaObject.invokeMethod(self.drone_surveyor, "start_drone_arrives_count", Qt.QueuedConnection, Q_ARG(int, len(drone_list)))    # Kolin: start the counter with exactly the drone amounts.


        for drone, pos in zip(drone_list, ring):
            # Kolin: Create a new thread for the movement of the drones to new location for the sake of not blocking the main thread.
            airsim_adapter = AirsimAdapter(self, self.drone_surveyor) 
            thread = QThread()
            airsim_adapter.moveToThread(thread)

            thread.finished.connect(thread.deleteLater)
            self.airsim_adapters_container.append(airsim_adapter)
            self.threads_container.append(thread)
            thread.start()   

            QMetaObject.invokeMethod(airsim_adapter, "fly_to_xyz_with_collision_avoidance_and_get_in_position_report", Qt.QueuedConnection, Q_ARG('QVariantList', pos), Q_ARG(str, drone))
        
        message = "Latitude: " + "{:.6f}".format(coordinates[0]) + ", Longitude: " + "{:.6f}".format(coordinates[1])

        self.view_formatter.map_ui.labelCoordinates.setText(QCoreApplication.translate("MapWindow", message, None))
        print("Der Titel der Seite wurde geaendert: " + title)



    #TODO: Implement the next button
    @Slot()
    def on_next_clicked(self):
        self.view_formatter.map_window.hide()

        #Die Mittlepunktkoordinaten wird eingesetzt

        self.view_formatter.main_window.show()



    @Slot()
    def on_cancel_clicked(self):
        self.view_formatter.map_window.close()
        #self.main_window.show()


    '''
    @Kolin: the implementation for the manual control buttom.
    '''
    def enable_manual_control(self, drone_name):
        # Erstelle den Code-Text im bestimmten Format
        code_text = f'''----------------{drone_name}----------------\nself.airsim_adapter.manual_controll("{drone_name}")\n----------------------------------------'''
        # Erstelle die Nachricht mit dem angegebenen Format
        message = Message(Roles.SYSTEM, code_text)
        # Rufe handle_openai_response mit der Nachricht auf
        self.handle_openai_response(message)


    def toggle_audio_recording(self):
        QMetaObject.invokeMethod(self.speech_to_text_worker, "toggle_audio_recording", Qt.QueuedConnection)


    '''
    @Kolin: add the instructions bar on the UI for each new drone.
    '''
    def add_drone_to_ui(self, drone_name):
        new_switch_action, new_delete_action, new_manual_control_action, new_get_position_action, new_get_gps_action = self.view_formatter.add_drone_to_ui(drone_name)  # Kolin: manual control added.
        new_switch_action.triggered.connect(lambda: self.airsim_adapter.switch_to_camera(drone_name))
        new_delete_action.triggered.connect(lambda: self.airsim_adapter.delete_drone(drone_name))
        new_manual_control_action.triggered.connect(lambda: self.enable_manual_control(drone_name))
        new_get_position_action.triggered.connect(lambda: self.display_return_value_of_functions_in_airsim_adapter("get_drone_postion", drone_name))
        new_get_gps_action.triggered.connect(lambda: self.display_return_value_of_functions_in_airsim_adapter("get_drone_gps", drone_name))
        
        self.create_new_picture_analyse_thread(drone_name)

    def delete_drone_from_ui(self, drone_name):
        self.view_formatter.delete_drone_from_ui(drone_name)


    def on_quit(self):
        print("Received about to quit signal")
        # Quit the image update thread
        self.image_update_worker.finished.emit()
        #self.openai_ask_worker.finished.emit()
        self.manual_ai_ask_worker.finished.emit()
     
        
    '''
    @Kolin: test bar on the UI for the reading of test_prompts.
    '''
    def code_test(self, test_number):
        try:
            message = None
            test_prompt = None
            if test_number == 1:                
                with open("Controller/DroneController/OpenAIAdapter/Prompts/test_1.txt", "r") as f:
                    test_prompt = f.read()
                                            
            elif test_number == 2:
                with open("Controller/DroneController/OpenAIAdapter/Prompts/test_2.txt", "r") as f:
                    test_prompt = f.read()
            
            message = Message(Roles.SYSTEM, test_prompt)
            self.handle_openai_response(message)
            
        except Exception as e:
            print(f"An error occurred during the code test: {e}")
            
    '''
    @Kolin: display the return values of some get functions on the screen.
    '''
    def display_return_value_of_functions_in_airsim_adapter(self, funtion_name, drone_name='Drone1'):
        return_value = None
        if funtion_name == "get_drone_postion":
            return_value = self.airsim_adapter.get_drone_position(drone_name)
            message =f"The position(Vector 3D) of the drone {drone_name} is: \n [ x: {return_value[0]} ]\n [ y: {return_value[1]} ] \n [ z: {return_value[2]} ]"
            
        elif funtion_name == "get_drone_gps":
            return_value = self.airsim_adapter.get_drone_geopoint(drone_name)
            message =f"The GPS of the drone {drone_name} is: \n [ latitude: {return_value.latitude} ] \n [ longitude: {return_value.longitude} ] \n [ altitude: {return_value.altitude} ]"
        
        self.display(Message(Roles.SYSTEM, message))        
        print(message) 
        
    '''
    @Kolin: add a new picture analyse thread for each new drone.
    '''
    def create_new_picture_analyse_thread(self, drone_name):
        new_airsim_client = airsim.MultirotorClient()
        new_object_detector = ObjectDetectionAPI4AI(new_airsim_client, api_mode='demo', rapidapi_key='a73564f61cmsh64e5459995ac69fp12616cjsn49a349a54798')
        
        new_object_detector_thread = QThread()
        new_object_detector.moveToThread(new_object_detector_thread)

        new_object_detector.finished.connect(new_object_detector_thread.quit)
        new_object_detector.finished.connect(new_object_detector.deleteLater)
        new_object_detector_thread.finished.connect(new_object_detector_thread.deleteLater)
        
        self.object_detector_container.append(new_object_detector)
        self.threads_container.append(new_object_detector_thread)
        
        self.drone_surveyor.link_object_detector_to_self()

        new_object_detector_thread.start() 

        QMetaObject.invokeMethod(new_object_detector, "take_picture_and_analyse", Qt.QueuedConnection, Q_ARG(str, drone_name))
            
            