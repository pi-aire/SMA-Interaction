from environnement import *

class Agent(threading.Thread):
    """
    Agent's class
    """
    def __init__(self, barriere, env:Environment, id:str, position:tuple) -> None:
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

    def run(self):
        print(self.id+" : Je démarre")
        self.goal = self.env.getGoal(self.id)
        # while self.pos[0] != self.goal[0] or self.pos[1] != self.goal[1]:
        for i in range(1000):
            messages, moves = self.perception()
            move = self.reflexion(messages, moves)
            if not (move is None):
                self.action(move)
            if self.pos[0] == self.goal[0] and self.pos[1] == self.goal[1]:
                break

    def perception(self):
        """
        Perception of the environment, we ask to the environment
        """
        self.goal = self.env.getGoal(self.id)
        messages = self.env.receiveMail(self.id)
        moveAvailable = []
        for dir in [(0,1),(1,0),(0,-1),(-1,0)]:
            newx =  self.pos[0] + dir[0]
            newy =  self.pos[1] + dir[1]
            if (newx < self.env.h and newx >= 0 and
                newy < self.env.w and newy >= 0 and
                self.env.grid[newx][newy] == ""):
                moveAvailable.append((newx,newy))
        return messages, moveAvailable

    def reflexion(self, messages:list , moves: list):
        """
        Reflexion of the future action
        """
        ## Move simple
        cDist  = self.manhattanDist(self.pos,self.goal)
        if len(moves) != 0:
            newDistance = [ self.manhattanDist(self.goal,npos) for npos in moves]
            minVal = min(newDistance)
            if cDist > minVal:
                return moves[newDistance.index(minVal)]
        return None

    def communication(self, dest:int, p:Performative, m:Message):
        """
        Send the message to the other agent
        """
        # New message
        m(self.id, dest, p, m)
        self.env.sendMail(m)

    def action(self, newPos:tuple):
        """
        Manage the action of the agent in the environment
        """
        if self.env.move(self.id, self.pos, newPos):
            self.pos = newPos

    def manhattanDist(self, pos1:tuple, pos2:tuple) -> int:
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])