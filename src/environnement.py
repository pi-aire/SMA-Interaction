import enum

class Performative(enum.Enum):
    Request = 0
    Informative = 1

class Message(object):
    """
    Message's class
    """
    def __init__(self, sender, receiver, performative, content) -> None:
        self.sender:str = sender
        self.receiver:str = receiver
        self.performative: Performative = performative
        self.content = content

class Environment(object):
    """
    Environment's class
    """
    def __init__(self) -> None:
        self.__mailBox:dict = dict()
        
        
    def sendMail(self, message: Message) -> None:
        if self.__mailBox[message.receiver] is None:
            self.__mailBox[message.receiver] = [message]
        else:
            self.__mailBox[message.receiver].append(message)

    def receiveMail(self,id:str) -> list:
        return self.__mailBox.get(id,[])