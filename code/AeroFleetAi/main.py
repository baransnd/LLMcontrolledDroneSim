import sys
from PySide6.QtCore import QMetaObject, Qt, Q_ARG
from PySide6.QtWidgets import QApplication
from Controller.ViewController.view_controller import ViewController



if __name__ == '__main__':
    app = QApplication(sys.argv)
    controller = ViewController()


    # Start the application
    with open("Controller/DroneController/OpenAIAdapter/Prompts/example_prompts_v2.txt", "r") as f:
        example_prompt = f.read()

    controller.show_map_window()

    #QMetaObject.invokeMethod(controller.openai_ask_worker, "ask", Qt.QueuedConnection, Q_ARG(str, example_prompt))     # Kolin: You guys can activate this. This is just for me deu to the problem with LLM.

    sys.exit(app.exec())
