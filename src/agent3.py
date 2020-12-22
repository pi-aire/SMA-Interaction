from environnement import *

class Request(enum.Enum):
    Move = 0
    CantMove = 1  # Très rare
    Yes = 2
    No = 3
    
class Content(object):
    """
        Content pour les agents de type 3
    """

    def __init__(self, request: Request, priority=0, positionS=None, positionR=None):
        self.request = request
        self.priority = priority  # La priorité peux être propagée si l'action nécessite
        self.positionS = positionS # Position du sender quand le message a été envoyé
        self.positionR = positionR # Position du receiver quand le message a été send

class Agent(threading.Thread):
    """
    Agent's class
    """

    def __init__(self, env: Environment, id: str, position: tuple) -> None:
        """
        Init
        Args:
            grid : The environment
            id : the id of the agent
            goal : the goal of the agent
        """
        threading.Thread.__init__(self)
        self.env: Environment = env
        self.id = id
        self.pos = position
        self.nb_moves = 0
        self.isWaiting = False # attend la réponse de ses voisins
        self.askNeighbours = []
        self.moveWait = dict() #le move attendu d'être faits
        # On calul le rang de l'agent
        self.rank = (self.env.h - self.pos[1]) * self.env.w
        self.rank += (self.env.w - self.pos[0])

    def run(self):
        print(self.id+" : Je démarre")
        self.goal = self.env.getGoal(self.id)
        # while self.pos[0] != self.goal[0] or self.pos[1] != self.goal[1]:
        for i in range(500):
            
            messages = self.perception()
            move = self.reflexion(messages)
            if not (move is None):
                self.action(move)
            # On si l'agent n'a pas atteind son objejectif
            if self.pos[0] == self.goal[0] and self.pos[1] == self.goal[1]:
                print(f"{self.id} : nb déplacement {self.nb_moves}")
                pass
                

    def perception(self):
        """
        Perception of the environment, we ask to the environment
        """
        messages = self.env.receiveMail(self.id)
        return messages

    def reflexion(self, messages: list):
        """
        Reflexion of the future action
        """
        
        # Si l'agent attend une réponse
        if self.isWaiting:
            selection= self.filterInformation(messages)
            if not (selection is None):
                self.isWaiting = False
                # On réalise l
                return self.moveWait[selection.sender]
                #On réalise le move que l'on souhaite
            elif len(self.askNeighbours) == 0:
                # Aucun voisin peux se déplacer
                print(f"{self.id} aucun voisin veut se déplacer")
                self.isWaiting = False
        else:
            # On cherche les messages interressants
            selection = self.bestRequest(messages)
            moves = self.env.moveAvailable(self.pos)
            if selection is None:
                if len(moves) != 0:
                    # On choisi un déplacement qui se rapproche de la solution
                    newDistance = [self.manhattanDist(
                        self.goal, npos) for npos in moves]
                    minVal = min(newDistance)
                    if self.manhattanDist(self.pos, self.goal) > self.manhattanDist(moves[newDistance.index(minVal)], self.goal):
                        return moves[newDistance.index(minVal)]
                    else:
                        return None
                else:
                    # On cherche les agents voisins
                    neighbours = self.env.neighbours(self.pos,self.rank)                    
                    if len(neighbours) == 0:
                        return None
                    newDistance = [self.manhattanDist(
                        self.goal, npos) for npos in neighbours]
                    minVal = min(newDistance)
                    posi = neighbours[newDistance.index(minVal)]
                    idN = self.env.grid[posi[0]][posi[1]]
                    if idN != "":
                        # On envoie une demande de dépalcement aux voisin
                        self.env.sendMail(
                            Message(self.id, idN, Performative.Request, Content(Request.Move, self.rank, self.pos, posi)))
                        # On sauvegarde la demande
                        self.askNeighbours.append(idN)
                        self.moveWait[idN] = posi
                        self.isWaiting = True
                    return None
            else:
                if len(moves) != 0:
                    # Libre peut faire de la place
                    # On choisi un déplacement libre
                    newDistance = [self.manhattanDist(
                        self.goal, npos) for npos in moves]
                    minVal = min(newDistance)
                    return moves[newDistance.index(minVal)]
                else:
                    # On fait une requête au autre voisin
                    c = Content(Request.Move,
                                    selection.content.priority,
                                    selection.content.positionS,
                                    selection.content.positionR)

                    for n in self.env.neighbours(self.pos,selection.content.priority):
                        idN = self.env.grid[n[0]][n[1]]
                        if idN != "" and idN != selection.sender:
                            self.env.sendMail(
                                Message(self.id, idN, Performative.Request, c))
                            # On sauvegarde la demande
                            self.askNeighbours.append(idN)
                            self.moveWait[idN] = n
                    self.isWaiting = True
                    return None

    def action(self, newPos: tuple):
        """
        Manage the action of the agent in the environment
        """
        if self.env.move(self.id, self.pos, newPos):
            self.pos = newPos
            self.nb_moves += 1

    def manhattanDist(self, pos1: tuple, pos2: tuple) -> int:
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def filterInformation(self, messages: list) -> list:
        selection = None
        for m in messages:
            if (m.performative == Performative.Informative
                and (m.content.request == Request.Yes or
                     m.content.request == Request.No)):
                if m.content.request == Request.Yes:
                    return m
                else:
                    self.askNeighbours.remove(m.sender)    
        return selection

    def bestRequest(self, messages: list) -> list:
        # On selectionne les messages des agents supérieurs
        selection = None
        maxPriority = -1
        for m in messages:
            if m.performative == Performative.Request and m.content.request == Request.Move:
                if (m.content.priority >= self.rank
                        and maxPriority < m.content.priority):
                    maxPriority = m.content.priority
                    selection = m
                else:
                    # on repond négativement
                    self.env.sendMail(
                        Message(self.id, m.receiver, Performative.Informative, Content(Request.No)))
        return selection
