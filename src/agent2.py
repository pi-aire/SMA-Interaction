from environnement import *


class Content(object):
    """
        Content pour les agents de type 2
    """

    def __init__(self, pSender, pReceiver, priority):
        self.pSender = pSender  # Position du sender quand le message à été envoyé
        self.pReceiver = pReceiver  # Position du reciever quand le message à été send
        self.prioritySender = priority

class Agent(threading.Thread):
    """
    Agent's class
    """

    def __init__(self, barrier,env: Environment, id: str, position: tuple) -> None:
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
        self.nb_move = 0
        self.barrier = barrier
        self.goal = self.env.getGoal(self.id)
        # On calul le rang de l'agent
        self.rank = (self.env.h - self.goal[0]) * self.env.w
        self.rank -= self.goal[1]
        self.isSatisfied = self.pos[0] == self.goal[0] and self.pos[1] == self.goal[1]

    def run(self):
        print(self.id+" : Je démarre")
        print(self.id + " : Lancement")
        print(f"{self.id}: rang {self.rank}")
        self.barrier.wait()
        # endSolution = False
        counter = 1000
        # while self.pos[0] != self.goal[0] or self.pos[1] != self.goal[1]:
        while counter > 0:
            messages, moves = self.perception()
            move = self.reflexion(messages, moves)
            if not (move is None):
                self.action(move)
            self.barrier.wait()
            counter -= 1
        print(f"{self.id}: nombre de mouvement {self.nb_move}")

    def perception(self):
        """
        Perception of the environment, we ask to the environment
        """
        self.goal = self.env.getGoal(self.id)
        self.isSatisfied = self.pos[0] == self.goal[0] and self.pos[1] == self.goal[1]
        messages = self.env.receiveMail(self.id)
        moveAvailable = []
        for dir in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            newx = self.pos[0] + dir[0]
            newy = self.pos[1] + dir[1]
            if (newx < self.env.h and newx >= 0 and
                newy < self.env.w and newy >= 0 and
                    self.env.grid[newx][newy] == ""):
                moveAvailable.append((newx, newy))
        return messages, moveAvailable

    def reflexion(self, messages: list, moves: list):
        """
        Reflexion of the future action
        """
        if self.isSatisfied and self.env.isLock(self.id,self.rank):
            return None
        
        needToMove = False
        # On regarde les messages
        if len(messages) != 0:
            for m in messages:
                # On regarde si entre temps, les agents ne ses sont pas déplacé
                if (self.env.agents[m.sender].pos == m.content.pSender and
                        self.pos == m.content.pReceiver):
                    needToMove = True
                    break

        # on essaye de se déplacer au plus prét de l'objectif
        cDist = self.manhattanDist(self.pos, self.goal)
        if len(moves) != 0:
            newDistance = [self.manhattanDist(
                self.goal, npos) for npos in moves]
            minVal = min(newDistance)
            if needToMove or (not self.isSatisfied and minVal < cDist):  # On se déplace seulement pour ce rapprocher de l'objectif
                return moves[newDistance.index(minVal)]
        
        # on cherche les voisins et on prend celui qui permet de se rapprocher le plus de l'objectif
        neighbours = self.env.neighbours(self.pos, self.rank)
        if len(neighbours) != 0:
            newDistance = [self.manhattanDist(self.goal, npos)
                        for npos in neighbours]
            minVal = min(newDistance)
            pNeighbour = neighbours[newDistance.index(minVal)]
            idNeighbour = self.env.grid[pNeighbour[0]][pNeighbour[1]]
            
            # on envoye le message pour que le voisin
            self.env.sendMail(
                Message(self.id, idNeighbour,
                        Performative.Request,
                        Content(self.pos, pNeighbour, self.rank)))
        return None

    def action(self, newPos: tuple):
        """
        Manage the action of the agent in the environment
        """
        if self.env.move(self.id, self.pos, newPos):
            self.nb_move += 1
            self.pos = newPos

    def manhattanDist(self, pos1: tuple, pos2: tuple) -> int:
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
