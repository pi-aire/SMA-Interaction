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

    def __init__(self, sender: str, receiver: str, performative: Performative, content) -> None:
        self.sender: str = sender
        self.receiver: str = receiver
        self.performative: Performative = performative
        self.content = content


class Environment(object):
    """
    Environment's class
    """

    def __init__(self, height: int, width: int, agents:dict) -> None:
        self.__mailBox: dict = dict()
        self.grid = np.full((height, width), "")
        self.__cellLocker = np.full((height, width), threading.Lock())
        self.h = height
        self.w = width
        self.lo = threading.Lock()
        self.agents = agents
        self.state = (0,False)

    def setGrid(self, ids: list, positions: list, goals: list) -> None:
        if len(ids) != len(positions):
            print("Erreur set de la grille impossible")
            exit(-1)
        self.goals = dict()
        for i in range(len(ids)):
            self.grid[positions[i][0]][positions[i][1]] = ids[i]
            self.goals[ids[i]] = goals[i]

    def getGoal(self, id: str) -> tuple:
        return self.goals[id]

    def move(self, id: str, pos: tuple, newPos: tuple) -> bool:
        # Lock et unlock automatiquement
        # lock1:threading.Lock = self.__cellLocker[pos[0]][pos[1]]
        # lock2:threading.Lock = self.__cellLocker[newPos[0]][newPos[1]]
        hasMoved = False
        with self.lo:
            if self.grid[newPos[0]][newPos[1]] == "":
                self.grid[newPos[0]][newPos[1]] = id
                self.grid[pos[0]][pos[1]] = ""
                hasMoved = True
        return hasMoved

    def sendMail(self, message: Message) -> None:
        if self.__mailBox.get(message.receiver) is None:
            self.__mailBox[message.receiver] = [message]
        else:
            self.__mailBox[message.receiver].append(message)

    def receiveMail(self, id: str) -> list:
        tmp = list(self.__mailBox.get(id, []))
        if tmp != []:
            self.__mailBox.pop(id)
        return tmp

    def neighbours(self,position:tuple, rank:int = -1) -> list:
        neighbours = []
        for dir in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            newx = position[0] + dir[0]
            newy = position[1] + dir[1]
            if (newx < self.h and newx >= 0 and
                newy < self.w and newy >= 0 and
                self.grid[newx][newy] != ""):
                if (rank == -1 or
                rank >= self.agents[self.grid[newx][newy]].rank):
                    neighbours.append((newx,newy))
        return neighbours

    def moveAvailable(self, position:tuple) -> list:
        moves = []
        for dir in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            newx = position[0] + dir[0]
            newy = position[1] + dir[1]
            if (newx < self.h and newx >= 0 and
                newy < self.w and newy >= 0 and
                self.grid[newx][newy] == ""):
                moves.append((newx, newy))
        return moves
    
    def isLock(self, id:str, rank:int, line:int) -> bool:
        for agent in self.agents.values():
            # On regarde si les agents de rank supérieur sont pas satisfait
            if (agent.id != id and 
                agent.rank > rank and 
                not agent.isSatisfied):
                return False
            # On regarde s'il n'y a pas d'agent de line plus basse
            if (agent.id != id and
                agent.pos[0] <= line and
                agent.line > line):
                return False
        return True
    
    def endGoal(self, step) -> bool:
        if self.state[0] == step:
            return self.state[1]
        else:
            for agent in self.agents.values():
                if not agent.isSatisfied:
                    self.state(step,False)
                    return False
            self.state(step, True)
            return True
                
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
