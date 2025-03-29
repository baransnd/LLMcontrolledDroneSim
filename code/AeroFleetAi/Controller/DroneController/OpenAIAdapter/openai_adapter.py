
'''@Kolin: direct connection to openai.

'''
'''
from openai import OpenAI

from Controller.DroneController.Utils.message import Roles
from Controller.DroneController.Utils.message import Message
import os




class OpenAiAdapter:

    def __init__(self, base_url="https://api.openai.com/v1/", api_key="NO_KEY", model="gpt-3.5-turbo"):
        self.url = base_url
        self.api_key = api_key
        self.model = model

        # Initialize OpenAI
        self.client = OpenAI(
            base_url = base_url,
            api_key = api_key,
        )

        # Create the chat history
        if os.path.exists('Controller/DroneController/OpenAIAdapter/Prompts/system_prompt.txt'):
            sys_prompt_path = os.path.abspath('Controller/DroneController/OpenAIAdapter/Prompts/system_prompt.txt')
        else:
            # Kolin: this path is for the integration test.
            sys_prompt_path = os.path.abspath('../../../../Controller/DroneController/OpenAIAdapter/Prompts/system_prompt.txt')
            
        with open(sys_prompt_path, "r") as f:
            sysprompt = f.read()

        self.chat_history = [Message(Roles.SYSTEM, sysprompt)]


    def process_completion(self, completion):   # Kolin: get the content from the answer from ai server.
        completion_text = ""
        for text in completion:
            completion_text += text
        return completion_text

    def ask(self, prompt):
        self.chat_history.append(Message(Roles.USER, prompt))

        json_chat_history = []
        for message in self.chat_history:
            json_chat_history.append(message.to_json())


        completion = self.client.chat.completions.create(
            model=self.model,
            messages=json_chat_history,
            temperature=0
        )

        completion_text = self._process_completion(completion)

        self.chat_history.append(Message(Roles.ASSISTANT, completion_text))

        return self.chat_history[-1]


#'''

''' without local LLM'''
#'''

from openai import OpenAI

from Controller.DroneController.Utils.message import Roles
from Controller.DroneController.Utils.message import Message
import asyncio
import sys
from g4f.Provider import You
import os

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())



class OpenAiAdapter:

    def __init__(self, base_url="https://api.openai.com/v1/chat/completions", api_key="NO_KEY", model="gpt-3.5-turbo"):
        self.url = base_url
        self.api_key = api_key
        self.model = model

        # Initialize OpenAI
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key,
        )

        # Create the chat history
        if os.path.exists('Controller/DroneController/OpenAIAdapter/Prompts/system_prompt.txt'):
            sys_prompt_path = os.path.abspath('Controller/DroneController/OpenAIAdapter/Prompts/system_prompt.txt')
        else:
            # Kolin: this path is for the integration test.
            sys_prompt_path = os.path.abspath('../../../../Controller/DroneController/OpenAIAdapter/Prompts/system_prompt.txt')
            
        with open(sys_prompt_path, "r") as f:
            sysprompt = f.read()

        self.chat_history = [Message(Roles.SYSTEM, sysprompt)]


    def _process_completion(self, completion):
        completion_text = ""
        for text in completion:
            completion_text += text
        return completion_text

    def ask(self, prompt):
        self.chat_history.append(Message(Roles.USER, prompt))

        json_chat_history = []
        for message in self.chat_history:
            json_chat_history.append(message.to_json())


        completion = You.create_completion(
            model="gpt-3.5-turbo",
            messages=json_chat_history,
            temperature=0)

        completion_text = self._process_completion(completion)

        self.chat_history.append(Message(Roles.ASSISTANT, completion_text))

        return self.chat_history[-1]

#'''