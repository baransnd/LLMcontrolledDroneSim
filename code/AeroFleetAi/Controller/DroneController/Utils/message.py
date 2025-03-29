from enum import Enum


class Types(str, Enum):
    ROLE = 'role'
    CONTENT = 'content'


class Roles(str, Enum):
    SYSTEM = 'system'
    USER = 'user'
    ASSISTANT = 'assistant'




class Message:
    role: Roles
    content: str

    def __init__(self, role, content):
        self.role = role
        self.content = content


    
    def to_json(self):
        return {
                Types.ROLE: self.role,
                Types.CONTENT: self.content
            }
    

    def get_content(self):
        return self.content
    
    def get_role(self):
        return self.role