from PySide6.QtCore import QObject, Signal, Slot, QUrl
from PySide6.QtMultimedia import QAudioInput, QMediaCaptureSession, QMediaRecorder
import os
from openai import OpenAI
import whisper

from Controller.DroneController.Utils.message import Roles
from Controller.DroneController.Utils.message import Message



class SpeechToTextAdapter(QObject):
    
    status_signal = Signal(Message)
    response_signal = Signal(Message)
    finished = Signal()


    def __init__(self):
        super().__init__()
        self.model = whisper.load_model("base")
        self.setup_audio()
    

    def speech_to_text(self, audio_file):
        transcription = self.client.audio.transcriptions.create(file=audio_file)
        return transcription.text
        


    def setup_audio(self):
        self.is_recording = False
        self.audio_input = QAudioInput()
        self.media_session = QMediaCaptureSession()
        self.media_session.setAudioInput(self.audio_input)
        self.media_recorder = QMediaRecorder(
            self.media_session)  # Ensure media_recorder is initialized with the media session
        self.media_session.setRecorder(self.media_recorder)

        self.media_recorder.setQuality(QMediaRecorder.HighQuality)
        self.audio_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "TmpAudioFiles")
        self.audio_file_path = os.path.join(self.audio_file_path, "audio_output.m4a")
        self.media_recorder.setOutputLocation(QUrl.fromLocalFile(self.audio_file_path))
        


    @Slot()
    def toggle_audio_recording(self):
        if not self.media_recorder:  # Check if media_recorder is None or not initialized
            self.setup_audio()  # Initialize or setup audio components

        if self.is_recording:
            self.status_signal.emit(Message(Roles.SYSTEM, "Stopped recording audio."))
            self.stop_recording()
        else:
            self.status_signal.emit(Message(Roles.SYSTEM, "Started recording audio."))
            self.start_recording()
        



    def start_recording(self):
        self.media_recorder.record()
        self.is_recording = True
        #self.view_formatter.main_ui.pushButton_2.setText("Stop")


    def stop_recording(self):
        self.media_recorder.stop()
        self.is_recording = False
        #self.view_formatter.main_ui.pushButton_2.setText("")

        # Optional: Konvertieren Sie die Audioaufnahme in Text und fgen Sie sie in das Eingabefeld ein.
        #audio_text = self.transcribe_audio("output.mp3")
        #self.view_formatter.main_ui.lineEdit_input.setText(audio_text)
        print(self.check_audio_file())
        print("Loading: " + self.audio_file_path)
        #model.load_audio()
        transcription = self.model.transcribe(self.audio_file_path, fp16=False, language='English')['text']
        self.response_signal.emit(Message(Roles.ASSISTANT, transcription))


    def transcribe_audio(self, audio_file_path):
        # Implementieren Sie die Spracherkennung
        transcription = self.client.audio.transcriptions.create(file=audio_file_path)
        return transcription.text

    def check_audio_file(self):
        if os.path.exists(self.audio_file_path):
            print(f"Datei gefunden: {self.audio_file_path}")
            if os.path.getsize(self.audio_file_path) > 0:
                print("Die Datei enthaelt Daten.")
            else:
                print("Die Datei ist leer.")
        else:
            print("Keine Datei gefunden.")
