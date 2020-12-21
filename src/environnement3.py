import enum
import numpy as np
import threading

class Performative(enum.Enum):
    REQUEST = 0
    INFORMA = 1


class Request(enum.Enum):
    MOVE = 0 # Pour demander à un agent de se déplacer
    IWANT = 1 # Pour dire qu'on ne bougera pas (Si dans un angle)
    YES = 2 # Pour dire qu'on va bouger asap
    NO = 3 # Pour dire qu'on ne va pas bouger sauf obligation


class ContentA2(object):
    """
        Content pour les agents de type 2
    """
    def __init__(self, priority, place, action):
        self.priority = priority
        self.place = place
        self.action = action

class Message(object):
    """
    Message's class
    """
    def __init__(self, sender, receiver, performative, content) -> None:
        self.sender:str = sender
        self.receiver:str = receiver
        self.performative: Performative = performative
        self.content = content
    
    def getContent(self) -> Request:
        """
        Retourne le contenu d'un message, 
        utilisé pour savoir si on doit bouger ou pas
        """
        return self.content

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
        self.angle = list()
        self.angle.append((0,0))
        self.angle.append((0,height))
        self.angle.append((0,width))
        self.angle.append((height, width))
            
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
            #print(self.__str__())
            pass
        return hasMoved

    def sendMail(self, message: Message) -> None:
        if self.__mailBox.get(message.receiver) is None:
            self.__mailBox[message.receiver] = [message]
        else:
            self.__mailBox[message.receiver].append(message)

    def receiveMail(self,id:str) -> list:
        return self.__mailBox.get(id,[])

    def getAngle(self) -> list:
        return self.angle

    def isFreePlace(self, posX: int, posY: int) -> bool:
        return (self.grid[posX][posY]== "")

    def getId(self, caseX, caseY):
        return self.grid[caseX][caseY]

    def printRequest(self) -> str:
        print(self.__str__())

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