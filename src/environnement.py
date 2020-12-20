import enum
import numpy as np
import threading

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
    def __init__(self, height:int, width:int) -> None:
        self.__mailBox:dict = dict()
        self.grid = np.full((height,width),"")
        self.__cellLocker = np.full((height,width), threading.Lock())
        self.h = height
        self.w = width
        self.lo = threading.Lock()
            
    def setGrid(self,ids:list, positions:list, goals:list) -> None:
        if len(ids) != len(positions):
            print("Erreur set de la grille impossible")
            exit(-1)
        self.goals = dict()
        for i in range(len(ids)):
            self.grid[positions[i][0]][positions[i][1]] = ids[i]
            self.goals[ids[i]] = goals[i]

    def getGoal(self, id:str)->tuple:
        return self.goals[id]
    
    def move(self, id:str,pos:tuple, newPos:tuple) -> bool:
        # Lock et unlock automatiquement
        # lock1:threading.Lock = self.__cellLocker[pos[0]][pos[1]]
        # lock2:threading.Lock = self.__cellLocker[newPos[0]][newPos[1]]
        hasMoved = False
        with self.lo:
            if self.grid[newPos[0]][newPos[1]] == "":
                self.grid[newPos[0]][newPos[1]] = id
                self.grid[pos[0]][pos[1]] = ""
                hasMoved = True
        if id == "🔴" and hasMoved :
            print(self.__str__())
        return hasMoved

    def sendMail(self, message: Message) -> None:
        if self.__mailBox[message.receiver] is None:
            self.__mailBox[message.receiver] = [message]
        else:
            self.__mailBox[message.receiver].append(message)

    def receiveMail(self,id:str) -> list:
        return self.__mailBox.get(id,[])
    
    def __str__(self) -> str:
        result = ""
        for line in self.grid:
            for value in line:
                if value == "":
                    result += "⬜"
                elif (len(value) == 1):
                    result += value
                else:
                    result += value
            result += "\n"
        return result