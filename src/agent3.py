from threading import main_thread
from environnement3 import *
import time
import random

class Agent(threading.Thread):
    """
    Agent's class
    """
    def __init__(self, env:Environment, id:str, position:tuple) -> None:
        """
        Init
        Args:
            grid : The environment
            id : the id of the agent
            goal : the goal of the agent
        """
        threading.Thread.__init__(self)
        self.env = env
        self.id = id
        self.pos = position
        self.nb_moves = 0
        self.waiting = False
        self.nextMove = None

    def run(self):
        """
        Execute le comportement de l'agent
        """
        print(self.id+" : Je démarre")
        self.goal = self.env.getGoal(self.id)
        for i in range(500000):
            messages, moves, freePlace = self.perception()
            move = self.reflexion(messages, moves, freePlace)
            if move is not None:
                if move in freePlace:
                    self.action(move)
                elif not self.waiting:
                    # Envoie du message bouge
                    receiver = self.getReceiver(move)
                    self.communication(receiver, Performative.REQUEST, Request.MOVE)
                    self.waiting = True
                    self.nextMove = move

    def perception(self):
        """
        Perception of the environment, we ask to the environment
        """
        self.goal = self.env.getGoal(self.id)
        messages = self.env.receiveMail(self.id)
        movesPotential = []
        freePlace = []
        for dir in [(0,1),(1,0),(0,-1),(-1,0)]:
            newx =  self.pos[0] + dir[0]
            newy =  self.pos[1] + dir[1]
            if (newx < self.env.h and newx >= 0 and
                newy < self.env.w and newy >= 0):
                if (self.env.isFreePlace(newx, newy)):
                    freePlace.append((newx, newy))
                if self.manhattanDistDecreases(newx, newy):
                    movesPotential.append((newx,newy))
        return messages, movesPotential, freePlace

    def reflexion(self, messages:list , moves: list, freePlace: list):
        """
        Reflexion of the future action
        """
        moveMessage, maxId = self.isThereMovementMessage(messages)
        if self.pos == self.goal and not moveMessage:
            return None
        if moveMessage:
            if len(freePlace) > 0:
                self.waiting = False
                self.nextMove = None
                return freePlace[0]
            else:
                if len(moves) != 0:
                    minDistance = self.env.h + self.env.w
                    minMove = []
                    for move in moves:
                        if self.manhattanDist(self.goal, move) < minDistance:
                            minDistance = self.manhattanDist(self.goal, move)
                            minMove.clear()
                            minMove.append(move)
                        if self.manhattanDist(self.goal, move) == minDistance:
                            minMove.append(move)
                    random.shuffle(minMove)
                    self.waiting = False
                    self.nextMove = None
                    return minMove[0]
                else:
                    return self.choiceMove()
        else:
            if self.waiting:
                if self.env.isFreePlace(self.nextMove[0], self.nextMove[1]):
                    self.waiting = False
                    self.nextMove = None
                    return self.nextMove
            if len(moves) != 0:
                minDistance = self.env.h + self.env.w
                minMove = None
                for move in moves:
                    if self.manhattanDist(self.goal, move) < minDistance:
                        minDistance = self.manhattanDist(self.goal, move)
                        minMove = move
                if self.env.isFreePlace(minMove[0], minMove[1]):
                    return minMove
                if (len(freePlace)>0):
                    return freePlace[0]
                else: 
                    return minMove
            elif self.pos == self.goal:
                return None
        return None

    def communication(self, dest:int, p:Performative, m:Request):
        """
        Send the message to the other agent
        """
        m = Message(self.id, dest, p, m)
        self.env.sendMail(m)

    def action(self, newPos:tuple):
        """
        Manage the action of the agent in the environment
        """
        if self.env.move(self.id, self.pos, newPos):
            self.pos = newPos
            self.nb_moves += 1

    def manhattanDist(self, pos1:tuple, pos2:tuple) -> int:
        """
        Calcule la distance de Manhattan entre deux points
        """
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def manhattanDistDecreases(self, posX, posY) -> bool:
        """
        Indique si en changeant de position, la distance de Manhattan pour 
        aller au but va diminuer
        """
        actualManhattanDist = self.manhattanDist(self.pos, self.goal)
        futureManhattanDist = self.manhattanDist((posX, posY), self.goal)
        return actualManhattanDist > futureManhattanDist

    def getNbMoves(self) -> int:
        """
        Renvoie le nombre de mouvements de l'agent
        """
        return self.nb_moves

    def isThereMovementMessage(self, messages) -> tuple:
        """
        Signale à l'agent si il a message lui demandant de bouger
        """
        for message in messages:
            if message.getContent() == Request.MOVE:
                sender = message.sender
                for i, mess in enumerate(messages):
                    if mess.getContent() == Request.MOVE:
                        # TODO : Répondre au destinataire (utile?)
                        if mess.getSender() > sender:
                            sender = mess.getSender
                        messages.pop(i)
                return True, sender
        return False, None

    def getReceiver(self, caseDest) -> str:
        """
        Donne le destinataire du message
        """
        return (self.env.getId(caseDest[0], caseDest[1]))

    def choiceMove(self):
        """
        Choisi une case aux hasard
        """
        potentialDest = []
        for dir in [(0,1),(1,0),(0,-1),(-1,0)]:
            newx =  self.pos[0] + dir[0]
            newy =  self.pos[1] + dir[1]
            if (newx < self.env.h and newx >= 0 and
                newy < self.env.w and newy >= 0):
                potentialDest.append((newx, newy))
        random.shuffle(potentialDest)
        return potentialDest[0]